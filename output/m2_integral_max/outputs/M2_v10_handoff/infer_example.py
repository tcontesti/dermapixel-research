#!/usr/bin/env python3
"""Minimal reproducible inference for the M2 handoff model (MedSAM2-tiny).

Loads: SAM2.1-hiera-tiny  +  MedSAM2_latest.pt (encoder/medical init)  +
       best.pt (our slim full_ft mask_decoder + prompt_encoder).
Runs a single box-prompted segmentation. Both deployment modes only differ in
WHERE the box comes from (clinician vs detector); the forward pass is identical.

Deps: torch, sam2 (SAM2 repo), numpy, pillow, huggingface_hub.
"""
import numpy as np, torch, torch.nn.functional as F
from PIL import Image

DEVICE = 'cuda'
S = 1024
IMNET_MEAN = np.array([0.485, 0.456, 0.406], np.float32)
IMNET_STD = np.array([0.229, 0.224, 0.225], np.float32)


def load_model(best_pt='best.pt'):
    from sam2.build_sam import build_sam2_hf
    from huggingface_hub import hf_hub_download
    m = build_sam2_hf('facebook/sam2.1-hiera-tiny').to(DEVICE)
    # 1) medical encoder + base from MedSAM2
    init = hf_hub_download('wanglab/MedSAM2', 'MedSAM2_latest.pt')
    ck = torch.load(init, map_location=DEVICE, weights_only=False)
    m.load_state_dict(ck['model'] if (isinstance(ck, dict) and 'model' in ck) else ck, strict=False)
    # 2) our slim full_ft decoder + prompt encoder
    best = torch.load(best_pt, map_location=DEVICE, weights_only=False)
    m.load_state_dict(best['state'], strict=False)
    m.eval()
    return m


@torch.no_grad()
def segment(model, image_path, box_xyxy):
    """box_xyxy: [x1,y1,x2,y2] in 1024-resized image coords.
    INTERACTIVE mode: box drawn by clinician.  AUTOMATIC mode: box from a lesion
    detector -> MUST cover the whole lesion + ~10% padding, NEVER tight
    (under-coverage costs up to -15 Dice pts; see box-robustness curve)."""
    raw = np.array(Image.open(image_path).convert('RGB').resize((S, S), Image.BILINEAR), np.float32)
    img = torch.from_numpy((raw / 255. - IMNET_MEAN) / IMNET_STD).permute(2, 0, 1)[None].float().to(DEVICE)
    box = torch.as_tensor(box_xyxy, dtype=torch.float32)[None].to(DEVICE)
    bb = model.forward_image(img)
    _, vf, _, fs = model._prepare_backbone_features(bb)
    if model.directly_add_no_mem_embed:
        vf[-1] = vf[-1] + model.no_mem_embed
    feats = [f.permute(1, 2, 0).view(1, -1, *s) for f, s in zip(vf[::-1], fs[::-1])][::-1]
    se, de = model.sam_prompt_encoder(points=None, boxes=box, masks=None)
    low, _, _, _ = model.sam_mask_decoder(
        image_embeddings=feats[-1], image_pe=model.sam_prompt_encoder.get_dense_pe(),
        sparse_prompt_embeddings=se, dense_prompt_embeddings=de,
        multimask_output=False, repeat_image=False, high_res_features=feats[:-1])
    prob = torch.sigmoid(F.interpolate(low, (S, S), mode='bilinear', align_corners=False).float())[0, 0].cpu().numpy()
    return (prob > 0.5).astype(np.uint8), prob  # binary mask, probability map


if __name__ == '__main__':
    import sys
    model = load_model(sys.argv[1] if len(sys.argv) > 1 else 'best.pt')
    mask, prob = segment(model, sys.argv[2], [int(x) for x in sys.argv[3:7]])
    print('mask sum', int(mask.sum()), 'prob max', float(prob.max()))
