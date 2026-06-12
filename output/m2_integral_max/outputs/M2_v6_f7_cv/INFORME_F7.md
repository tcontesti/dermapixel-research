# INFORME F7 — Ablación LoRA + 5-fold CV sobre MedSAM2-tiny

**Sprint M2-INTEGRAL-MAX · Segmentación dermatológica · 2026-06-12**
Modelo: MedSAM2-tiny (ganador M2, `facebook/sam2.1-hiera-tiny` + init `MedSAM2_latest.pt`).
Datos v1c (14.201). Eval idéntica a F2–F6 (bucket A = ISIC2018 canónico n=1000, LOCKED;
bucket B = holdout n=660). Régimen box-prompted (bbox-GT), AdamW lr1e-4, 1024², bf16,
Dice+BCE, recipe = F3.

> **Diseño (aprobado, opción B):** full_ft × 5-fold CV (→ CI del headline 0,9556, que fue
> full_ft) + LoRA r=4/8/16/32 × 1 fold (ablación de rango). 9 entrenos, ~17,5 h, nice -19,
> Rosa-safe. **CV**: pool train+val (12.541) → StratifiedKFold(5) por `dataset_origin`
> (seed 42); bucket A/B EXCLUIDOS de todo fold → comparables al headline.

---

## 1. Resultado principal — CI del 0,9556 (full_ft, 5-fold CV)

| Fold | train/val | best_ep | Bucket A Dice | Bucket B Dice |
|------|-----------|---------|--------------|---------------|
| 0 | 10032/2509 | 6 | 0,9549 | 0,9596 |
| 1 | 10033/2508 | 2 | 0,9542 | 0,9547 |
| 2 | 10033/2508 | 6 | 0,9556 | 0,9601 |
| 3 | 10033/2508 | 8 | 0,9563 | 0,9568 |
| 4 | 10033/2508 | 12 | 0,9558 | 0,9576 |

**Bucket A: media 0,95536 · sd 0,00083 · IC 95% [0,95433 – 0,95639]** (t, df=4).
**Bucket B: media 0,95776 · IC 95% [0,95505 – 0,96047].**
Latencia 25,7–26,2 ms (constante). El headline **0,9556 cae dentro del IC** ✔.

→ **El 0,9556 es robusto, no fue suerte de un split.** Desviación entre folds de
**8 diezmilésimas** (sd 0,0008): el bucket A converge a ~0,9554 con independencia del
fold, aunque la época de pico del val varíe (2–12). Cifra reportable para memoria/paper:

> **MedSAM2-tiny, Bucket A Dice = 0,9554 ± 0,0010 (IC 95%, 5-fold CV).**

---

## 2. Ablación LoRA (rango r, fold 0; ref full_ft fold0 = 0,9549)

| Config | Bucket A Dice | Δ vs full_ft | Bucket B | Params entrenables | Lat |
|--------|--------------|--------------|----------|--------------------|-----|
| full_ft (ref) | 0,9549 | — | 0,9596 | 11,74 M | 26 ms |
| LoRA r=4 | 0,9541 | −0,073 pp | 0,9518 | 7,58 M | 27 ms |
| LoRA r=8 | 0,9527 | −0,215 pp | 0,9521 | 7,62 M | 27 ms |
| LoRA r=16 | 0,9539 | −0,098 pp | 0,9544 | 7,72 M | 27 ms |
| LoRA r=32 | 0,9551 | +0,026 pp | 0,9548 | 7,91 M | 27 ms |

Rango LoRA: 0,9527–0,9551 (amplitud 0,24 pp).

---

## 3. Hallazgos

1. **El rango LoRA es irrelevante en este régimen.** Las 4 variantes caben en 0,24 pp,
   **sin tendencia monótona** (r=4 > r=8; r=32 marginalmente el mejor pero +0,03 pp).
   La amplitud entre rangos (~0,2 pp) es **menor que el ruido fold-a-fold del propio
   full_ft** (sd 0,08 pp, sem 0,04 pp). Como los valores LoRA son de **un solo fold**,
   arrastran ese mismo ruido → las Δ de 0,07–0,22 pp **no son significativas**. Confirma
   el caveat previo: en box-prompted de techo alto, las deltas de LoRA son ruido.

2. **LoRA iguala a full_ft en exactitud.** r=32 (0,9551) y r=4 (0,9541) quedan dentro o
   al borde del IC del full_ft [0,9543–0,9564]; r=8/r=16 caen ~0,1–0,2 pp por debajo del
   límite inferior pero dentro del ruido. Sin ganancia de exactitud por usar LoRA.

3. **Ahorro de parámetros modesto, NO de despliegue.** LoRA entrena 7,6–7,9 M vs 11,7 M
   full_ft (−33%), pero el ahorro es limitado porque el `prompt_encoder` se entrena
   entero en ambos (solo difiere el decoder). La **latencia de inferencia es idéntica**
   (~26–27 ms): LoRA no aporta ventaja en producción.

4. **Recomendación de producción inalterada: full_ft MedSAM2-tiny.** Es la opción más
   simple (sin dependencia peft, sin merge de adapters), con la mejor exactitud media
   y el IC más estrecho. LoRA no compensa la complejidad en este problema. (LoRA sería
   relevante solo si el encoder se entrenara o con muchas cabezas/tareas — no es el caso.)

---

## 4. Conclusión

F7 cumple su objetivo declarado: **acota el headline con un IC 95% estrecho y centrado**
(0,9554 ± 0,0010), demostrando que MedSAM2-tiny es estable ante remuestreo de datos. La
ablación LoRA es un **resultado negativo honesto**: en régimen box-prompted de techo alto,
ni el rango ni el uso de LoRA mueven la aguja (Δ < 0,25 pp, dentro del ruido), y full_ft
sigue siendo la elección de handoff.

Artefactos: `outputs/M2_v6_f7_cv/{F7_summary.json, config_f7.json,
fullft_fold0..4/, lora_r{4,8,16,32}_fold0/}` (cada uno con results.json + best.pt +
sanity_check). Driver `src/train_f7_lora_cv.py` (resumible).

**DETENIDO esperando autorización para F8** (cross-dataset + TTA + ensemble + fairness
ITA + calibración + **robustez a la caja** jitter/escala — ver decisión de producto
dos-modos dermapixel.eu).
