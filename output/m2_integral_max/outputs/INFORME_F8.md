# INFORME F8 — Robustez, generalización, equidad y calibración de MedSAM2-tiny

**Sprint M2-INTEGRAL-MAX · Segmentación dermatológica · 2026-06-12**
Modelo evaluado: **MedSAM2-tiny** (ganador M2, F3 `M2_v2_medsam2/best.pt`), box-prompted.
Todo eval-only sobre bucket A (ISIC2018 canónico, n=1000, LOCKED) y bucket B (holdout n=660).
Eval idéntica a F2–F7 (`eval_metrics.py`, 1024²). nice -19, Rosa-safe.

---

## 1. ⭐ Robustez a la caja (PRIORIDAD — decide el modo automático del switch)

Estima la calidad del **modo automático** (detector→caja→MedSAM2) degradando la bbox-GT y
midiendo Dice. Techo = **modo interactivo** (clínico dibuja la caja ≈ GT).

| Perturbación | box-IoU vs GT | Dice | Δ vs GT | HD95 |
|---|---|---|---|---|
| **GT (techo, interactivo)** | 1.000 | **0.9558** | — | 23.0 |
| jitter ±5 px | 0.980 | 0.9551 | −0.07 | 23.1 |
| jitter ±10 px | 0.960 | 0.9536 | −0.22 | 23.7 |
| jitter ±20 px | 0.923 | 0.9472 | −0.86 | 26.6 |
| escala +10 % (floja) | 0.848 | 0.9274 | −2.84 | 36.9 |
| escala −10 % (apretada) | 0.810 | 0.8877 | −6.81 | 52.1 |
| escala +20 % | 0.738 | 0.8679 | −8.79 | 61.1 |
| escala −20 % (apretada) | 0.640 | 0.8020 | **−15.38** | 85.1 |

**Hallazgos (→ spec del detector para F9):**
- **El jitter de esquinas es casi inocuo** (±20 px → −0.86 pp). La precisión exacta de las
  esquinas del detector NO es crítica.
- **La escala SÍ es crítica y asimétrica**: a IoU comparable, **encoger es mucho peor que
  agrandar** (−10 % → −6.8 pp vs +10 % → −2.8 pp; −20 % → −15.4 pp). Una caja apretada
  recorta la lesión y el modelo solo segmenta el interior.
- **Regla de despliegue**: el detector debe sesgar hacia cajas **ligeramente flojas**
  (cubrir toda la lesión + ~10 % margen), nunca apretadas. Coverage ≫ precisión de borde.

---

## 2. Mejoras de inferencia — TTA y Ensemble (bucket A)

| Método | Dice | Δ vs base | HD95 |
|---|---|---|---|
| Base (single MedSAM2-tiny) | 0.9558 | — | 23.0 |
| TTA 4-vistas (id/hflip/vflip/both) | 0.9571 | +0.13 | — |
| Ensemble 5 modelos (5-fold F7) | 0.9572 | +0.14 | — |

Ambos aportan **ganancias marginales (~0.13–0.14 pp)**: en régimen box-prompted de techo
alto no hay margen. Ensemble ≈ TTA, pero el ensemble cuesta 5× cómputo y 5× memoria →
**no compensa en producción**; TTA es gratis en memoria si se quiere exprimir ese 0.1 pp.

---

## 3. Cross-dataset — generalización por origen (bucket B, n=660)

| Dataset | n | Dice |
|---|---|---|
| PH2 | 9 | 0.9621 |
| HAM10000 | 501 | 0.9597 |
| ISIC2018 | 135 | 0.9459 |
| ISIC2017 | 15 | 0.9413 |

Generaliza de forma consistente (0.941–0.962). El grueso (HAM10000) es el más alto; ISIC17/18
algo menores (y con n pequeño en ISIC17/PH2). Sin caída de dominio relevante.

---

## 4. Equidad — fairness ITA pseudo-Fitzpatrick (bucket A, n=1000)

`fitzpatrick_type` ausente en el manifiesto → **ITA calculado** (Individual Typology Angle)
sobre la **piel peri-lesional** (píxeles no-lesión, no-viñeta), agrupado en escala tipo
Fitzpatrick (Kinyanjui).

| Grupo (ITA) | n | Dice |
|---|---|---|
| I muy claro (>55°) | 574 | 0.956 |
| II claro (41–55°) | 126 | 0.961 |
| III intermedio (28–41°) | 122 | 0.956 |
| IV tan (10–28°) | 100 | 0.950 |
| V–VI moreno/oscuro (<10°) | 78 | 0.950 |

**Gap máximo 1.1 pp.** El modelo es **equitativo** entre tonos, con un dip leve y esperado en
los grupos más oscuros (IV, V–VI: 0.950 vs 0.961 en II). Caveat: ITA sobre imagen dermoscópica
es un **proxy** (piel peri-lesional bajo dermatoscopio), no Fitzpatrick clínico real; pero el
spread es pequeño y consistente.

---

## 5. Calibración

### 5a. Pixel-calibración vs GT (bucket A, n=1000)
**ECE (15 bins) = 0.0082 · Brier = 0.0187.** El modelo está **bien calibrado** respecto a la
máscara dura: sus probabilidades de píxel reflejan la frecuencia real de lesión.

### 5b. Multi-anotador IMA++ (subset bucket A con ≥2 anotadores, n=312, 2.3 anot/img)
Compara MedSAM2-tiny (box = GT, modo interactivo) contra varias anotaciones humanas.

| Métrica | Valor |
|---|---|
| **IAA humano** (Dice par-a-par entre anotadores) | **0.728** |
| Model Dice vs consenso MV (majority vote) | **0.915** |
| Model Dice vs v1c GT (ISIC oficial) | 0.9405 |
| Dentro del envelope humano (model-vs-MV ≥ peor par humano) | **97.8 %** |
| ECE vs soft-label humano (acuerdo por píxel) | 0.094 |
| Brier vs soft-label humano | 0.047 |

**Hallazgos:**
- **El modelo concuerda con el consenso humano (0.915) mucho mejor que los humanos entre sí
  (IAA 0.728).** El límite real de la tarea es el **ruido de etiqueta intrínseco** (~0.73 de
  acuerdo humano), por debajo del techo del modelo (0.956). MedSAM2-tiny está **dentro o por
  encima del envelope humano en el 97.8 % de los casos** → consistencia supra-anotador.
- **Sobre-confianza en bordes ambiguos**: el ECE vs soft-label humano (0.094) es mayor que el
  pixel-ECE vs GT (0.0082). El modelo predice máscaras nítidas (0/1) mientras los humanos
  muestran incertidumbre graduada en el borde; el modelo **no expresa esa incertidumbre de
  contorno**. Es bien-calibrado contra GT dura pero algo sobre-confiado frente a la
  variabilidad humana en los límites. (Mejora futura: probabilidades de borde más suaves.)

---

## 6. Conclusión y entradas para el handoff F9

1. **Modo interactivo (caja del clínico ≈ GT)**: techo **Dice 0.956** (IC95% [0.9543–0.9564]
   por F7). Tolerante a imprecisión de esquinas (±20 px ≈ sin pérdida).
2. **Modo automático (detector→caja)**: la cifra depende de la calidad del detector. La curva
   de §1 la cuantifica: con un detector que produzca cajas **ligeramente flojas** (~+10 %,
   sin recortar), Dice esperado **~0.93**; si el detector aprieta (−10/−20 %) cae a 0.80–0.89.
   **Spec para el detector**: maximizar coverage de la lesión, padding ~10 %, nunca recortar.
3. **Robustez confirmada**: equitativo entre tonos (gap 1.1 pp), generaliza cross-dataset
   (0.94–0.96), bien calibrado vs GT (ECE 0.008), y **supra-anotador** vs consenso humano
   (0.915 > IAA 0.728, dentro del envelope 97.8 %).
4. **TTA/Ensemble no compensan** (+0.13–0.14 pp); recomendación de despliegue = **single
   MedSAM2-tiny full_ft** (25.6 ms, 11.7 M params).

Artefactos: `outputs/M2_v7_f8_box_robustness/box_robustness.json`,
`outputs/M2_v8_f8_analyses/f8_analyses.json`,
`outputs/M2_v9_f8_imapp/imapp_calibration.json`. Scripts en `src/eval_f8_*.py`.

**DETENIDO esperando autorización para F9** (handoff: documentar los dos modos de despliegue
con techo caja-GT 0.956 y curva de caja imperfecta).
