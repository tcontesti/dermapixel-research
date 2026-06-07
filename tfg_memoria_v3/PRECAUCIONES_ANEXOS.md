# Precauciones para redacción de Anexos F–J

Origen: auditoría `tfg-experiment-auditor` ejecutada el 2026-05-26 sobre
la versión `tfg_uib_70pv2/`. Detectó 2 contradicciones críticas (C1, C2)
y varias discrepancias menores entre lo afirmado en el TFG y lo
verificable en `results/`, `output/`, código y reportes técnicos.

En el TFG activo (`tfg_memoria_v3/`, paper-style) la mayoría de estos
gaps **no están activos todavía** porque los anexos correspondientes
(F, G, H, I, J) son esqueletos. Este documento lista las precauciones
que deben aplicarse cuando se redacten esos anexos para no reproducir
las inconsistencias detectadas.

---

## AnexoF · Sparse Autoencoders y diccionario de conceptos

### M2 · Sparsity del SAE

- **NO escribir**: «sparsity ≈ 15%».
- **Escribir**: «sparsity ≈ 16,5%».
- **Fuente**: `results/SAE_LARGE_RESULTS.md`.
- Justificación: el 15% es un redondeo grueso; el valor exacto que figura
  en los reportes del SAE Large es 16,5%. Si se mantiene el 15% como
  cifra aproximada, justificarlo explícitamente como objetivo de diseño,
  no como valor medido.

### M3 · CBM sobre SkinCon

- **NO escribir**: «AUROC 0,920 / 0,909».
- **Escribir**: «AUROC 0,880 / 0,864» (cifra agregada sobre el dataset
  completo SkinCon, 48 conceptos).
- **Si se desea reportar la cifra alta (0,920/0,909)**: aclarar
  explícitamente que corresponde a un subconjunto de los 22 conceptos con
  mayor cobertura, no a los 48 conceptos del dataset.
- **Fuente**: `results/SKINCON_CBM_RESULTS.md`.

---

## AnexoG · Recuperación visual aumentada (RAG)

Sin gaps detectados en la auditoría. Mantener la descripción del módulo
como recuperación visual densa (no como RAG generativo) tal y como queda
en Cap2 §2.4.

---

## AnexoH · Modelos de lenguaje multimodales: comparación extendida

### A6 · «Zona dulce 8–15 palabras» del prompt zero-shot

- **NO presentar** como resultado de un barrido sistemático de longitud
  de prompt.
- **Presentar** como observación cualitativa extrapolada de tres puntos
  discretos del experimento (Simple / Top-3 / Top-5).
- Si se quiere reportar la observación: declarar explícitamente que es
  una hipótesis sugerida por la comparación, no una conclusión empírica
  con N puntos de barrido y test estadístico.

### Coherencia con Cap2 §2.7

- Repetir las cifras de modelos accedidos por API (GPT-4o, Gemini~2.5~Pro)
  como tamaño no público.
- Para MedGemma~27B: dejar claro que la variante evaluada es la versión
  ajustada con LoRA ($r=8$) cuando se reporten cifras superiores al
  baseline; las dos variantes (con y sin LoRA) deben distinguirse en las
  tablas.

---

## AnexoI · Prototipo DermApIxel

### C1 · Arquitectura del clasificador unificado (CONTRADICCIÓN CRÍTICA)

- **NO escribir**: «tres cabezas lineales independientes que comparten
  el backbone, optimizadas mediante una pérdida que suma tres entropías
  cruzadas (una por nivel L1/L2/L3)».
- **Escribir**: «clasificador plano de 43 clases L3 (esquema
  \emph{merged43}), entrenado con \emph{cross-entropy} estándar; la
  lectura jerárquica L1/L2 se obtiene mediante agregación determinista
  post-hoc según el mapping \texttt{merged43\_hierarchy.json}».
- **Fuente**: el comando real de entrenamiento es `--nb_classes 43`,
  sin flag `--hier`. Confirmado en `AUDIT_SPARK_RESULTS.md` y en
  los logs de entrenamiento.
- **Riesgo**: el tribunal puede leer Cap5 y AnexoA simultáneamente en la
  versión `tfg_uib_70pv2/` y detectar la incoherencia. En el v3 actual
  no aparece esta narrativa en el cuerpo; cuidar AnexoI para no
  reintroducirla.

### A2 · Cifras del clasificador unificado L3

- **L3 Acc 81% / BAcc 81,8% / Top-3 95,4%** corresponden a la variante
  \emph{merged43 + TTA} (43 clases), NO a un L3 plano de 47 clases.
- Si se cita la cifra de L3 47 clases plano, es **79,7%** (sin la fusión
  47→43 ni TTA).
- Cap5 del `tfg_uib_70pv2/` ya menciona la fusión 47→43 correctamente;
  AnexoI debe ser coherente con esta nomenclatura.

### A4 · Cinco estrategias L3

- **NO afirmar** que existe una tabla comparativa de las cinco
  estrategias evaluadas (focal loss, weighted CE, continued pretraining,
  augmentaciones, TTA).
- **Reportar** sólo la estrategia ganadora (\emph{merged43 + TTA}) con
  sus cifras finales y mencionar las cuatro restantes como estrategias
  exploradas con resultado inferior, sin tabla cuantitativa.
- `results/` no preserva las cuatro estrategias intermedias.

---

## AnexoJ · Caminos abiertos y trabajo futuro

### C2 · Composición real del ensemble OR melanoma (CONTRADICCIÓN
CRÍTICA)

- **NO escribir**: «ensemble M1 + M7 + SigLIP alcanza recall 100% sobre
  HAM10000».
- **Escribir**: «el ensemble OR top-3 entre M1 (PanDerm Large
  fine-tuned sobre HAM10000) y SigLIP-Large SO400M es suficiente para
  alcanzar recall melanoma del 100% sobre el \emph{split} de test de
  HAM10000 ($N = 70$ melanomas, top-3); M7 (clasificador unificado de
  43 clases sobre el corpus armonizado) no añade melanomas adicionales
  sobre HAM, pero mantiene valor en escenarios multidataset por su
  cobertura ontológica más amplia».
- **Fuente**: `output/ensemble_eval/ENSEMBLE_REPORT.md`.
- **Caveats explícitos** a incluir:
  - El recall del 100% es \textbf{top-3}, no top-1.
  - El tamaño muestral es $N = 70$ melanomas; los intervalos de
    confianza al 95% son amplios.
  - No se ha validado prospectivamente sobre cohorte hospitalaria.

### Otros elementos sin gap detectado

- Cinco bloques derivados (ontología, ensemble, equidad, SAE, RAG,
  prototipo): se mencionan como contribuciones en Cap1 §1.9 y se
  desarrollan en sus anexos respectivos.
- Roadmap TFM y agéntica: describir como líneas abiertas sin
  comprometer cifras concretas ni plazos.
- Derm7pt + SAE (quick win #4 de la memoria activa): mencionar como
  línea concreta con experimentos E1–E4 identificados pero no
  ejecutados.

---

## Cap4 Resultados · tabla `tab:equidad`

### A1 · AUROC de PanDerm en fairness

- **NO escribir**: «AUROC 0,912».
- **Escribir**: «AUROC 0,908».
- **Gap entre fototipos extremos**: 8,9 pp (0,089) — esta cifra sí
  coincide entre el TFG y los reportes técnicos, mantenerla.
- **Fuente**: `tfg_figures/fairness_5models/summary_5models.md`.

### Resto de la tabla

Cuando se rellenen las cifras `[NE]` del Cap4 §4.6, verificar
celda-a-celda contra `summary_5models.md` y no contra cifras agregadas
de `RESULTADOS_TFG.md` (que están redondeadas).

---

## Cap3 §3.3 · DermapixelAI (ya aplicado en v3)

### M1 · Distinción label_source vs rosa_verified

Aplicado el 2026-05-26 en `Cap3_MaterialesMetodos.tex`. El texto actual
declara explícitamente las dos cifras:
- 97,93% \texttt{label\_source = ontology}: mapeo ontológico con
  revisión experta del vocabulario.
- 82,96% \texttt{rosa\_verified}: revisión visual caso-a-caso por la
  Dra.~Taberner.

El AnexoC ya detalla las tres cifras de validación
(\texttt{label\_source}, \texttt{diagnosis\_source}, \texttt{rosa\_verified})
y declara su no-intercambiabilidad.

---

## Resumen de gaps por severidad

| ID | Anexo destino | Severidad | Estado en v3 |
|---|---|---|---|
| C1 | AnexoI | BLOQUEANTE | Pendiente (placeholder) |
| C2 | AnexoJ | BLOQUEANTE | Pendiente (placeholder) |
| A1 | Cap4 tab:equidad | IMPORTANTE | Pendiente (`[NE]`) |
| A2 | AnexoI / AnexoJ | IMPORTANTE | Pendiente (placeholder) |
| A4 | AnexoJ | IMPORTANTE | Pendiente (placeholder) |
| A6 | AnexoH | IMPORTANTE | Pendiente (placeholder) |
| M1 | Cap3 §3.3 | MENOR | **Resuelto** 2026-05-26 |
| M2 | AnexoF | MENOR | Pendiente (placeholder) |
| M3 | AnexoF | MENOR | Pendiente (placeholder) |

## Citas bibliográficas

La auditoría confirma que las 18 `\cite{}` del cuerpo `tfg_uib_70pv2/`
resuelven todas a un `\bibitem` existente. En `tfg_memoria_v3/` la
verificación se ha realizado tras cada compilación (0 referencias
rotas, 0 citas rotas en el último build). Mantener esta política tras
cada edición sustancial.

---

## Acción para defensa (sólo si se defiende `tfg_uib_70pv2/`)

1. Releer C1 y C2 antes de la defensa con respuesta preparada.
2. Mantener abiertos durante la defensa:
   - `RESULTADOS_TFG.md`
   - `output/ensemble_eval/ENSEMBLE_REPORT.md`
   - `tfg_figures/fairness_5models/summary_5models.md`
   - `tfg_uib_70pv2/Annexos.tex`
3. Si una publicación derivada (SpanDerm Pub~2): C1 y C2 deben
   resolverse explícitamente en el manuscrito, no relegarse a anexo.
