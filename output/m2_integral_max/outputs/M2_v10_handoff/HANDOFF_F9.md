# HANDOFF F9 — MedSAM2-tiny para dermapixel.eu (segmentación de lesión)

**Sprint M2-INTEGRAL-MAX · 2026-06-12 · panderm research → producción**
Modelo de segmentación recomendado tras comparar 6 arquitecturas (F2–F8).
Entrega para integración en dermapixel.eu con **switch de dos modos**.

> Charter: investigación entrena/evalúa; producción integra. Este handoff documenta
> qué desplegar y con qué garantías. **Pesos + metadata + comando reproducible incluidos.**

---

## 0. Qué se entrega (`outputs/M2_v10_handoff/`)

| Archivo | Qué es |
|---|---|
| `best.pt` | Pesos SLIM (16,9 MB): `sam_mask_decoder` + `sam_prompt_encoder` full_ft. sha256 `972131ac…`. **No incluye el encoder** (viene de MedSAM2). |
| `metadata.json` | Model card reproducible (charter regla 10): arquitectura, recipe, hashes, comando de entreno, todas las cifras F2–F8. |
| `infer_example.py` | Inferencia mínima reproducible (carga + forward box-prompted). |
| `HANDOFF_F9.md` | Este documento. |

**Carga (resumen):** `build_sam2_hf('facebook/sam2.1-hiera-tiny')` → cargar
`MedSAM2_latest.pt` (HF `wanglab/MedSAM2`, encoder médico) → cargar `best.pt['state']`
(`strict=False`). Forward = box-prompt, 1024², norm ImageNet, bf16. Ver `infer_example.py`.

---

## 1. Modelo

- **Arquitectura**: SAM2.1 Hiera-tiny, encoder con pretraining médico (MedSAM2), full-FT
  del `mask_decoder` + `prompt_encoder` (encoder congelado). 11,7 M params entrenables / 39 M total.
- **Entrada**: imagen 1024×1024 + **una bounding box** [x1,y1,x2,y2]. **Salida**: máscara binaria.
- **Latencia**: **25,6 ms** por imagen (1024², GPU). VRAM baja (tiny).
- **Por qué este**: gana a las otras 4 SAM en bucket A (Wilcoxon p≪0,001) y empata/supera a
  modelos 6–24× mayores. LoRA r=4/8/16/32 NO mejora (Δ<0,25 pp) → full_ft, más simple.

---

## 2. Los DOS modos de despliegue

### Modo 1 — INTERACTIVO (el clínico dibuja la caja)
- La caja del clínico ≈ caja-GT → **techo de calidad**.
- **Dice esperado: 0,956** · **IC 95 % [0,9543 – 0,9564]** (5-fold CV, F7).
- **Tolerante a imprecisión**: jitter de esquinas de ±20 px → solo −0,86 pp. El clínico no
  necesita dibujar la caja con precisión de píxel.

### Modo 2 — AUTOMÁTICO (detector de lesión → caja → MedSAM2-tiny)
- La calidad depende del **detector**. La caja imperfecta degrada el Dice según esta curva
  (medida en bucket A, §F8):

| Caja del detector | Dice |
|---|---|
| Perfecta (= GT) | 0,956 |
| Floja +10 % | **0,927** |
| Floja +20 % | 0,868 |
| Apretada −10 % | 0,888 |
| Apretada −20 % | **0,802** |

- **Cifra esperada con buen detector: ~0,93.**
- ⚠️ **SPEC OBLIGATORIA DEL DETECTOR**: la caja debe **cubrir toda la lesión + ~10 % de
  margen**. **Sesgar SIEMPRE hacia cajas flojas, NUNCA apretadas.** Encoger la caja recorta
  la lesión (el modelo solo segmenta el interior) y es **mucho peor** que agrandarla a IoU
  comparable. Una caja −20 % cuesta −15 pp; una caja +10 % solo −2,8 pp.

---

## 3. Cifras de respaldo (F2–F8)

| Métrica | Valor |
|---|---|
| Bucket A (ISIC2018 canónico, n=1000) | **0,9562** (0,9556 pareado) |
| Bucket B (holdout, n=660) | 0,9570 |
| 5-fold CV (F7) | **0,9554 ± 0,0010** (IC95 [0,9543–0,9564]) |
| vs baseline producción M2_v0 (0,9473) | **+0,83 pp** |
| Cross-dataset (HAM/ISIC18/ISIC17/PH2) | 0,960 / 0,946 / 0,941 / 0,962 |
| Equidad ITA pseudo-Fitzpatrick (gap) | **1,1 pp** (equitativo entre tonos) |
| Calibración pixel-ECE vs GT | 0,0082 (bien calibrado) |
| Baseline automático sin caja (F6 U-Net) | 0,8811 (contexto: la caja vale ~6,5–7,5 pp) |

**Comparativa SAM (bucket A, todas Wilcoxon p≪0,001):** MedSAM2-tiny 0,9562 > SAM2.1-tiny
0,9517 > SAM2.1-Large 0,9503 > SAM-Med2D 0,9465 > MedSAM-v1 0,9458.

---

## 4. Nota supra-anotador (IMA++ multi-anotador)

Sobre las 312 imágenes de bucket A con ≥2 anotadores humanos (IMA++):

- **Acuerdo entre humanos (IAA, Dice par-a-par): 0,728.** La frontera de la lesión es
  genuinamente ambigua; ni los expertos coinciden mucho.
- **MedSAM2-tiny vs consenso humano (majority vote): 0,915** — concuerda con el consenso
  **mucho mejor que los humanos entre sí**.
- **Dentro del envelope humano en el 97,8 % de los casos** (model-vs-consenso ≥ peor par humano).
- → El **ruido de etiqueta intrínseco (~0,73) es el techo real** de la tarea; el modelo es
  **supra-anotador** en consistencia. La cifra de 0,956 vs GT está por encima del acuerdo humano.
- **Caveat honesto**: el modelo es **sobre-confiado en bordes ambiguos** (ECE vs soft-label
  humano 0,094 vs 0,008 contra GT dura): predice contornos nítidos donde los humanos dudan.
  No afecta al Dice pero conviene saberlo si se muestran probabilidades al clínico.

---

## 5. Recomendaciones de integración

1. Desplegar **single MedSAM2-tiny full_ft** (TTA/ensemble solo dan +0,13–0,14 pp, no compensan).
2. **Modo interactivo** como referencia de calidad (0,956); **modo automático** detrás de un
   detector que cumpla la spec de caja floja (§2).
3. Umbral de máscara 0,5; norma ImageNet; 1024². Reescalar la máscara de salida al tamaño
   original de la imagen para overlay.
4. Mostrar la probabilidad como mapa de confianza es válido, pero recordar el caveat de
   sobre-confianza en bordes (§4).

Artefactos de evaluación que respaldan estas cifras: `outputs/M2_v6_f7_cv/`,
`outputs/M2_v7_f8_box_robustness/`, `outputs/M2_v8_f8_analyses/`, `outputs/M2_v9_f8_imapp/`,
informes `INFORME_F7.md` / `INFORME_F8.md`.
