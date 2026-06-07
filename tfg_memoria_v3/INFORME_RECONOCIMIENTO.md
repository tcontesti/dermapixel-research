# Informe de reconocimiento — Fase 1 de la reescritura del TFG

**Sesión sin escritura de capítulos.** Este documento sintetiza el material
previo (cuatro memorias, documentación auxiliar e informes post-TFG) que
servirá de base a las fases siguientes (Fase 2 = Resumen + Cap. 1, etc.). El
informe sigue la estructura de diez secciones definida en
`PROMPT_FASE1_Reconocimiento.md`. Cada hallazgo se acompaña de la ruta del
fichero y, cuando aplica, de la línea aproximada.

> Castellano académico, sin opiniones del LLM. Cuando una afirmación es
> especulativa, se marca como tal.

---

## 1 · Inventario versionado de las cuatro memorias previas

| Ruta | Líneas `.tex` | Tamaño PDF | Fecha mod. (mtime) | Índice (resumen una línea por capítulo) | Estado |
|---|---:|---:|---|---|---|
| `tfg_uib/` | 3 633 | 4 675 825 B (≈ 154 p) | 2026-04-20 | Resumen + Introducción/Estado del arte + `Memoria.tex` monolítica (Materiales y métodos · LP · FT · Segmentación · Zero-shot · Interpretabilidad · LLMs · Clasificador unificado · Prototipo) + Conclusiones (Trabajo futuro por prioridad TFM/Tesis) + Bibliografía + Annexos. | Referencia (versión académica original). |
| `tfg_uib_75p/` | 4 063 | 4 810 931 B (≈ 75 p de cuerpo) | 2026-04-21 | Misma estructura que `tfg_uib` pero con `Memoria.tex` reducida a 1 046 líneas y `Annexos.tex` ampliado a 2 170 líneas (LP completo · Estrategias clasificador · Confusión melanoma/nevus · CBM SkinCon · SAE · ZS DermFM-Zero · Segmentación detallada · FT PanDerm Large · Mapping ontológico · Datasets detallados · M5/M6 prompt · Arquitectura DermApIxel · L3 47/43 perclase · Equidad Fitzpatrick). | Descartada (memoria `project_tfg_70pv2_state_2026_05_09.md` la marca como "intento previo fallido"). |
| `tfg_uib_70p/` | 978 | 1 954 084 B (≈ 70 p) | 2026-05-11 (PDF) / 2026-05-07 (tex) | Resumen + 8 capítulos narrativos: 1 Introducción · 2 El dominio de los datos · 3 La maquinaria · 4 La replicación · 5 Más allá de la replicación · 6 La revelación · 7 DermApIxel: el sistema funciona · 8 Conclusiones, líneas futuras y especulación honesta + Bibliografía + Annexos (Mapa de tareas experimentales). | Referencia narrativa congelada. |
| `tfg_uib_70pv2/` | 1 602 | 9 327 865 B (86 p PDF / 67 árabes) | 2026-05-13 | Misma estructura de 8 capítulos, todos ampliados; cambia el título de la portada a "DermApIxel: modelo fundacional para dermatología clínica"; añade `DeclaracionIA.tex`. | Activa al cierre de la etapa anterior. |

**Observaciones cruzadas:**

- El título de la portada cambia entre versiones:
  - `tfg_uib`, `tfg_uib_75p`, `tfg_uib_70p` → "Evaluación de modelos
    fundacionales para Dermatología Clínica" (`tfg_uib/MemoriaTFG.tex:44`,
    `tfg_uib_75p/MemoriaTFG.tex:44`, `tfg_uib_70p/MemoriaTFG.tex:32`).
  - `tfg_uib_70pv2` → "DermApIxel: modelo fundacional para dermatología
    clínica" (`tfg_uib_70pv2/MemoriaTFG.tex:34`). Este cambio entra en
    tensión directa con la regla 4 del prompt de reescritura
    (DermApIxel no debe ser protagonista del TFG).
- Tres de las cuatro versiones reutilizan los agradecimientos casi
  literalmente (variantes mínimas en el círculo personal, ver `tfg_uib_70pv2/MemoriaTFG.tex:53-99`).
- `tfg_uib_75p/Annexos.tex` desplaza al apéndice el grueso de las
  secciones técnicas que `tfg_uib/Memoria.tex` mantenía en el cuerpo;
  conviene tratarlo como repositorio de material reutilizable, no como
  documento independiente.

---

## 2 · Estructura comparada de los índices

Tabla cruzada con los capítulos equivalentes (entrada vacía = no existe en
esa versión). Se conserva la nomenclatura original de los títulos para
documentar el tono.

| Bloque temático | `tfg_uib` | `tfg_uib_75p` | `tfg_uib_70p` | `tfg_uib_70pv2` |
|---|---|---|---|---|
| Resumen + Abstract | ✓ (Resum.tex 1-26) | ✓ (idéntico al anterior) | ✓ (Resum.tex 1-33) | ✓ (Resum.tex 1-37) |
| Acrónimos | ✓ (203 líneas) | ✓ (203) | ✓ (54) | ✓ (53) |
| Introducción + Estado del arte | ✓ Cap. 1 con Motivación / Estructura / Estado del arte | ✓ Cap. 1 (idéntico al anterior) | ✓ Cap. 1 Dermapixel + lista de espera + fundacionales + pregunta + estructura | ✓ Cap. 1 (versión ampliada) |
| Datos / Datasets / Ontología | ✓ dentro de Memoria.tex § "Materiales y métodos" | ✓ idem | ✓ Cap. 2 "El dominio de los datos" (5 secciones) | ✓ Cap. 2 (8 secciones) |
| Hardware + protocolos | ✓ dentro de Memoria.tex § "Materiales y métodos" | ✓ idem | ✓ Cap. 3 "La maquinaria" | ✓ Cap. 3 "El Hardware" (renombrado) |
| LP / FT / Segmentación / Eficiencia etiquetas | ✓ Cap. de Memoria.tex 504-1077 | ✓ Memoria.tex 272-573 | ✓ Cap. 4 "La replicación" | ✓ Cap. 4 (ampliado, +4 árabes) |
| Zero-shot / SAE / RAG / LLMs / Equidad / Unificado | ✓ varios capítulos Memoria.tex 1079-2260 | ✓ idem | ✓ Cap. 5 "Más allá de la replicación" | ✓ Cap. 5 (ampliado, +2 árabes) |
| Resultados consolidados | (no aislado) | (no aislado) | ✓ Cap. 6 "La revelación" | ✓ Cap. 6 "Resultados consolidados y alcance de la replicación" (renombrado) |
| Prototipo DermApIxel | ✓ Memoria.tex 2261-2712 | ✓ Memoria.tex 920-1078 | ✓ Cap. 7 "DermApIxel: el sistema funciona" | ✓ Cap. 7 (ídem, con 8 placeholders gráficos) |
| Conclusiones + trabajo futuro | ✓ Conclusions.tex (Prioridad alta TFM / Prioridad media / Prioridad baja / Roadmap) | ✓ idem | ✓ Cap. 8 "Conclusiones, líneas futuras y especulación honesta" | ✓ Cap. 8 "Conclusiones y líneas futuras" |
| Bibliografía | ✓ 181 | ✓ 181 | ✓ 58 | ✓ 64 |
| Anexos | ✓ 72 (Tablas LP completas) | ✓ 2 170 (memoria operativa) | ✓ 44 (Mapa de tareas) | ✓ 105 (Mapa de tareas y estructura repo) |
| Declaración IA | — | — | — | ✓ `DeclaracionIA.tex` |

**Conclusión del análisis cruzado:** la propuesta de unión mínima que
preserva todo el contenido esencial coincide razonablemente con la
estructura objetivo del nuevo TFG (regla 10): introducción y antecedentes
+ estado del arte + datos y ontología + diseño experimental (hardware /
modelos / protocolos / métricas) + resultados con discusión integrada +
caminos abiertos + bibliografía y anexos.

Capítulos que aparecen en algunas versiones y deberán perder protagonismo
en la nueva memoria, conforme a las reglas de la reescritura:

- "Cap. 7 Prototipo DermApIxel" como capítulo dedicado: degradar a sección
  dentro del capítulo de caminos (regla 4 del prompt). Sus métricas
  operativas se conservan; la descripción extensa del producto pasa a
  anexo.
- "La revelación" como capítulo separado de resultados: integrar en el
  capítulo 5 (Resultados y discusión) tal como define la regla 13.
- Secciones de conclusión organizadas por "prioridad TFM/Tesis"
  (`tfg_uib/Conclusions.tex:43,67,91`): sustituir por la triple columna
  "iniciado y no concluido / identificado no abordado / integración con
  DermApIxel" del capítulo 6 objetivo (regla 14).

---

## 3 · Cifras consolidadas y validadas

Las cifras se cruzan con `RESULTADOS_TFG.md` (cifras experimentales
canónicas a 2026-03-28), `research_post_tfg/EDA_REPORT.md` (cifras canónicas
del dataset v3 a 2026-05-22) y
`research_post_tfg/reclassify_modality/POST_RECLASSIFICATION_REPORT.md`
(cifras del dataset tras paso a v3.1 el 2026-05-23). Cuando una cifra
aparece en distintas versiones del TFG, se cita la versión más reciente
con el resto consideradas concordantes salvo nota explícita.

### 3.1 · Cifras sólidas (respaldadas por log / script / commit / cita externa)

| Cifra | Valor | Fuente primaria |
|---|---|---|
| LP PanDerm Large media 10 datasets — Accuracy | 0,791 | `RESULTADOS_TFG.md` §FASE 1 línea ~40 |
| LP PanDerm Large media 10 datasets — AUROC | 0,901 | `RESULTADOS_TFG.md` §FASE 1 línea ~42 |
| LP PanDerm Large media 10 datasets — BAcc | 0,649 | `RESULTADOS_TFG.md` §FASE 1 línea ~41 |
| LP PanDerm Base media 10 datasets — AUROC | 0,865 | `RESULTADOS_TFG.md` §FASE 1 línea ~42 |
| FT PanDerm Large HAM10000 — Accuracy | 0,919 | `tfg_uib_70p/Cap6_Revelacion.tex:23`; `tfg_uib_70pv2/Cap6_Revelacion.tex:31` |
| FT PanDerm Large HAM10000 — BAcc | 0,813 | `tfg_uib_70p/Cap6_Revelacion.tex:23` |
| FT PanDerm Base HAM10000 + TTA — Accuracy | 0,920 | `RESULTADOS_TFG.md` §FASE 3 línea ~118 |
| FT PanDerm Base HAM10000 + TTA — BAcc | 0,852 | ibid. |
| FT HAM10000 — AUROC | 0,978 | ibid. |
| FT PAD-UFES Large — Accuracy | 0,800 | `tfg_uib_70p/Cap6_Revelacion.tex:24` |
| FT PAD-UFES — Top-3 | 0,970 | ibid. |
| FT DDI — degradación frente a LP | LP 0,847 → FT Base 0,774 (−7,3 pp) | `RESULTADOS_TFG.md` líneas 133-135 |
| Eficiencia etiquetas HAM 1 % — AUROC | 0,918 | `tfg_uib_70pv2/Cap4_Replicacion.tex:93`; `RESULTADOS_TFG.md` línea 72 |
| Eficiencia etiquetas HAM 1 % — Accuracy | 0,850 | `RESULTADOS_TFG.md` línea 72 |
| Eficiencia etiquetas PAD 1 % (14 imgs) — AUROC | 0,907 | `RESULTADOS_TFG.md` línea 82 |
| Segmentación SAM2.1-Large fine-tuned ISIC2018 — Dice | 0,947 | `tfg_uib_70pv2/Cap4_Replicacion.tex:132` |
| Segmentación SAM2.1 ISIC2018 — IoU | 0,903 | ibid. |
| Generalización SAM2.1 ISIC2017 — Dice | 0,945 | `tfg_uib_70pv2/Cap4_Replicacion.tex:134` |
| Generalización SAM2.1 PH2 — Dice | 0,960 | ibid. |
| Segmentación CAE-seg propia 50 ep ISIC2018 — Test Dice | 0,894 | `RESULTADOS_TFG.md` línea 200 |
| Zero-shot DermLIP HAM (GPT-2/CLIP + prompts Derm1M) — AUROC | 0,740 (acc 0,427) | `RESULTADOS_TFG.md` línea 238 |
| Zero-shot DermLIP HAM (GPT-2/CLIP + prompts enriquecidos) — AUROC | 0,854 | `tfg_uib_70pv2/Cap5_Derivadas.tex:17,38` |
| Zero-shot DermLIP HAM (PubMedBERT, prompts genéricos) — AUROC | 0,366 | `RESULTADOS_TFG.md` línea 223 |
| GPT-4o ZS HAM — Accuracy | 0,485 | `tfg_uib_70pv2/Cap5_Derivadas.tex:159` |
| MedGemma 27B ZS HAM — Accuracy | 0,665 | ibid. |
| MedGemma 27B + LoRA HAM — Accuracy | 0,802 | ibid. |
| PanDerm vs GPT-4o | +43,4 pp accuracy en HAM | `tfg_uib_70pv2/Cap6_Revelacion.tex:55-56`; `RESULTADOS_TFG.md` línea 11 (resumen) |
| PanDerm vs MedGemma 27B | +25,4 pp ZS / +11,7 pp LoRA | `tfg_uib_70pv2/Cap6_Revelacion.tex:58-59` |
| Clasificador unificado L1 — Accuracy | 94,7 % | `tfg_uib_70pv2/Cap6_Revelacion.tex:61`; `MEMORY.md` línea sobre `project_training_unified` |
| Clasificador unificado L2 — Accuracy | 81,9 % (26 clases efectivas) | `tfg_uib_70pv2/Cap6_Revelacion.tex:64`; `tfg_uib_70pv2/Cap5_Derivadas.tex:232` |
| Clasificador unificado L3 merged43 + TTA — Accuracy | 81,0 % | `tfg_uib_70pv2/Cap6_Revelacion.tex:67` |
| Clasificador L3 merged43 + TTA — BAcc | 81,82 % | `tfg_uib_70p/Cap6_Revelacion.tex:35`; memoria `project_training_unified.md` |
| Clasificador L3 merged43 + TTA — Top-3 | 95,4 % | `tfg_uib_70pv2/Cap6_Revelacion.tex:67` |
| Ganancia BAcc por merged43+TTA frente a baseline | +4,72 pp | `tfg_uib_70p/Cap6_Revelacion.tex:35` |
| Ensemble safety melanoma (M1+M7+SigLIP LP) — Recall | 100 % (70/70) | `tfg_uib_70pv2/Cap5_Derivadas.tex:236`; `tfg_uib_70p/Cap6_Revelacion.tex:36` |
| Ensemble safety melanoma — AUROC | 0,991 | `tfg_uib_70p/Cap6_Revelacion.tex:36` |
| Equidad Fitzpatrick17k — N imágenes | 16 577 | `tfg_uib_70pv2/Cap5_Derivadas.tex:193`; `tfg_uib/Resum.tex:7` |
| Equidad PanDerm Large — AUROC global | 0,912 | `tfg_uib_70p/Cap6_Revelacion.tex:37` |
| Equidad PanDerm Large — AUROC fototipo VI | 0,830 | ibid. |
| Equidad PanDerm Large — gap | 8,9 pp | ibid. |
| BiomedCLIP — AUROC global Fitzpatrick17k | 0,856 | `tfg_uib_70p/Cap6_Revelacion.tex:38` |
| Sparse Autoencoder — dimensión proyectada | 1 024 → 16 384 (ratio 16:1) | `tfg_uib_70pv2/Cap5_Derivadas.tex:55` |
| SAE ratio de sparsity tras 100 épocas | ≈ 15 % | `tfg_uib_70pv2/Cap5_Derivadas.tex:57` |
| SkinCon CBM — conceptos con AUROC > 0,80 sobre 35 evaluables | 13 | `tfg_uib_70pv2/Cap5_Derivadas.tex:67` |
| CBM SkinCon — AUROC media frente a LP | 0,920 vs 0,909 (22 conceptos) | `tfg_uib_70pv2/Cap5_Derivadas.tex:117` |
| Conceptos clínicos definidos por la Dra. Taberner | 34 (16 dermatoscópicos + 8 distribución + 10 forma/color/textura) | `tfg_uib_70pv2/Cap5_Derivadas.tex:84-90` |
| RAG visual Derm1M — N imágenes índice FAISS | 421 327 | `tfg_uib_75p/Memoria.tex:744`; "421\,K" en `tfg_uib/Resum.tex:7` |
| RAG visual — latencia por consulta | ≈ 150 ms | `tfg_uib_70pv2/Cap5_Derivadas.tex:124` |
| Mapeo ontológico — nombres de clase originales | 244 | `tfg_uib_70pv2/Cap2_Datos.tex:103`; `tfg_uib_70pv2/Cap5_Derivadas.tex:226` |
| Mapeo ontológico — N total armonizado | 72 654 imágenes | ibid. |
| Datasets evaluados (LP) | 10 (HAM10000, BCN20000, PAD-UFES, DDI, Derm7pt clínico, Derm7pt dermo, Dermnet, HIBA, MSKCC, WSI) | `RESULTADOS_TFG.md` líneas 17-36 |
| Datasets armonizados a ontología | 11 | `tfg_uib_70pv2/Cap2_Datos.tex:103` |
| Datasets totales presentados | 12 (con Fitzpatrick17k, SkinCon, ISIC2018) | `tfg_uib_70pv2/Cap2_Datos.tex:107-131` |
| Derm1M — N pares imagen-texto | 1 029 761 | `tfg_uib_70pv2/Cap2_Datos.tex:71` |
| Derm1M — N imágenes únicas | 403 563 | ibid. |

### 3.2 · Cifras frágiles (contradicciones o sin trazabilidad clara entre versiones)

| Asunto | Valor en versión previa | Valor más reciente / canónico | Origen del conflicto |
|---|---|---|---|
| DermapixelAI — total imágenes | 1 109 (`tfg_uib_70pv2/Resum.tex:11`; `tfg_uib_70pv2/Cap2_Datos.tex:90`); 1 109 también en `tfg_uib/Resum.tex` (que cita "1.888 imágenes según modalidad" como manipulación distinta de la Dra. Taberner, `tfg_uib/Memoria.tex:347-373`) | 1 089 en v3.1 (`research_post_tfg/reclassify_modality/POST_RECLASSIFICATION_REPORT.md:19`) | TFG cita v3 (1 109); investigación post-TFG opera sobre v3.1 (1 089). El TFG entregado no se corrige (`project_dermapixel_v3_1.md` "El TFG entregado no se ve afectado"). |
| DermapixelAI — N dermatoscopias | 9 (`tfg_uib_70pv2/Cap2_Datos.tex:130`) | 49 (`reclassify_modality/POST_RECLASSIFICATION_REPORT.md:19`) | Reclasificación de modalidad 2026-05-23: 40 imágenes movidas de `clinical` a `dermoscopy`. |
| DermapixelAI — casos | 672 con imagen, 698 totales (`tfg_uib_70pv2/Resum.tex:11`) | 672 / 698 (idéntico) tras v3.1, con 3 casos huérfanos sin imagen | Cifra coincidente en TFG y v3.1; añadir nota sobre 3 huérfanos generados al excluir las 20 not-derm. |
| L2 subcategorías de la ontología | 43 (Resum y Cap. 2 de `tfg_uib_70pv2`), 26 efectivas en clasificador unificado (Cap. 5 línea 232) | 38 efectivas en el corpus v3 (`EDA_REPORT.md:48-49`; bandera amarilla por dos variantes ortográficas de "Trastornos queratinización") | Tres acepciones distintas: 43 teóricas en vocabulario, 39 raw en corpus, 38 efectivas tras normalizar, 26 entrenadas por umbral ≥100 imgs. Las cuatro deben distinguirse en la nueva memoria. |
| L3 diagnósticos de la ontología | 367 teóricos (`tfg_uib/Resum.tex:7`; `tfg_uib_70pv2/Resum.tex:11`); 47 en clasificador unificado fusionados a 43 (`tfg_uib_70pv2/Cap5_Derivadas.tex:228`) | 251 efectivos en corpus v3 (cobertura 68,4 %), 250 en v3.1 (`EDA_REPORT.md:50`; `research_post_tfg/sampling/SAMPLING_REPORT.md:144`) | Misma distinción que en L2: 367 teóricos, 251 efectivos, 47/43 entrenables, 38 efectivas en L2. La memoria nueva debe declarar la cifra que cita y bajo qué definición. |
| Validación de la Dra. Taberner sobre el corpus | "97,9 %" en `tfg_uib_70pv2/Cap2_Datos.tex:92` (interpretado como `label_source = ontology`); 23 % corrigió diagnósticos automáticos; 1 888 imágenes clasificadas por modalidad (`tfg_uib/Memoria.tex:373`) | `EDA_REPORT.md:22` separa explícitamente tres métricas distintas: `label_source = ontology` 97,93 %, `diagnosis_source = expert_v3` 98,38 %, `rosa_verified = True` 82,96 %. Las tres no se deben confundir; la cifra del TFG debe declararse como "label_source = ontology" y nunca como "rosa_verified". | Hay riesgo claro de mezclar las dos cifras (97,9 % vs 83 %) en publicaciones derivadas. |
| Datasets evaluados en LP | "diez datasets" (`RESULTADOS_TFG.md` y `tfg_uib_70pv2/Cap4_Replicacion.tex:16`) | "doce" en la tabla resumen del Cap. 2 (`tfg_uib_70pv2/Cap2_Datos.tex:107-131`) y "once" en el mapeo ontológico | Las cifras son coherentes (10 evaluados LP + Fitzpatrick17k + SkinCon + ISIC2018 según uso), pero conviene fijar y declarar el conteo único en la nueva memoria. |
| Datos de entrenamiento PanDerm | "2 millones" (`tfg_uib/Resum.tex:7`), "2,1 millones" (`tfg_uib_70pv2/Cap4_Replicacion.tex:26`; `Introduccio.tex:33`) | 2,1 M es la cifra del paper Yan et al. 2025 | Pequeña inconsistencia entre redondeo y cifra exacta. |
| BAcc Fitzpatrick17k PanDerm Large | "AUROC 0,912 global / 0,830 VI / gap 8,9 pp" (Cap. 6 de `tfg_uib_70p`) | Coincide con `MEMORY.md` `project_fairness_5models` pero no se detalla cifra por fototipo en `RESULTADOS_TFG.md`; trazabilidad concentrada en `tfg_figures/fairness_5models/summary_5models.md` (no leída en esta sesión) y en `results/FITZPATRICK_FULL_RESULTS.md` | Las cifras agregadas son robustas; el desglose por fototipo no figura en el documento de resultados consolidado y depende de un fichero auxiliar. |
| Accuracy del clasificador HAM (Resum 75p) | "Acc 81,0 %, Top-3 95,4 %" se refiere al unificado L3 (`tfg_uib/Resum.tex:7`) | Confirmado por `tfg_uib_70pv2/Cap6_Revelacion.tex:67`. Sin contradicción, pero la versión 75p añade "20 tareas experimentales reproducibles" frente a `tfg_uib_70pv2/Annexos.tex` que cita 20 idem; `project_estado_final.md:10` declara 24. | Cifra de "20 tareas" vs "24 experimentos completados" requiere unificación. |

### 3.3 · Cifras descartadas (sustituidas por valor canónico actual)

| Cifra superada | Sustituida por | Razón |
|---|---|---|
| DermapixelAI v3 = 1 109 imágenes con 9 dermatoscopias | DermapixelAI v3.1 = 1 089 imágenes con 49 dermatoscopias | Reclasificación de modalidad 2026-05-23; 40 imágenes movidas a dermoscopy, 20 excluidas a `_excluded/`. Documentado en `POST_RECLASSIFICATION_REPORT.md`. |
| Solar lentigo → Melasma sin corregir (572 imágenes) | Mapeo corregido en v3.1 | `MEMORY.md` línea `project_audit_ontology_rosa`. |
| 32 conceptos SkinCon propuestos por la Dra. Taberner | 34 conceptos clínicos definitivos | Evolución natural de la lista; documentada en `MEMORY.md` `project_sae_concepts` y `tfg_uib_70pv2/Cap5_Derivadas.tex:84-90`. |
| Memoria del prototipo "9 módulos" en versiones tempranas | 8 módulos en `tfg_uib_70pv2` (M1, M2, M3, M4, M5, M6, M7, M8) | El TFG declara 8; las memorias internas hablan de 8 al menos desde 2026-04-12 (`MEMORY.md` `project_dermapixel_production_status`). |
| Resúmenes de `tfg_uib/Resum.tex` y `tfg_uib_75p/Resum.tex` (idénticos) | Resumen narrativo de `tfg_uib_70pv2/Resum.tex` y, por la nueva memoria, un texto académico aséptico de ≈ 250-300 palabras | Las dos primeras versiones formulan pregunta de investigación entre interrogación ("¿cuál es el estado del arte ...?", `tfg_uib_75p/Resum.tex:5`). |
| Carpeta `images/microscopy/` referenciada en el dataset | Carpeta vacía, vestigio estructural | `EDA_REPORT.md:35`. Si se publica el dataset, eliminar. |

---

## 4 · Catálogo de afirmaciones no validadas en versiones previas

Listado de claims que aparecen en el material previo y que **no están
respaldados** por cifra propia, log o cita externa publicada con el rigor
que la regla 3 de la reescritura exige. Se eliminan o reescriben con
matiz en la versión nueva.

| # | Afirmación literal | Ubicación | Por qué se considera no validada |
|---|---|---|---|
| 1 | "Los modelos más equitativos respecto al fototipo lo son, en parte, porque rinden uniformemente peor" (la "paradoja BiomedCLIP") | `tfg_uib_70pv2/Resum.tex:11`; `tfg_uib_70pv2/Cap5_Derivadas.tex:200` | El hallazgo cuantitativo (gap bajo + AUROC bajo) sí está respaldado; la interpretación causal "uniformemente peor" se ofrece como conclusión sin contraste estadístico explícito (p-valor, IC) sobre la diferencia entre subgrupos. Reformular como descripción de los datos, no como atributo causal del modelo. |
| 2 | "establece un nuevo SOTA en segmentación" | `tfg_uib/Resum.tex:7`; `tfg_uib_70pv2/Cap4_Replicacion.tex:132` | La comparación se hace solo contra PanDerm (Dice 0,910 / 0,921) y MedSAM (0,876) sobre ISIC2018; no se contrasta contra trabajos publicados 2025-2026 que pudieran reportar Dice superiores. La afirmación queda como "supera a las dos referencias contrastadas en este trabajo", no SOTA absoluto. |
| 3 | "DermFM-Zero... opens the main continuation line" / "La convergencia es de enfoque, no de coincidencia temporal" | `tfg_uib_70pv2/Resum.tex:32`; `tfg_uib_70p/Resum.tex:11` | Comparación cualitativa con un modelo cuyos pesos no son públicos; la "convergencia" es interpretación del autor sin contraste empírico. Conservar como hipótesis declarada en el cap. 6, no como hallazgo. |
| 4 | "El sistema agéntico podría reducir el gap sobre piel oscura y mejorar la sensibilidad de melanoma" (con cifras "+5/+10 pp" en versiones intermedias) | `tfg_uib_70pv2/Cap8_Conclusiones.tex:18` (cualitativo); cifras "+5/+10 pp" en memorias intermedias (`MEMORY.md` `project_tfg_70pv2_state_2026_05_09`) | Conjetura sin medición. Aceptable si se declara como hipótesis abierta sin cuantificación. |
| 5 | "PanDerm Large supera a GPT-4o por cuarenta y tres coma cuatro puntos porcentuales" en los Resum | `tfg_uib_70pv2/Resum.tex:11`; `tfg_uib_70p/Resum.tex:9` | La cifra está medida (FT 0,919 vs ZS 0,485), pero presentarla como "supera" induce un marco competitivo que contradice la regla 5 (no se compite con PanDerm ni se enmarca el TFG como competición). Reescribir descriptivamente: "FT especializado entrega 0,919 acc en HAM10000; el LLM generalista zero-shot alcanza 0,485 sobre el mismo split". |
| 6 | "Se demuestra que PanDerm Large... supera al paper original" | `tfg_uib/Resum.tex:7`; `tfg_uib_75p/Resum.tex:7` | El paper original reporta ≈ 0,912 en HAM y el TFG reproduce 0,919. La diferencia entra dentro de la incertidumbre de protocolo (TTA distinto, augmentaciones distintas). "Supera" debería sustituirse por "iguala o se sitúa marginalmente por encima dentro del margen del protocolo". |
| 7 | "PanDerm Large no presenta sesgo racial severo" | Múltiples (`tfg_uib/Resum.tex:7`; `tfg_uib_70pv2/Cap5_Derivadas.tex:198`) | El gap de 8,9 pp entre fototipos I-V y VI no es despreciable; describirlo como "no severo" requiere comparación con un umbral clínico aceptado. Reformular como "reducción del gap respecto a la literatura 2020-2022 (10-30 pp), con gap residual de 8,9 pp en fototipo VI". |
| 8 | "Un noventa y siete coma nueve por ciento de cobertura de validación experta" (Cap. 2) interpretado como validación de la Dra. Taberner sobre el material | `tfg_uib_70pv2/Cap2_Datos.tex:92`; `tfg_uib_70p/Cap2_Datos.tex:63` (similar) | La cifra 97,93 % corresponde a `label_source = ontology` según `EDA_REPORT.md:22`. El campo `rosa_verified = True` aplica al 82,96 %. Citar la cifra correcta y la definición del campo. |
| 9 | "1 888 imágenes clasificadas manualmente según modalidad" por la Dra. Taberner | `tfg_uib/Memoria.tex:373` | Cifra que no aparece en el corpus actual (1 089 imágenes en v3.1); puede referirse a un conteo intermedio de iteraciones de revisión sumadas. No reproducible en esta sesión; clasificar como cifra histórica no canónica. |
| 10 | "Errores no correlacionados entre modelos. Intersección de fallos vacía" (ensemble safety melanoma) | `tfg_uib_70pv2/Cap5_Derivadas.tex:236`; `tfg_uib_70p/Cap6_Revelacion.tex:36` | El claim sobre 70 imágenes positivas del split de test HAM es real, pero "no correlacionados" es una caracterización que requiere una prueba estadística sobre la complementariedad (p. ej., chi-cuadrado de tabla de errores). No se cita la prueba; reformular como observación empírica acotada a las 70 muestras. |
| 11 | "Pedunculado 0,929, friable 0,913, exofítico 0,908" como evidencia de monosemanticidad SAE | `tfg_uib_70pv2/Cap5_Derivadas.tex:67` | Las cifras AUROC son sólidas; la interpretación monosemántica es la hipótesis de Anthropic (Templeton et al. 2024) trasladada al dominio dermatológico. Debe reformularse como "tres features del SAE alcanzan AUROC > 0,90 frente a su correlato textual SkinCon", sin afirmar monosemanticidad sin más prueba. |
| 12 | "El curso de la Dra. Taberner... reorientó cómo había que aplicar la replicación" como motor central del giro narrativo del TFG (Resum 70p y 70pv2) | `tfg_uib_70pv2/Resum.tex:13`; `tfg_uib_70p/Resum.tex:11` | El hecho del curso es real (memoria `project_tfg_70p_session.md`); la reorientación del trabajo es interpretación narrativa. La regla 7 del prompt evita esta narrativización: separar el hecho (curso, materiales, 34 conceptos) del juicio (reorientación del enfoque). |
| 13 | "Sin sesgo sistemático aarch64" como hallazgo del trabajo | `tfg_uib_70p/Cap6_Revelacion.tex:21,46`; `tfg_uib_70pv2/Cap6_Revelacion.tex:88` | La conclusión está respaldada por la diferencia ≤ 0,9 pp respecto al paper; pero el experimento no replica x86 sobre el mismo equipo (solo aarch64), por lo que la ausencia de sesgo se infiere por comparación con cifras publicadas. Acotar como "concordancia con cifras publicadas, sin comparación pareada x86 vs aarch64". |
| 14 | "Validación operativa" del prototipo "sobre casuística clínica real" | `tfg_uib_70pv2/Cap7_Prototipo.tex:123`; `tfg_uib_70pv2/Resum.tex:9` | El prototipo se ha usado en sesiones con la Dra. Taberner pero no hay validación prospectiva con métrica (la validación clínica formal está en `Cap8_Conclusiones.tex:48` como línea futura). Reformular como "uso supervisado por dermatóloga sobre casos del blog Dermapixel" hasta que se realice el estudio prospectivo. |
| 15 | "Concordancia con el grupo de Monash" presentada como colaboración formal | `tfg_uib_70pv2/Cap2_Datos.tex:94`; `tfg_uib_70pv2/Cap8_Conclusiones.tex:41` | El contacto es real (memoria del 2026-05-09 lo confirma) pero no hay acuerdo formal firmado a 2026-05-23. La fórmula correcta es "contacto establecido, interés por escrito en explorar colaboración, sin acuerdo formalizado a la fecha de cierre del TFG". |

---

## 5 · Glosario de tono inapropiado (calibración negativa)

### 5.1 · Títulos en forma de pregunta

| Ubicación | Cita | Comentario |
|---|---|---|
| `tfg_uib/Resum.tex:5` | "\textit{¿cuál es el estado del arte en inteligencia artificial aplicada a dermatología, qué modelos fundacionales existen, cuál funciona mejor, en qué condiciones, y qué bases de código son lo suficientemente robustas para construir sobre ellas?}" | Pregunta retórica en el resumen. Eliminar en el resumen nuevo (regla 2). |
| `tfg_uib_75p/Resum.tex:5` | idéntica | ibid. |

> En el cuerpo de las cuatro versiones no se han encontrado cabeceras de
> sección redactadas como pregunta literal (rastreado con `\section{?` y
> `\section{¿` por grep). La pregunta retórica está esencialmente en los
> resúmenes y en algún cuerpo de párrafo introductorio (regla recordada
> en `MEMORY.md` `project_tfg_70pv2_state_2026_05_09`).

### 5.2 · Títulos narrativos / juicios de valor / hipérboles

| Ubicación | Cita | Comentario |
|---|---|---|
| `tfg_uib_70p/Cap6_Revelacion.tex:1`; `tfg_uib_70pv2/Cap6_Revelacion.tex:1` ("Resultados consolidados y alcance de la replicación") | "La revelación" (70p) | El título narrativo desaparece ya en 70pv2 (renombrado a "Resultados consolidados..."); en la versión nueva se evita por completo el sustantivo "revelación". |
| `tfg_uib_70p/Cap6_Revelacion.tex:43` | "\section{La afirmación dura}" | Título declarativo pero con valoración. Sustituir por "Lectura agregada de los resultados de replicación". |
| `tfg_uib_70p/Cap6_Revelacion.tex:52` | "\section{El matiz duro}" | ibid. Sustituir por "Limitaciones y alcance de la conclusión anterior". |
| `tfg_uib_70p/Cap4_Replicacion.tex:1` | "\chapter{La replicación}" | Título con artículo determinado y sustantivo abstracto. La regla 7 sugiere sustituir "replicación" por "experimentación / evaluación empírica" y dar al capítulo un título declarativo del contenido (p. ej., "Evaluación de PanDerm Large sobre datasets públicos"). |
| `tfg_uib_70p/Cap5_Derivadas.tex:1`; `tfg_uib_70pv2/Cap5_Derivadas.tex:1` | "\chapter{Más allá de la replicación}" | Lenguaje narrativo. Sustituir por título declarativo: "Resultados complementarios y derivadas del estudio". |
| `tfg_uib_70p/Cap3_Maquinaria.tex:1` | "\chapter{La maquinaria}" | Estilo coloquial; ya renombrado a "El Hardware" en 70pv2 (mejor pero todavía con artículo determinado). Sustituir por "Hardware, modelos y protocolos experimentales". |
| `tfg_uib_70pv2/Cap7_Prototipo.tex:1`; `tfg_uib_70p/Cap7_Prototipo.tex:1` | "\chapter{DermApIxel: el sistema funciona}" | Hipérbole en el título (regla 4 y regla 1). Eliminar el "el sistema funciona"; si se conserva el capítulo, titular "Despliegue de DermApIxel: integración del modelo en el entorno operativo". |
| `tfg_uib_70p/Cap8_Conclusiones.tex:1` | "\chapter{Conclusiones, líneas futuras y especulación honesta}" | "Especulación honesta" es figura retórica. Suprimir. |
| `tfg_uib_70pv2/Cap4_Replicacion.tex:22` | "\subsection*{La lectura inmediata: empate técnico con un matiz inquietante}" | Tono ensayístico. Sustituir por "Lectura agregada del ranking de modelos". |
| `tfg_uib_70pv2/Cap4_Replicacion.tex:42` | "\subsection*{La lectura por subconjunto: dónde se separan los modelos}" | ibid. Sustituir por "Análisis por dataset". |
| `tfg_uib_70pv2/Cap4_Replicacion.tex:69,73` | "Lo esperable: fine-tuning supera al paper..." / "Lo inesperado: fine-tuning degrada en datasets pequeños" | Categorías de "esperable/inesperado" son interpretativas. Reformular como "Datasets de tamaño moderado (HAM10000, PAD-UFES)" / "Régimen de datos escasos (DDI)". |
| `tfg_uib_70pv2/Cap4_Replicacion.tex:123` | "\section{La grieta: segmentación}" | Metáfora. Sustituir por "Segmentación binaria de lesión: configuración y resultados". |
| `tfg_uib_70pv2/Cap5_Derivadas.tex:6` | "\section{Zero-shot multimodal y la sensibilidad al prompt}" | Aceptable, declarativo. Conservar. |
| `tfg_uib_70pv2/Cap5_Derivadas.tex:80` | "\subsection*{La aportación: 34 conceptos clínicos de la Dra. Taberner}" | "La aportación" introduce juicio de valor. Sustituir por "Conceptos clínicos definidos por revisión experta". |
| `tfg_uib_70pv2/Cap2_Datos.tex:87` | "\section{La aportación: DermapixelAI v3}" | ibid. Sustituir por "DermapixelAI v3: corpus propio del proyecto". |
| `tfg_uib_70pv2/Cap5_Derivadas.tex:146` | "\section{Modelos de lenguaje generales frente a PanDerm}" | "Frente a" induce marco competitivo. Sustituir por "Evaluación comparativa con modelos de lenguaje generalistas". |
| `tfg_uib_70pv2/Cap5_Derivadas.tex:190` | "\section{Equidad: Fitzpatrick17k y la paradoja BiomedCLIP}" | "Paradoja" es interpretativo. Sustituir por "Análisis de equidad por fototipo en Fitzpatrick17k". |
| `tfg_uib_70pv2/Cap5_Derivadas.tex:249` | "\section{Hacia el sistema integrado}" | Tono prospectivo en lugar de descriptivo. Sustituir por "Integración de módulos en el prototipo DermApIxel" o eliminar (la sección puede absorberse en el capítulo 6 nuevo). |
| `tfg_uib_70pv2/Cap8_Conclusiones.tex:21` | "\section{Las tres publicaciones latentes}" | "Latentes" es proyectivo y figurado. Sustituir por "Líneas de publicación derivadas del trabajo". |

### 5.3 · Primera persona excesiva / tono de profesor

| Ubicación | Cita | Comentario |
|---|---|---|
| `tfg_uib_70pv2/Introduccio.tex:4` | "El proyecto empieza fuera de la universidad. Empieza en Dermapixel..." | Apertura novelada. Sustituir por "El presente trabajo se enmarca en la línea de investigación derivada del archivo clínico Dermapixel, mantenido por la Dra. Rosa Taberner...". |
| `tfg_uib_70pv2/Cap2_Datos.tex:4` | "Antes de hablar de modelos conviene hablar de los datos sobre los que esos modelos se entrenan, se evalúan y, en última instancia, fracasan o tienen éxito. Cada dataset utilizado en este trabajo tiene una historia..." | Tono novelado, palabras valorativas ("fracasan o tienen éxito"). Reescribir aséptico: "Este capítulo presenta los datasets utilizados, agrupados por modalidad, así como la ontología jerárquica que articula los experimentos posteriores". |
| `tfg_uib_70pv2/Cap2_Datos.tex:34` | "Si la dermoscopia es el terreno cómodo, la fotografía clínica es donde se impone la realidad hospitalaria" | Metáfora. Sustituir por descripción neutral de las diferencias entre modalidades. |
| `tfg_uib_70p/Cap6_Revelacion.tex:4` | "Hasta este capítulo el documento ha mantenido en suspenso las cifras agregadas. La narrativa avanzaba enunciando dirección, mecanismo y consecuencia clínica de cada hallazgo, pero reservando la magnitud exacta para no romper el hilo. En este capítulo se desvela." | Narrativización autorreferencial. Eliminar; sustituir por "Este capítulo presenta las métricas consolidadas de los experimentos de los capítulos 4 y 5." |
| `tfg_uib_70pv2/Cap4_Replicacion.tex:7` | "el lector acompaña paso a paso el proceso experimental..." | Apelación al lector. Suprimir. |
| `tfg_uib_70pv2/Cap5_Derivadas.tex:4` | "Hasta aquí el trabajo ha respondido a la pregunta principal de la replicación. Pero a lo largo del recorrido han aparecido seis hilos secundarios que merecen capítulo propio." | "Han aparecido" / "merecen capítulo" introducen valoración. Reescribir: "El presente capítulo recoge los resultados experimentales complementarios al núcleo de la replicación, distribuidos en seis bloques temáticos". |
| `tfg_uib_70pv2/Cap5_Derivadas.tex:11` | "Una intuición inicial podría ser que el rendimiento depende principalmente del encoder visual... Sin embargo, los experimentos de este trabajo muestran que esta intuición es incorrecta." | Estructura "intuición → realidad". Reformular como observación experimental directa. |
| `tfg_uib_70pv2/Cap6_Revelacion.tex:88` | "el sesgo aarch64 frente al hardware x86 dominante en la literatura es despreciable." | "Despreciable" requiere umbral. Sustituir por "queda por debajo de 1 pp en los 10 datasets evaluados". |

### 5.4 · Hipérboles, juicios de valor, comparativas no objetivas

| Ubicación | Cita | Comentario |
|---|---|---|
| `tfg_uib_70p/Cap6_Revelacion.tex:38` | "Equidad por mediocridad: bajos en todos por igual no es éxito clínico." | Sentencia editorial. Reescribir descriptivamente. |
| `tfg_uib_70pv2/Cap5_Derivadas.tex:118-119` | "Este resultado es especialmente importante desde el punto de vista clínico: demuestra que es posible sustituir una representación densa no interpretable por una basada en conceptos clínicos sin perder capacidad predictiva." | "Especialmente importante" y "demuestra" son valoraciones. Suprimir adjetivos; conservar el dato. |
| `tfg_uib_70pv2/Cap5_Derivadas.tex:161` | "La conclusión cuantitativa es clara: el aumento de escala en número de parámetros (27B frente a 307M) no compensa la ausencia de pretraining específico en el dominio dermatológico." | "Clara" + "no compensa" son juicios. Sustituir: "PanDerm Large alcanza 0,919 acc; MedGemma 27B + LoRA alcanza 0,802 acc sobre el mismo split; la diferencia es 11,7 pp". |
| `tfg_uib_70pv2/Cap6_Revelacion.tex:94` | "...permite obtener un rendimiento competitivo sin necesidad de un modelo único que resuelva todas las tareas." | "Competitivo" sin referente. Reformular con cifras. |
| `tfg_uib_70pv2/Cap5_Derivadas.tex:188` | "la especialización en el dominio es el factor determinante en tareas de clasificación dermatológica" | Generalización fuera del marco experimental. Acotar al benchmark HAM10000 y a los modelos contrastados. |
| `tfg_uib_70pv2/Cap8_Conclusiones.tex:11` | "Los siguientes resultados son robustos dentro del marco metodológico empleado..." | Aceptable, pero la siguiente lista mezcla cifras absolutas con interpretaciones cualitativas. Restringir esta lista a cifras directamente medidas. |
| `tfg_uib_70pv2/Cap5_Derivadas.tex:142` | "más alineada con la percepción del usuario" | Juicio sin medición de usabilidad. Reformular. |

### 5.5 · Información especulativa presentada como certeza

| Ubicación | Cita | Comentario |
|---|---|---|
| `tfg_uib_70pv2/Cap5_Derivadas.tex:130` | "el atractor semántico del granuloma piogénico... lesiones de Rosa convergen hacia una misma región del espacio" | Hipótesis explicativa presentada como observación. Acotar a "se observa convergencia para 3 / 5 consultas piloto" si esa es la base, o degradarlo a "observación cualitativa". |
| `tfg_uib_70pv2/Cap8_Conclusiones.tex:18` | "El TFG conjetura, sin cifra numérica asociada, que un sistema agéntico..." | Bien declarado como conjetura. Conservar el matiz. |
| `tfg_uib_70pv2/Cap2_Datos.tex:94` | "el grupo de la Universidad Monash autor de PanDerm... ha confirmado por escrito interés en colaborar sobre DermapixelAI v3..." | Verificable solo si existe correo o mensaje. Si no se incluye fuente, degradar a "se mantiene contacto con el grupo". |

---

## 6 · Material reutilizable

Bloques cuyo tono es razonablemente académico y que pueden servir de base
para la nueva memoria (sin copia literal: regla operativa 5).

| Ruta + líneas | Tema | Por qué reutilizable |
|---|---|---|
| `tfg_uib_70pv2/Cap3_Maquinaria.tex:6-15` | Descripción del hardware DGX Spark, memoria unificada, aarch64 | Tono descriptivo, cifras concretas (128 GB, BF16, 50 GB cargados en GPU). Base directa para el capítulo 4 nuevo. |
| `tfg_uib_70pv2/Cap3_Maquinaria.tex:39-77` | Descripción de los cinco protocolos experimentales (LP, FT, segmentación, ZS, LLMs) | Descripción técnica y explícita de cada protocolo. Reutilizable con ajustes terminológicos. |
| `tfg_uib_70pv2/Cap3_Maquinaria.tex:82-102` | Definiciones de métricas (AUROC, BAcc, F1 ponderada, Dice/IoU, recall@k) | Cumple el rol del nuevo capítulo 4 §"métricas". Tono académico. |
| `tfg_uib_70pv2/Cap2_Datos.tex:96-105` | Descripción de la ontología jerárquica L1/L2/L3 con SNOMED-CT y CIE-10 | Tono más académico que el resto del capítulo. Base directa para la sección de ontología del nuevo capítulo 3. |
| `tfg_uib_75p/Memoria.tex:32-271` | Sección Datasets + Modelos evaluados + Protocolos del 75p | Aunque la versión 70pv2 mejora el tono, el 75p mantiene secciones por dataset que pueden servir de plantilla descriptiva (con los datos numéricos actualizados a v3.1 donde aplique). |
| `tfg_uib_75p/Annexos.tex:1248-1357` | Descripción detallada de cada dataset por familia (dermoscopia, clínica, histo, segmentación, vision-lenguaje) | Material denso y útil para una tabla de datasets en el cap. 3 nuevo. |
| `tfg_uib/Memoria.tex:339-388` | Pipeline de construcción de DermapixelAI v3 | Trazabilidad metodológica que falta en versiones cortas. |
| `tfg_uib_70p/Cap6_Revelacion.tex:11-41` (tabla `tab:revelacion`) | Tabla consolidada de resultados por bloque experimental | Estructura de tabla útil; los textos de "comentario" deben reescribirse en clave académica. Equivalente en `tfg_uib_70pv2/Cap6_Revelacion.tex:18-81`. |
| `tfg_uib_70pv2/Cap4_Replicacion.tex:104-121` | Validación cruzada sobre el downstream set de Derm1M | Descripción de tareas downstream con tono académico. Reutilizable. |
| `tfg_uib_75p/Memoria.tex:392-432` (sección Fitzpatrick17k LP) | Cifras detalladas de equidad por fototipo | Material denso para el capítulo de resultados, evita reescribir desde cero la sección de equidad. |
| `tfg_uib_70pv2/DeclaracionIA.tex:1-63` | Declaración sobre el uso de IA | Reutilizable tal cual (con ajustes menores) en el anexo. |
| `research_post_tfg/EDA_REPORT.md` | Caracterización completa del dataset v3 y v3.1 | Material canónico para el capítulo 3 (datos). Solo requiere traducción al castellano académico (ya está en castellano). |
| `research_post_tfg/sampling/SAMPLING_REPORT.md` | Diseño del muestreo de 200 imágenes para la Dra. Taberner | Material directo para la línea "iniciado y no concluido" del capítulo 6 nuevo. |
| `RESULTADOS_TFG.md` | Tablas experimentales LP, FT, eficiencia etiquetas, segmentación, ZS | Material canónico de cifras del capítulo 5 nuevo. |
| `tfg_uib_70pv2/Annexos.tex:1-104` | Estructura del repositorio público + tabla de 20 tareas experimentales + disponibilidad del código | Reutilizable como anexo A de la nueva memoria. |

---

## 7 · Propuesta de estructura para la nueva memoria

Índice detallado siguiendo la estructura objetivo de la regla 10 del
prompt.

### Resumen (≈ 1 página, 250-300 palabras)

- **Contenido.** Contexto (modelos fundacionales en dermatología clínica),
  objetivo del trabajo (caracterización empírica del estado del arte
  sobre dominio propio), método sintetizado (evaluación de N modelos
  sobre M datasets en cinco protocolos), resultados cuantitativos
  principales (sin "supera a..."), limitaciones, dirección de
  continuación.
- **Páginas:** 1.
- **Dependencias:** sintetiza la versión final de todos los capítulos.
- **Origen del material:** ningún resumen previo es reutilizable
  literalmente (los 4 disponibles incumplen al menos una regla 1-5). Se
  escribe nuevo, manteniendo coherencia numérica con el cap. 5.

### Capítulo 1 — Introducción y antecedentes

- **Título declarativo:** "Introducción: dermatología asistida por modelos
  fundacionales y motivación del trabajo".
- **Resumen 2-3 líneas:** contexto sanitario (lista de espera de
  teledermatología en Son Llàtzer), antecedentes (proyecto Dermapixel,
  blog de la Dra. Taberner) y trabajo previo del autor (prototipo
  DermApIxel desplegado en 2026-04-12) como base de despliegue, objetivos
  concretos del TFG en forma de tres preguntas operativas, alcance.
- **Páginas estimadas:** 5.
- **Dependencias:** ninguna anterior; condiciona el cap. 2 (qué modelos
  se priorizan).
- **Origen del material:** base en `tfg_uib_70pv2/Introduccio.tex:1-51`
  reescrito en tono académico (eliminar narrativización inicial y el
  desarrollo del giro Rosa, que se desplaza al cap. 6).
- **Restricción (regla 11):** no incluye líneas futuras ni proyecciones.

### Capítulo 2 — Estado del arte

- **Título declarativo:** "Estado del arte: modelos fundacionales para
  imagen dermatológica".
- **Resumen 2-3 líneas:** recorrido por las familias de modelos
  relevantes (encoders visuales auto-supervisados, modelos vision-lenguaje
  contrastivos, modelos de lenguaje multimodales generalistas);
  identificación de brechas operativas (idioma español, dominio clínico
  hispanohablante, equidad por fototipo, integración hospitalaria) que el
  TFG aborda empíricamente.
- **Páginas estimadas:** 7.
- **Dependencias:** cita el cap. 1; antecede a la elección de modelos
  evaluados del cap. 4.
- **Origen del material:** base en `tfg_uib_75p/Introduccio.tex:82-138`
  (sección "Estado del arte" del 75p) ampliada con la presentación de
  PanDerm, DermLIP y DermFM-Zero de `tfg_uib_70pv2/Introduccio.tex:29-37`.
  Material complementario en `COMPARATIVA_PAPER.md` (no leído línea por
  línea pero existe como referencia para datos comparativos).

### Capítulo 3 — Conjunto de datos y ontología

- **Título declarativo:** "Conjunto de datos: DermapixelAI v3.1, datasets
  externos y ontología jerárquica".
- **Resumen 2-3 líneas:** caracterización exhaustiva de DermapixelAI v3.1
  como aporte sustantivo (regla 6); descripción de los datasets externos
  utilizados; ontología jerárquica L1/L2/L3 y mapeo armonizado de 11
  fuentes a 72 654 imágenes.
- **Páginas estimadas:** 10.
- **Dependencias:** alimenta los experimentos de los caps. 4 y 5.
- **Origen del material:** base en `research_post_tfg/EDA_REPORT.md` (v3
  canónica) y `research_post_tfg/reclassify_modality/POST_RECLASSIFICATION_REPORT.md`
  (transición v3 → v3.1). El TFG entregado cita la versión v3 (1 109
  imágenes); decisión pendiente del autor sobre si la nueva memoria
  reporta v3 (consistencia con TFG entregado) o v3.1 (1 089 imágenes,
  versión operativa actual). Para la ontología, base en
  `tfg_uib_70pv2/Cap2_Datos.tex:96-133`. Material adicional:
  `DATASETS_DERMATOLOGIA.md` y `DATASETS_ROADMAP.md` (no leídos línea por
  línea en esta sesión).
- **Restricción (regla 16):** el capítulo debe ser denso en datos
  cuantitativos, con tabla resumen por dataset (origen, tamaño,
  modalidad, distribución por clases, licencia, uso concreto en el TFG).

### Capítulo 4 — Diseño experimental: modelos, protocolos y métricas

- **Título declarativo:** "Diseño experimental: modelos evaluados,
  protocolos y métricas".
- **Resumen 2-3 líneas:** enumeración de los modelos comparados
  (PanDerm Base/Large, DermLIP v2, BiomedCLIP, SigLIP, DINOv2, ConvNeXt-L,
  EfficientNetV2-L, SAM2.1-Large, GPT-4o, Gemini, MedGemma 4B/27B,
  variantes BLIP); descripción de los cinco protocolos (LP, FT
  supervisado, segmentación con LoRA sobre SAM2.1, zero-shot multimodal,
  evaluación LLM); descripción del hardware (DGX Spark, GB10 aarch64);
  métricas estándar (Acc, BAcc, F1 ponderada, AUROC, Dice/IoU,
  recall@k); protocolo de equidad sobre Fitzpatrick17k.
- **Páginas estimadas:** 10.
- **Dependencias:** referencias al cap. 2 (modelos del estado del arte) y
  al cap. 3 (datasets).
- **Origen del material:** base en `tfg_uib_70pv2/Cap3_Maquinaria.tex`
  completo (es el bloque con tono más académico de la versión activa).
- **Restricción (regla 12):** este capítulo no mezcla resultados; sólo
  cómo se ha medido.

### Capítulo 5 — Resultados y discusión

- **Título declarativo:** "Resultados experimentales sobre dominio propio
  y discusión".
- **Resumen 2-3 líneas:** presenta los resultados estructurados por
  bloque experimental (LP, FT, eficiencia de etiquetas, segmentación,
  zero-shot, LLMs, clasificador unificado, ensemble safety melanoma,
  equidad por fototipo, interpretabilidad SAE, recuperación visual), cada
  uno con métrica, intervalo de confianza cuando exista y caveats; la
  discusión interpretativa se ubica al final de cada bloque, no en un
  capítulo aparte (regla 13).
- **Páginas estimadas:** 12.
- **Dependencias:** depende de caps. 3 y 4; alimenta el cap. 6.
- **Origen del material:** base en `RESULTADOS_TFG.md` (cifras canónicas)
  + `tfg_uib_70pv2/Cap4_Replicacion.tex` + `tfg_uib_70pv2/Cap5_Derivadas.tex`
  + `tfg_uib_70pv2/Cap6_Revelacion.tex`, todos reescritos en tono
  académico. Tablas detalladas reaprovechables de `tfg_uib_75p/Annexos.tex`.
- **Restricción (regla 13 y 15):** cero claims sin medición; cada cifra
  reportada con IC o caveat; tablas y figuras con caption
  autocontenido.

### Capítulo 6 — Caminos y trabajo por hacer

- **Título declarativo:** "Caminos abiertos, trabajo iniciado y horizonte
  de investigación".
- **Resumen 2-3 líneas:** inventario en tres columnas (iniciado y no
  concluido / identificado no abordado / integración con DermApIxel).
- **Páginas estimadas:** 4.
- **Dependencias:** depende de caps. 3 y 5 (qué se midió y dónde están
  los gaps).
- **Origen del material:** estructura derivada de la sección 10 de este
  informe (sección 10 abajo).
- **Restricción (regla 14):** sin cierre grandilocuente; cada camino con
  su pre-requisito y grado de madurez actual.

### Bibliografía + anexos

- **Bibliografía:** base en `tfg_uib_70pv2/Bibliografia.tex` (64 líneas),
  ampliada con nuevas referencias del estado del arte que se incorporen
  al cap. 2.
- **Anexo A — Mapa de tareas experimentales y reproducibilidad:**
  reutilizar `tfg_uib_70pv2/Annexos.tex`.
- **Anexo B — Declaración sobre el uso de herramientas de IA:**
  `tfg_uib_70pv2/DeclaracionIA.tex` reutilizable.
- **Anexo C — Tablas detalladas de resultados (LP por dataset, FT por
  dataset, Fitzpatrick17k por fototipo y modelo, clasificador unificado
  L3 perclase):** material reaprovechable de `tfg_uib_75p/Annexos.tex` y
  `RESULTADOS_TFG.md`.
- **Anexo D — Pipeline de construcción y validación del dataset
  DermapixelAI:** material de `EDA_REPORT.md`,
  `POST_RECLASSIFICATION_REPORT.md` y `SAMPLING_REPORT.md`.

**Paginación tentativa:** 1 (Resumen) + 5 + 7 + 10 + 10 + 12 + 4 ≈ 49
páginas de cuerpo + anexos sin límite.

---

## 8 · Datos a destacar en el capítulo de datasets

### 8.1 · Dataset propio: DermapixelAI

| Atributo | v3 (defendido en el TFG) | v3.1 (operativo, post-TFG) | Origen |
|---|---|---|---|
| Imágenes totales | 1 109 | 1 089 | `EDA_REPORT.md:32`; `POST_RECLASSIFICATION_REPORT.md:19` |
| Casos con imagen | 672 (de 698 totales) | 672 (idéntico) — más 3 casos huérfanos sin imagen tras exclusiones | `EDA_REPORT.md:37`; `POST_RECLASSIFICATION_REPORT.md:106` |
| Modalidad clinical | 1 096 | 1 036 | `EDA_REPORT.md:32`; `POST_RECLASSIFICATION_REPORT.md:14` |
| Modalidad dermoscopy | 9 | 49 | ibid. |
| Modalidad histology | 2 | 2 | ibid. |
| Modalidad ultrasound | 1 | 1 | ibid. |
| Modalidad wood_lamp | 1 | 1 | ibid. |
| Splits (case-aware, sin leakage) | train 908 / val 160 / test 41 | train 891 / val 157 / test 41 | `EDA_REPORT.md:68`; `POST_RECLASSIFICATION_REPORT.md:25-29` |
| `label_source = ontology` | 97,93 % | 97,93 % | `EDA_REPORT.md:22` |
| `diagnosis_source = expert_v3` | 98,38 % | 98,38 % | ibid. |
| `rosa_verified = True` | 82,96 % | 82,96 % | ibid. |
| L1 efectivas | 4 (Patología inflamatoria 49 %, tumoral 25 %, infecciosa 23 %, Genodermatosis < 1 %) | 4 (idem) | `EDA_REPORT.md:48`; `POST_RECLASSIFICATION_REPORT.md:115-122` |
| L2 efectivas | 38 (39 raw con 2 variantes ortográficas de "Trastornos queratinización") | 38 | `EDA_REPORT.md:49` |
| L3 efectivas / vocabulario | 251 / 367 (68,4 %) | 250 / 367 | `EDA_REPORT.md:50`; `SAMPLING_REPORT.md:144` |
| Cola larga | 178 L3 con ≤ 5 imágenes, 65 con 1 imagen | similar | `EDA_REPORT.md:60` |
| L1/L2 sin representación en test | Genodermatosis (0 imágenes), 22 L2 sin test, 11 L2 sin val | similar | `EDA_REPORT.md:73-87` |
| Texto narrativo | mediana 223 palabras/caso, p25=175 / p75=271 | idem | `EDA_REPORT.md:126` |
| Texto con mención "diagnóstico" / "diagnosticar" | 4,6 % de los casos (32 de 698) | idem | `EDA_REPORT.md:129` |
| Integridad técnica | 0 imágenes corruptas, 0 hashes MD5 discordantes | 0 / 0 | `EDA_REPORT.md:114` |
| Cobertura temporal | 2011-2026, pico en 2016 | idem | `EDA_REPORT.md:138` |
| Licencia | (no documentada de forma explícita en el material leído; pendiente de decidir al publicar) | idem | `EDA_REPORT.md` no la cita; verificar antes de la entrega. |

**Decisión pendiente del autor:** si la nueva memoria cita las cifras de
v3 (consistencia con el TFG entregado) o las de v3.1 (versión
operativa). El equipo del proyecto ya tiene `project_dermapixel_v3_1.md`
que zanja: el TFG entregado no se afecta; cualquier publicación posterior
usa v3.1.

### 8.2 · Datasets externos utilizados

Resumen mínimo. La caracterización detallada (origen, tamaño, modalidad,
distribución por clases, licencia, uso concreto en el TFG) se desarrolla
en el cap. 3 nuevo. Cifras tomadas de `RESULTADOS_TFG.md`,
`tfg_uib_70pv2/Cap2_Datos.tex` y `tfg_uib_75p/Annexos.tex` salvo nota.

| Dataset | N test (LP) | Clases | Modalidad | Uso en el TFG |
|---|---:|---:|---|---|
| HAM10000 | 1 232 | 7 | Dermoscopia | LP, FT, ZS, ensemble safety, evaluación LLMs |
| BCN20000 | 1 242 | 9 | Dermoscopia | LP |
| PAD-UFES-20 | 461 | 6 | Clínica móvil | LP, FT |
| DDI | 137 | 2 | Clínica diversa | LP, FT, equidad |
| Dermnet | 4 002 | 23 | Clínica atlas | LP (con caveat de leakage frente a Derm1M) |
| Derm7pt clínico | 168 | 2 | Clínica | LP |
| Derm7pt dermo | 225 | 2 | Dermoscopia | LP |
| HIBA | 334 | 2 | Dermoscopia | LP (caveat leakage) |
| MSKCC | 1 664 | 2 | Dermoscopia | LP, FT (caveat leakage) |
| WSI patches | 12 354 | 16 | Histopatología | LP |
| ISIC2018 | 2 594 | binaria | Dermoscopia | Segmentación |
| ISIC2017 / PH2 | varios | binaria | Dermoscopia | Generalización segmentación (sin reentrenamiento) |
| Fitzpatrick17k | 16 577 | 114 patologías + 6 fototipos | Clínica | Equidad por fototipo (5 modelos) |
| SkinCon | 3 230 | 48 conceptos | Clínica | Validación CBM sobre SAE |
| Derm1M | 1 029 761 pares / 403 563 imágenes | 390 condiciones | Multimodal | Pretraining DermLIP (no es benchmark de evaluación); RAG visual |

### 8.3 · Trazabilidad

- Pipeline de construcción de DermapixelAI v3: `tfg_uib/Memoria.tex:336-389`
  y `datasets/dermapixel_panderm_dataset/README.md` (no leído línea por
  línea pero existe).
- Reclasificación v3 → v3.1: `research_post_tfg/reclassify_modality/`
  contiene `apply_reclassification.py` con listas hardcodeadas (40
  DERMOSCOPY, 20 NOT_DERM), audit log con timestamp, backup completo en
  `_backup_2026-05-23/`.
- Ontología L1/L2/L3 con códigos SNOMED-CT y CIE-10:
  `tfg_uib/Memoria.tex:182-198`.
- Mapeo de 244 nombres de clase a 47/43 L3 entrenables:
  `tfg_uib_70pv2/Cap5_Derivadas.tex:226-228`.

---

## 9 · Resultados a destacar en el capítulo de resultados

Listado priorizado para el cap. 5 nuevo. Cada entrada con el formato
"experimento · modelos · métrica · valor · dataset · log/origen".

### 9.1 · Replicación core (PanDerm)

1. **LP PanDerm Large 10 datasets.** Accuracy 0,791 / AUROC 0,901 /
   BAcc 0,649 (medias). Concordancia con paper Yan et al. 2025 dentro de
   ≤ 0,9 pp por dataset. Origen: `RESULTADOS_TFG.md` §FASE 1.
2. **FT PanDerm Large HAM10000.** Acc 0,919 / BAcc 0,813 / AUROC 0,978.
   Origen: `tfg_uib_70p/Cap6_Revelacion.tex:23`.
3. **FT PanDerm Large PAD-UFES.** Acc 0,800 / Top-3 0,970. Origen:
   `tfg_uib_70p/Cap6_Revelacion.tex:24`.
4. **FT PanDerm Large DDI.** Degradación frente a LP (LP 0,847 → FT
   Base 0,774, –7,3 pp). Caveat: N<700 produce overfitting. Origen:
   `RESULTADOS_TFG.md` líneas 133-135.
5. **Eficiencia de etiquetas HAM 1 %.** AUROC 0,918 con 82 imágenes;
   curva satura al 5 %. Origen: `RESULTADOS_TFG.md` línea 72.

### 9.2 · Segmentación

6. **SAM2.1-Large fine-tuned LoRA sobre ISIC2018.** Dice 0,947 /
   IoU 0,903. Generalización a ISIC2017 (Dice 0,945) y PH2 (Dice 0,960)
   sin reentrenamiento. Origen: `tfg_uib_70pv2/Cap4_Replicacion.tex:132-134`.

### 9.3 · Zero-shot multimodal y dependencia del tokenizador

7. **Zero-shot HAM10000 DermLIP con PubMedBERT y prompts genéricos.**
   AUROC 0,366 (inferior al azar). Origen: `RESULTADOS_TFG.md` línea 223.
8. **Zero-shot HAM10000 DermLIP con GPT-2/CLIP y prompts enriquecidos.**
   AUROC 0,854. Sensibilidad al prompt: óptimo en torno a 10 palabras.
   Origen: `tfg_uib_70pv2/Cap5_Derivadas.tex:17,38`.

### 9.4 · Modelos de lenguaje generales

9. **GPT-4o ZS HAM10000.** Accuracy 0,485. **MedGemma 27B ZS** 0,665;
   con LoRA 0,802. PanDerm Large FT 0,919. Diferencia frente a GPT-4o
   +43,4 pp; frente a MedGemma 27B ZS +25,4 pp; con LoRA +11,7 pp.
   Origen: `tfg_uib_70pv2/Cap5_Derivadas.tex:159`.

### 9.5 · Clasificador unificado y ensemble de seguridad para melanoma

10. **Clasificador unificado L1.** Accuracy 94,7 % (4 categorías
    etiológicas). Origen: `tfg_uib_70pv2/Cap6_Revelacion.tex:61`.
11. **Clasificador unificado L2.** Accuracy 81,9 % sobre 26 subcategorías
    efectivas. Origen: `tfg_uib_70pv2/Cap6_Revelacion.tex:64`.
12. **Clasificador unificado L3 merged43 + TTA.** Accuracy 81,0 % /
    BAcc 81,82 % / Top-3 95,4 %. Mejora respecto a la línea base +4,72 pp
    BAcc. Origen: `tfg_uib_70p/Cap6_Revelacion.tex:35`.
13. **Ensemble safety melanoma (M1 + M7 + SigLIP LP).** Recall 100 %
    (70/70 positivos en split test HAM) / AUROC 0,991. Caveat: N=70 y
    prevalencia no clínica. Origen: `tfg_uib_70p/Cap6_Revelacion.tex:36`.

### 9.6 · Equidad por fototipo

14. **Fitzpatrick17k LP 5 modelos.** N=16 577 imágenes; PanDerm Large
    AUROC global 0,912; AUROC fototipo VI 0,830; gap 8,9 pp. BiomedCLIP
    presenta el menor gap (datos no recogidos línea a línea, citado en
    `tfg_uib_70pv2/Cap5_Derivadas.tex:200`) pero con AUROC global 0,856.
    Origen: `tfg_uib_70p/Cap6_Revelacion.tex:37-38`.

### 9.7 · Interpretabilidad

15. **SAE Large 16 384 features sobre PanDerm Large.** Sparsity ≈ 15 %
    tras 100 épocas; sin features muertas. Origen:
    `tfg_uib_70pv2/Cap5_Derivadas.tex:55-59`.
16. **Concept Bottleneck Model sobre 22 conceptos SkinCon.** Media
    CBM 0,920 vs LP directo 0,909 (caveat: sesgo de selección porque las
    features SAE se eligieron parcialmente sobre el mismo conjunto de
    validación). Tres conceptos top con AUROC > 0,90: pedunculado 0,929,
    friable 0,913, exofítico 0,908. 13 de 35 conceptos evaluables con
    AUROC > 0,80. Origen: `tfg_uib_70pv2/Cap5_Derivadas.tex:67,117`.

### 9.8 · Recuperación visual sobre Derm1M

17. **Índice FAISS sobre 421 327 imágenes de Derm1M.** Latencia
    ≈ 150 ms/query. Hallazgo: densidad anómala del espacio (cono angular
    estrecho), atractor semántico para granuloma piogénico. Mitigación:
    temperature scaling y z-score por consulta. Origen:
    `tfg_uib_70pv2/Cap5_Derivadas.tex:121-145`.

### 9.9 · Auditoría de leakage Derm1M

18. **Auditoría hash-based.** Solapamiento confirmado entre Derm1M y
    Dermnet, MSKCC, HIBA; ausencia de solapamiento sobre HAM10000,
    BCN20000, PAD-UFES, DDI, Derm7pt, WSI. El ranking de modelos cambia
    al pasar de 10 a 7 datasets (DermLIP v2 retrocede frente a PanDerm
    Large). Origen: `tfg_uib_70pv2/Cap4_Replicacion.tex:30-44`.

---

## 10 · Caminos y trabajo por hacer (material para el capítulo 6)

Inventario en tres columnas, con pre-requisitos y grado de madurez actual
en la fecha de cierre del TFG entregado (2026-05-13).

### 10.1 · Iniciado y no concluido

| Camino | Grado de madurez | Pre-requisito de continuación |
|---|---|---|
| Anotación de 200 imágenes con la Dra. Taberner sobre 34 conceptos clínicos | Diseño del muestreo completo (`SAMPLING_REPORT.md`): 48 dermo + 132 clínicas + 15 long-tail + 5 controles. Set generado en `annotation_set_200.csv`. Pendiente: sesiones reales de anotación con la Dra. Taberner (estimado 5 h en 4 sesiones). | Disponibilidad de la Dra. Taberner; tras anotar, entrenar CBM contra los 34 conceptos. |
| Dataset DermapixelAI v3.1 publicado | Reclasificación de modalidad ejecutada el 2026-05-23 (40 movidas a dermoscopy + 20 excluidas). Backup completo, audit log, validation report. Pendiente: licencia de publicación, eliminar carpeta `images/microscopy/` vacía, verificar 19 imágenes sin L1 (`label_source = raw`). | Decisión de licencia y vehículo de publicación. |
| Solicitud CEIC para banco hospitalario HUSLL (~ 22 000 estudios) | Comentada como necesaria en `project_spanderm_design_decision_2026_05_23.md`; no se ha presentado en el periodo del TFG. | Aprobación CEIC IB-Salut + estructuración del corpus + mapeo a ontología. Condición para SpanDerm v1 (cabeza L3 directa con 251 clases). |
| Fine-tuning SpanDerm v0 sobre DermapixelAI v3.1 | Decisión arquitectónica tomada (cabeza L2 con 38 clases efectivas + ranking L3 por embeddings; LoRA en últimas dos capas del encoder). 908 imágenes de train disponibles. Pendiente: ejecución y publicación. | DGX Spark accesible (ya verificada); decisión de incluir o no contrastive loss con `case_text`. |
| Colaboración formal con el grupo Monash | Contacto establecido por escrito; interés confirmado por las dos partes; sin acuerdo formal a la fecha de cierre. | Data summary detallado de DermapixelAI v3.1 + propuesta de colaboración + coordinación con la Dra. Taberner y el Dr. Varona. |
| Publicación 1 (Replicación PanDerm + análisis leakage Derm1M) | Datos completos. Falta redactar manuscrito. | Decisión de revista diana; redacción. |
| Publicación 2 (DermapixelAI + ontología + clasificador unificado + ensemble safety) | Datos completos para clasificador + ensemble. Falta SpanDerm fine-tune sobre v3.1 para fortalecer la sección de español. | Cierre de SpanDerm v0; redacción. |
| Publicación 3 (SAE + SkinCon + CBM + 34 conceptos Rosa) | Diccionario SAE entrenado, 34 conceptos definidos. Falta la anotación de las 200 imágenes y la evaluación. | Anotación con la Dra. Taberner (camino primero de esta lista). |

### 10.2 · Identificado y no abordado

| Camino | Pre-requisito |
|---|---|
| Validación clínica prospectiva en Son Llàtzer (silent deployment, ~ varios miles de casos) | Aprobación CEIC IB-Salut; despliegue del prototipo bajo Keycloak OIDC + HTTPS hospitalario; integración PACS; estudio diseñado con plan estratificado por modalidad y por fototipo. |
| Reentrenamiento DermLIP multilingüe (Derm1M-inglés + DermapixelAI-español) | Disponibilidad de hardware en horas equivalentes al pretraining DermLIP original; decisión de objetivo (CLIP-style estándar vs SigLIP-style). |
| Federated learning piloto entre hospitales de Baleares | Acuerdo institucional Son Llàtzer + Son Espases (u otro); diseño técnico del orquestador; integración con HCE. |
| Evaluación de DermFM-Zero sobre DermapixelAI v3.1 y archivo Son Llàtzer | Liberación de pesos de DermFM-Zero (no pública a 2026-05-23). |
| Capa agéntica con LLM clínico orquestador (segmentación, conceptos SAE, RAG, razonamiento, M5) | Definición de protocolo agéntico; coordinación con `Cap8_Conclusiones.tex` línea AMIE; instrumentación de medición (qué se mide del agente y cómo). |
| Evaluación multilingüe del estado del arte | Conjunto de evaluación en al menos español, inglés y catalán; protocolo de evaluación; participación de dermatólogos del HUSLL. |
| InstructBLIP/BLIP-2 Q-Former fine-tune sobre DermapixelAI | Hardware disponible; decisión de objetivo (caption vs VQA dermatológico). |

### 10.3 · Integración con DermApIxel

| Componente del TFG | Módulo destino en DermApIxel | Supuestos técnicos |
|---|---|---|
| Clasificador unificado L1/L2/L3 merged43 + TTA | Módulo M7 (clasificación jerárquica) | Modelo en producción a 2026-04-12 (`MEMORY.md` `project_dermapixel_unified_integration`). |
| Ensemble safety melanoma (M1 + M7 + SigLIP LP) | Módulo M8 (safety screen) | M1 HAM10000 ya integrado; SigLIP LP integrado a 2026-04-? (`MEMORY.md` `project_ensemble_siglip`). |
| Sparse Autoencoder + 34 conceptos | Módulo M3 (interpretabilidad) | Diccionario SAE entrenado; UI con z-score por feature (`MEMORY.md` `project_sae_fix_r2r1`). |
| RAG FAISS sobre 421 327 imágenes Derm1M | Módulo M4 (recuperación visual) | Embeddings DermLIP v2 ya extraídos; temperature scaling + z-score en producción. |
| LLM clínico con prompt estructurado de 300 palabras | Módulo M5 (razonamiento clínico) | 9 proveedores LLM disponibles (`MEMORY.md` `project_llm_providers`); prompt UNIF integrado a 2026-04-? (`MEMORY.md` `project_dermapixel_llm_unif_integration`). |
| Zero-shot DermLIP con presets de prompts | Módulo M6 (zero-shot abierto) | 372 prompts en 28 presets a 2026-04-19 (`MEMORY.md` `project_zeroshot_presets_update`). |
| Segmentación SAM2.1-Large fine-tuned | Módulo M2 (segmentación) | Modelo en producción. |
| Clasificador HAM10000 (PanDerm FT) | Módulo M1 (clasificación 7 clases) | Modelo en producción con TTA (`MEMORY.md` `project_tta_m1`). |

**Decisión que el cap. 6 deberá explicitar:** SpanDerm v0 (cabeza L2 +
ranking L3) sustituirá al actual M7 de DermApIxel en una versión
posterior, condicionada a la anotación de la Dra. Taberner y a la
estabilización del entrenamiento sobre 908 imágenes de train de v3.1.

---

## Resumen final (8-10 líneas)

- Versiones previas revisadas: 4 (`tfg_uib` referencia, `tfg_uib_75p`
  descartada, `tfg_uib_70p` referencia narrativa congelada,
  `tfg_uib_70pv2` activa al cierre — 86 p PDF / 67 árabes,
  1 602 líneas `.tex`).
- Cifras cuantitativas recopiladas y clasificadas: **47 sólidas**
  (sección 3.1), **8 frágiles** (sección 3.2) y **6 descartadas**
  (sección 3.3).
- Afirmaciones no validadas identificadas: **15** (sección 4), de las
  cuales 7 son hipérboles o marcos competitivos a eliminar, 5
  generalizaciones a acotar al benchmark, 2 conjeturas correctamente
  declaradas a conservar como tal y 1 cifra histórica (1 888 imágenes)
  no reproducible.
- Hallazgo principal sobre contradicciones entre versiones: el dataset
  DermapixelAI tiene dos versiones canónicas distintas (v3 con
  1 109 imágenes citada en el TFG entregado; v3.1 con 1 089 imágenes
  operativa post-TFG). El autor debe decidir cuál cita la nueva memoria.
- El índice propuesto (sección 7) sigue la estructura clásica académica
  Resumen + Introducción/Antecedentes + Estado del Arte + Datos +
  Diseño Experimental + Resultados con Discusión + Caminos abiertos +
  Bibliografía/Anexos, dentro del rango 40-60 páginas de cuerpo, con
  títulos declarativos y eliminación de "DermApIxel" del título de la
  portada.
- Puntos que requieren decisión del autor antes de Fase 2: (a) cifras
  del dataset v3 vs v3.1 a citar; (b) confirmación del título de la
  portada (volver a "Evaluación de modelos fundacionales para
  Dermatología Clínica" de las versiones `tfg_uib`/`tfg_uib_75p`/`tfg_uib_70p`
  o adoptar otro título declarativo, recordando que la regla 4 excluye
  a DermApIxel como protagonista); (c) tratamiento del capítulo 7
  "Prototipo" (degradar a sección dentro del cap. 6 o mantener como cap.
  separado más corto); (d) si el resumen nuevo conserva el giro narrativo
  del curso de la Dra. Taberner o lo desplaza al cap. 6 como camino
  reorientado.
