# INFORME F6 — U-Net + ResNet101 (control clásico AUTOMÁTICO)

**Sprint M2-INTEGRAL-MAX · Segmentación dermatológica · 2026-06-10**
Datos: `m2_integral_max_v1c_local.parquet` (14.201 imgs). Eval idéntica a F2–F5
(bucket A = `test_canonical` n=1000 ISIC2018 canónico; bucket B = `holdout_combined`
n=660; per-dataset; HD95 scipy @1024²; latencia).

> ⚠️ **CAVEAT METODOLÓGICO — leer antes de la tabla.**
> U-Net es un segmentador **AUTOMÁTICO**: recibe solo la imagen y debe **localizar
> + segmentar** la lesión. Los modelos SAM (F2–F5) son **BOX-PROMPTED**: a cada uno
> se le entrega la *bounding box* GT en inferencia. **No es head-to-head de
> arquitectura.** U-Net se reporta en sección SEPARADA "baseline clásico
> automático". Nunca en la columna de ganador de los SAM.

---

## 1. Configuración

| | |
|---|---|
| Arquitectura | `segmentation_models_pytorch` U-Net, encoder ResNet101 ImageNet |
| Régimen | full fine-tune (sin LoRA, encoder entrenable), 51,5 M params |
| Pérdida | 0,5·BCE + 0,5·Dice | 
| Datos | v1c, train 10.659 / val 1.882, batch 8, 1024² |
| Schedule | AdamW lr 1e-4, warmup 300, coseno, patience 8 |
| Norma | ImageNet (0–1) |
| Prompt | **NINGUNO (automático)** |

Smoke `--smoke` verificado end-to-end antes del full run.
Convergencia: **best valDice 0,9365 @ ep27**, early-stop @ ep35 (~17,5 h, ~30 min/ep
a 1024² en GB10). Rosa monitorizada en producción durante las 35 épocas: estable a
11,57 GB, `status:ok`, cero contención. El run sobrevivió a 2 cortes de SSH (nohup).

---

## 2. Resultados F6 (AUTOMÁTICO)

### Bucket A — ISIC2018 canónico (n=1000)
| Dice | IoU | F1 | Precision | Recall | HD95 (px) | Latencia |
|------|-----|----|-----------|--------|-----------|----------|
| **0,8811** ±0,121 | 0,8037 | 0,8811 | 0,8556 | 0,9423 | 65,96 | 44,4 ms |

`vs_baseline_pp` (M2_v0 = 0,9473): **−6,62 pp**

### Bucket B — holdout combinado (n=660)
| Overall Dice | IoU | Precision | Recall | HD95 |
|------|-----|-----------|--------|------|
| 0,9386 ±0,085 | 0,8935 | 0,9455 | 0,9431 | 36,70 |

Per-dataset (bucket B):
| Dataset | n | Dice | HD95 |
|---------|---|------|------|
| HAM10000 | 501 | 0,9519 | 32,5 |
| ISIC2017 | 15 | 0,9269 | 29,9 |
| ISIC2018 | 135 | 0,8910 | 50,3 |
| PH2 | 9 | 0,9329 | 77,6 |

---

## 3. Tabla comparativa — SAM box-prompted vs U-Net automático

**Sección A — modelos BOX-PROMPTED (paradigma F2–F5, columna de ganador):**
| # | Modelo | Familia | Bucket A Dice | IoU | HD95 | Prec | Rec | Bucket B | Latencia | Params |
|---|--------|---------|--------------|-----|------|------|-----|----------|----------|--------|
| **F3** | **MedSAM2-tiny** med | SAM2.1 | **0,9562** | 0,918 | 22,9 | 0,965 | 0,950 | 0,9570 | 25,6 ms | 11,7 M |
| F3b | SAM2.1-tiny gen | SAM2.1 | 0,9519 | 0,911 | 25,6 | 0,960 | 0,947 | 0,9578 | 25,9 ms | 11,7 M |
| F2 | SAM2.1-Large gen | SAM2.1 | 0,9505 | 0,908 | 26,6 | 0,957 | 0,948 | 0,9562 | 95,9 ms | 11,7 M |
| F4 | SAM-Med2D med | SAM-v1 adapt | 0,9465 | 0,901 | 29,0 | 0,950 | 0,947 | 0,9487 | 20,3 ms* | 4,1 M |
| F5 | MedSAM-v1 med | SAM-v1 | 0,9460 | 0,900 | 30,3 | 0,947 | 0,949 | 0,9514 | 73,9 ms | 4,1 M |

\* SAM-Med2D opera a 256² (latencia @256).
Comparativa pareada Wilcoxon de los 5: `comparison_all5_bucketA.json` (todas p≪0,001).

**Sección B — baseline clásico AUTOMÁTICO (NO comparable head-to-head):**
| # | Modelo | Prompt | Bucket A Dice | IoU | HD95 | Prec | Rec | Bucket B | Latencia | Params |
|---|--------|--------|--------------|-----|------|------|-----|----------|----------|--------|
| F6 | U-Net ResNet101 | **AUTOMÁTICO (sin box)** | 0,8811 | 0,804 | 66,0 | 0,856 | 0,942 | 0,9386 | 44,4 ms | 51,5 M |

---

## 4. Hallazgos

1. **El box-prompt vale ~6,5–7,5 pp de Dice.** Sobre el MISMO bucket A canónico, el
   mejor automático (U-Net 0,8811) queda **−7,51 pp** bajo el mejor box-prompted
   (MedSAM2-T 0,9562), y **−6,49 pp** incluso bajo el SAM más débil (MedSAM-v1 0,9460).

2. **La brecha NO es arquitectura, es el prompt.** Todo el abanico de los 5 SAM
   (0,9460→0,9562) cabe en **~1,0 pp**; el efecto del prompt (~6,5–7,5 pp) es
   **6–7× mayor** que la diferencia entre cualquier par de arquitecturas SAM. Esto
   *valida* que la comparativa F2–F5 fue un contraste justo dentro del paradigma
   prompted — el factor dominante de toda la segmentación es disponer de la caja.

3. **Perfil de error característico del automático.** Recall alto (0,942 ≈ SAM) pero
   precision muy inferior (0,856 vs 0,95–0,965 de los SAM) y HD95 **2,5–3× peor**
   (66 vs 23–30 px). Sin caja que le diga *dónde*, U-Net encuentra píxeles de lesión
   (recall ok) pero se desborda a regiones erróneas / blobs falsos → colapsan
   precisión y exactitud de contorno. Desviación típica 0,121 (vs ~0,037 de SAM):
   algunas imágenes fallan catastróficamente.

4. **Mucho más sensible a la distribución.** val (dominado por HAM10000) 0,9365 vs
   bucket A (ISIC2018 canónico) 0,8811 → caída intra-modelo de 5,5 pt. El per-dataset
   lo confirma: HAM10000 0,952 (fácil, grueso del train) pero ISIC2018 0,891. Los SAM
   box-prompted se mantuvieron 0,9465–0,9562 en ese mismo bucket A: el automático es
   mucho menos robusto al cambio de distribución.

5. **Latencia.** 44 ms automático: más lento que MedSAM2-T (25,6) y SAM-Med2D
   (20,3@256), más rápido que SAM2.1-L (95,9) y MedSAM-v1 (73,9). Matiz justo: U-Net
   NO necesita bbox en inferencia (end-to-end real), mientras los SAM requieren un
   detector previo que produzca la caja (latencia de detección no contabilizada aquí).

---

## 5. Conclusión

F6 funciona como **control negativo** del sprint: cuantifica que la ventaja de los
SAM no es "saben segmentar mejor" sino "se les dice dónde". La recomendación de
handoff a producción **se mantiene inalterada: MedSAM2-tiny** (0,9556 val / 0,9562
bucket A, 25,6 ms, 11,7 M params). U-Net contextualiza *por qué* el paradigma
box-prompted es el correcto para este problema, y aporta un baseline automático
honesto (0,881 bucket A) para la memoria.

Artefactos: `outputs/M2_v5_unet_r101/{results.json, best.pt (197 MB), train.log,
sanity_check/*.png}`.

**DETENIDO esperando autorización para F7.**
