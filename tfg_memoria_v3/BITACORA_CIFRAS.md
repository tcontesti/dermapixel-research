# Bitácora de cifras — TFG memoria v3

Tabla de control de trazabilidad numérica. Cada cifra citada en un capítulo
de la nueva memoria queda registrada aquí con su valor exacto, ubicación
en el documento, fuente primaria y fecha de la fuente. La bitácora se
revisa al cierre de cada fase para detectar contradicciones entre
capítulos.

Convenciones:

- "valor" es el valor literal citado, conservando el formato (ortográfico
  en cuerpo de texto, numérico en tablas).
- "cap. + sección" referencia la etiqueta LaTeX del bloque donde
  aparece.
- "fuente primaria" es la ruta y línea del fichero canónico que respalda
  la cifra; si la fuente es bibliográfica, se cita la `\bibitem` clave.
- "fecha de la fuente" es la fecha del documento o, si la fuente es un
  log/script, la fecha del experimento o de la operación.

---

## Capítulo 1 · Introducción y antecedentes

| Cifra | Valor | Cap. + sección | Fuente primaria | Fecha de la fuente |
|---|---|---|---|---|
| Antigüedad del archivo asistencial del Servicio de Dermatología del HUSLL | "aproximadamente veinticinco años" (≈ 25) | `cap:intro` § `sec:contexto` | Dato cualitativo asociado a la trayectoria asistencial del HUSLL desde su apertura (2001); sin documento institucional citado | 2026 |
| Supervivencia específica melanoma cutáneo, estadio I → IV (5 años) | ≈ 99 % → ≈ 25 % | `cap:intro` § `sec:contexto` | `\cite{ajcc8}` (AJCC Cancer Staging Manual, 8.ª ed.; Gershenwald et al. 2017) | 2017 |
| DIADERM — diagnósticos | 10 999 | `cap:intro` § `sec:contexto` | `\cite{diaderm2018}` (Buendía-Eisman et al., *Actas Dermo-Sifiliográficas*) | 2018 |
| DIADERM — pacientes | 8 953 | `cap:intro` § `sec:contexto` | `\cite{diaderm2018}` | 2018 |
| DIADERM — diagnósticos más prevalentes | 10 (queratosis actínica, carcinoma basocelular, nevus melanocítico, queratosis seborreica, otras neoplasias benignas, psoriasis, acné, verrugas víricas, otros trastornos de la pigmentación, otras dermatitis) | `cap:intro` § `sec:contexto` | `\cite{diaderm2018}` | 2018 |
| HUSLL — diagnósticos diferentes a lo largo de un año asistencial (Taberner 2010) | 213 | `cap:intro` § `sec:contexto` | `\cite{taberner2010_motivos}` (Taberner et al., *Actas Dermo-Sifiliográficas*) | 2010 |
| Dermapixel — casos clínicos comentados | "más de setecientos" (> 700) | `cap:intro` § `sec:dermapixel` | Blog Dermapixel ([https://dermapixel.com](https://dermapixel.com)); confirmado en `tfg_uib_70pv2/Resum.tex:5` y `tfg_uib_70pv2/Introduccio.tex:7` | 2026-05-13 (snapshot del archivo del blog en el cierre del material previo) |
| Dermapixel — años de actividad | "más de quince" (> 15) | `cap:intro` § `sec:dermapixel` | ídem | ídem |
| Antecedentes técnicos del autor | (cualitativos, sin cifras) | `cap:intro` § `sec:trabajo-previo` | Dos líneas previas en colaboración con la Dra.~R.~Taberner: (a) modernización tecnológica del archivo Dermapixel desde Blogger a pila propia; (b) participación en un proyecto institucional del IB-Salut sobre teledermatología hospitalaria. No se cita el prototipo DermApIxel en esta sección por desarrollarse durante el TFG (descrito en cap.~7). | 2025--2026 (anteriores al cierre del TFG) |
| PanDerm — modalidades del preentrenamiento | 4 (fotografía corporal total, dermoscopia, fotografía clínica, histopatología) | `cap:intro` § `sec:fundacionales-intro` | `\cite{panderm2025}` (Yan et al., *Nature Medicine*) | 2025 |
| Datasets externos contrastados en el TFG | 12 (HAM10000, BCN20000, PAD-UFES-20, DDI, Dermnet, Derm7pt clínico, Derm7pt dermatoscópico, HIBA, MSKCC, WSI patches, Fitzpatrick17k, SkinCon, ISIC2018; Derm7pt cuenta como una entrada del corpus aunque se trabaja en dos variantes) | `cap:intro` § `sec:objetivos` y § `sec:estructura` | `INFORME_RECONOCIMIENTO.md` § 8.2; `RESULTADOS_TFG.md` líneas 17--36 | 2026-05-23 |
| Niveles de la ontología jerárquica | 3 (L1 etiológico, L2 subcategoría, L3 diagnóstico) | `cap:intro` § `sec:objetivos` | Diseño con revisión experta de la Dra.~R.~Taberner; `tfg_uib_70pv2/Cap2_Datos.tex:96--105` | 2026-05-13 |
| Frentes experimentales principales | 5 (LP/FT, segmentación, evaluación cruzada Derm1M, zero-shot multimodal, comparación con LLMs) | `cap:intro` § `sec:alcance` | Definición operativa del TFG, alineada con `INFORME_RECONOCIMIENTO.md` § 7 y § 9 | 2026-05-23 |
| Bloques derivados | 5 (clasificador unificado, ensamble safety melanoma, equidad por fototipo, interpretabilidad SAE+CBM, recuperación visual densa) | `cap:intro` § `sec:alcance` | ídem | 2026-05-23 |
| Hardware único del trabajo | NVIDIA DGX Spark, chip Grace Hopper GB10, sistema aarch64 | `cap:intro` § `sec:alcance` | `tfg_uib_70pv2/Cap3_Maquinaria.tex:9-13` | 2026-05-13 |
| DermapixelAI v3.1 — imágenes totales | 1 089 | `cap:intro` § `sec:estructura` | `research_post_tfg/reclassify_modality/POST_RECLASSIFICATION_REPORT.md:19` | 2026-05-23 |
| Estructura del documento | 7 capítulos + 4 anexos | `cap:intro` § `sec:estructura` | Decisión de redacción de Fase 2 alineada con `INFORME_RECONOCIMIENTO.md` § 7 ampliado por `PROMPT_FASE2_Cap1_Introduccion.md` decisión 3 (Cap. 7 separado) | 2026-05-23 |

**Notas de correcciones aplicadas tras revisión del autor (post-Fase 2):**

- Se elimina la cifra "> 300 000 imágenes archivadas en HUSLL" del § 1.1 por falta de fuente institucional formal. Reformulada cualitativamente como "volumen significativo de imágenes archivadas".
- Se añade la cifra de supervivencia específica del melanoma cutáneo (estadio I ≈ 99 % → estadio IV ≈ 25 %, 5 años) con `\cite{ajcc8}` (AJCC 8.ª ed.) como sustento del párrafo sobre criticidad temporal del diagnóstico melanocítico. La entrada se mantiene en la tabla principal.
- Bibliografía: a la lista de claves pendientes de añadir a la consolidación (Fase 9) se suma `\cite{ajcc8}` además de `\cite{diaderm2018}` y `\cite{taberner2010_motivos}` (estas dos últimas ya estaban en `tfg_uib_70pv2/Bibliografia.tex`).
- Reescritura completa del § 1.3. La sección anterior identificaba erróneamente el prototipo DermApIxel como trabajo previo del autor; la versión vigente lo desplaza al cap.~7 (se desarrolla durante el TFG, no antes) y describe en su lugar las dos líneas técnicas verdaderamente previas: (a) migración tecnológica del archivo Dermapixel desde Blogger a una pila propia, y (b) participación en un proyecto institucional del IB-Salut sobre teledermatología hospitalaria. En consecuencia se retira de la bitácora la cifra "12 de abril de 2026" (despliegue del prototipo) por no figurar ya en el cap.~1. La fecha se reincorporará a la bitácora cuando se documente en el cap.~7.
- Reescritura del bloque de objetivos (§ 1.5). La versión anterior identificaba a DermapixelAI v3.1 como "corpus propio" eje del trabajo y a la ontología L1/L2/L3 como aplicada sobre él. La realidad operativa del TFG es la inversa: el núcleo experimental se construye sobre doce datasets externos públicos armonizados mediante una ontología jerárquica L1/L2/L3 diseñada con revisión experta, y la construcción del corpus DermapixelAI se desarrolla en paralelo con experimentación sistemática iniciada hacia el cierre del TFG y prolongada en la fase posterior (cap.~6). Los objetivos pasan de tres a cuatro: O1 evaluación sobre los 12 datasets externos · O2 armonización ontológica · O3 construcción del corpus DermapixelAI · O4 integración operativa. En coherencia, se reformula el bloque derivado (a) del § 1.6 y la descripción del cap.~3 en el § 1.7. Se añaden a esta bitácora dos entradas: "Datasets externos contrastados en el TFG · 12" y "Niveles de la ontología jerárquica · 3".
- Reescritura del primer párrafo del § 1.1. La versión anterior describía el archivo HUSLL como soporte de un flujo de teledermatología actual sobre el que el dermatólogo decide sin examen físico previo. Esta caracterización no corresponde a la situación real del Servicio: el archivo es el resultado acumulado de aproximadamente veinticinco años de consulta externa presencial, organizado de forma idiosincrásica por cada facultativo y sin esquema común de metadatos. Se sustituye también el segundo párrafo, introduciendo la derivación desde atención primaria por el médico de familia como mecanismo habitual de acceso al especialista, y la teledermatología como vía complementaria orientada al cuello de botella de capacidad asistencial.
- Reescritura del § 1.2 (Antecedentes del proyecto Dermapixel). La versión anterior fusionaba la descripción del blog con la mención al proyecto institucional del IB-Salut y con el curso formativo de la Dra.~Taberner sobre razonamiento melanocítico/no melanocítico, del que derivaba el vocabulario de 34 conceptos clínicos. La separación correcta es: (a) § 1.2 describe únicamente el blog Dermapixel como antecedente clínico/docente y su rol como material base de DermapixelAI; (b) la colaboración técnica entre el autor y la Dra.~Taberner sobre la migración del archivo y sobre el proyecto IB-Salut se desplaza al § 1.3 (trabajo previo del autor, ya reescrito en corrección anterior); (c) el curso formativo y el vocabulario de 34 conceptos se reservan para los capítulos donde se documentan los resultados experimentales o el trabajo en curso (cap.~5 o cap.~6, no cap.~1). Como consecuencia se retira de esta bitácora la entrada "Conceptos clínicos visuales adicionales a SkinCon definidos con la Dra.~Taberner · 34" del cap.~1; la cifra reaparecerá en la bitácora cuando se documente en su capítulo correspondiente.
- Adición al § 1.4 de un párrafo final sobre la integración del componente lingüístico como dimensión históricamente subexplotada en los modelos de imagen dermatológica y como motivación, compartida entre el autor y la Dra.~Taberner, para priorizar la línea multimodal del estudio. No introduce cifras nuevas.
- Refuerzo del objetivo O3 del § 1.5 con la explicitación de que la construcción del corpus DermapixelAI se realiza en un formato "compatible con la práctica investigadora habitual" y orientado a "habilitar su uso en trabajos académicos posteriores".
- Reformulación del objetivo O1. El enunciado anterior ("Evaluación empírica del estado del arte sobre los datasets canónicos") presentaba la actividad como aplicación de protocolos sobre modelos publicados, sin reflejar el componente de implementación y puesta en funcionamiento que constituye el grueso del trabajo experimental. La versión vigente lo retitula "Implementación y validación experimental de los modelos fundacionales del estado del arte sobre los datasets accesibles", explicita que se trata de montar y poner en funcionamiento los modelos sobre el hardware del proyecto y de verificar empíricamente su comportamiento sobre los datasets externos efectivamente accesibles, y declara expresamente que este objetivo constituye la base experimental sobre la que se asienta el resto del trabajo.
- Reducción del bloque de objetivos del § 1.5 de cuatro a dos. La armonización ontológica jerárquica (antiguo O2) y la integración operativa en el prototipo DermApIxel (antiguo O4) no eran objetivos formulados al inicio del trabajo, sino bloques de trabajo que emergieron durante el desarrollo del proyecto a partir de los objetivos principales (O1 implementación y validación experimental, O2 actual construcción del corpus DermapixelAI). En la versión vigente, los objetivos formales del TFG son únicamente dos. A partir de ellos se reconocen explícitamente los bloques derivados ---armonización ontológica, ensamble de seguridad para melanoma, equidad por fototipo, interpretabilidad SAE/CBM, recuperación visual densa, integración en prototipo---, que se desplazan en su totalidad al capítulo~6, donde se discuten en clave de prácticas habituales en el campo, hallazgos parciales, limitaciones observadas y líneas de evolución futura. En consecuencia se eliminan del § 1.6 los cinco bloques derivados (a-e), se reformula la descripción del capítulo~6 en el § 1.7, y se mantienen los cinco frentes principales del § 1.6 como descomposición operativa exclusiva del objetivo O1.

---

## Capítulo 2 · Estado del arte

Todas las cifras de este capítulo son cifras heredadas de la literatura
publicada (no resultados experimentales del TFG). El cap. 5 reserva las
cifras propias.

| Cifra | Valor | Cap. + sección | Fuente primaria | Fecha de la fuente |
|---|---|---|---|---|
| DINOv2 — corpus de preentrenamiento (imágenes naturales curadas) | 142 millones | `cap:sota` § `sec:encoders-visuales` | `\cite{dinov2}` (Oquab et al., TMLR 2024) | 2024 |
| PanDerm — imágenes de preentrenamiento | "aproximadamente dos millones cien mil" (≈ 2,1 M) | `cap:sota` § `sec:encoders-visuales` | `\cite{panderm2025}` (Yan et al., Nature Medicine 2025) | 2025 |
| PanDerm — instituciones de origen del corpus | 11 | `cap:sota` § `sec:encoders-visuales` | `\cite{panderm2025}` | 2025 |
| PanDerm — modalidades del preentrenamiento | 4 (fotografía corporal total, dermoscopia, fotografía clínica, histopatología) | `cap:sota` § `sec:encoders-visuales` | `\cite{panderm2025}` | 2025 |
| CLIP — pares imagen-texto de preentrenamiento | 400 millones | `cap:sota` § `sec:vision-lenguaje` | `\cite{clip2021}` (Radford et al., ICML 2021) | 2021 |
| BiomedCLIP — pares imagen-texto biomédicos | "aproximadamente quince millones" (≈ 15 M) | `cap:sota` § `sec:vision-lenguaje` | `\cite{biomedclip}` (Zhang et al., NEJM AI 2024) | 2024 |
| Derm1M — pares imagen-texto | 1 029 761 | `cap:sota` § `sec:vision-lenguaje` | `\cite{derm1m}` (Yan et al., 2025) | 2025 |
| Derm1M — imágenes únicas | 403 563 | `cap:sota` § `sec:vision-lenguaje` | `\cite{derm1m}` | 2025 |
| Derm1M — niveles de la ontología jerárquica de origen | 4 | `cap:sota` § `sec:vision-lenguaje` | `\cite{derm1m}` | 2025 |
| DermFM-Zero — imágenes para masked latent modeling | 3 millones | `cap:sota` § `sec:zero-shot-nativo` | `\cite{dermfmzero2026}` (Yan et al., 2026) | 2026 |
| DermFM-Zero — pares texto-imagen para bootstrapped contrastive learning | 1 millón | `cap:sota` § `sec:zero-shot-nativo` | `\cite{dermfmzero2026}` | 2026 |
| DermFM-Zero — clínicos participantes en los reader studies | "más de mil cien" (> 1 100) | `cap:sota` § `sec:zero-shot-nativo` | `\cite{dermfmzero2026}` | 2026 |
| SAM — imágenes de preentrenamiento | 11 millones | `cap:sota` § `sec:segmentacion` | `\cite{sam2023}` (Kirillov et al., ICCV 2023) | 2023 |
| SAM — máscaras generadas | "más de mil millones" (> 1 000 M) | `cap:sota` § `sec:segmentacion` | `\cite{sam2023}` | 2023 |
| Latencia típica de consulta en recuperación visual densa (FAISS) | "del orden de los cien milisegundos" (≈ 100 ms) sobre corpus de centenares de miles a millones de embeddings precomputados | `cap:sota` § `sec:vision-lenguaje` | `\cite{faiss2019}` (Johnson et al., IEEE Trans. Big Data 2019); rango general reportado por la literatura de búsqueda vectorial aproximada | 2019 (paper de referencia) |
| Brechas operativas identificadas | 4 (disponibilidad efectiva de modelos · concentración geográfica de corpus · ausencia de texto clínico en español · distancia entre evaluación publicada e integración hospitalaria) | `cap:sota` § `sec:brechas` | Síntesis propia del autor a partir del repaso del estado del arte | 2026-05-24 |

**Referencias añadidas a `Bibliografia.tex` para el Cap. 2:**
`\cite{vit2021}` (Dosovitskiy et al., ICLR 2021), `\cite{clip2021}`
(Radford et al., ICML 2021), `\cite{siglip2023}` (Zhai et al., ICCV
2023), `\cite{sam2023}` (Kirillov et al., ICCV 2023), `\cite{blip2_2023}`
(Li et al., ICML 2023) y `\cite{faiss2019}` (Johnson et al., IEEE
Trans. Big Data 2019). Las claves `\cite{panderm2025}`, `\cite{derm1m}`,
`\cite{dermfmzero2026}`, `\cite{dinov2}`, `\cite{biomedclip}`,
`\cite{sam2}`, `\cite{isic2018}`, `\cite{fitzpatrick17k}`,
`\cite{amie2024}` y `\cite{deepmind_aicoclinician}` ya estaban en la
bibliografía heredada del `tfg_uib_70pv2/Bibliografia.tex`.

**Acrónimos añadidos a `Acronims.tex` por el Cap. 2:** API, FAISS,
HNSW, InfoNCE, LLM, RAG, SigLIP, SOTA, VQA.

**Nota de incorporación post-cierre del Cap. 2:** revisión retrospectiva
del material previo (`tfg_uib_70pv2/Cap5_Derivadas.tex`
§\,\ref{sec:rag}; `tfg_uib_70pv2/Cap7_Prototipo.tex` §\,M4) identifica
que la recuperación visual densa con índice FAISS sobre los embeddings
DermLIP del corpus Derm1M es un componente operativo desarrollado en
el TFG. Se incorpora al § 2.3 del Cap.~2 como párrafo declarativo
sobre la implementación operativa de la recuperación cross-modal
(índices vectoriales FAISS y HNSW, latencias típicas), con la
distinción explícita entre recuperación visual densa y el patrón RAG
en sentido estricto (que requiere acoplamiento con un modelo de
lenguaje generativo). Se añade la referencia `\cite{faiss2019}` a la
bibliografía y los acrónimos FAISS, HNSW y RAG a la lista. No se
incorpora detalle adicional al Cap.~1; el bloque derivado de
recuperación visual densa ya figura mencionado en el § 1.5 (párrafo
final sobre bloques derivados) y en el § 1.7 (descripción del cap.~6).
La caracterización experimental completa de este componente
(densidad anómala del espacio Derm1M, atractor semántico del
granuloma piogénico, mitigaciones con escalado de temperatura y
z-score por consulta, integración como módulo M4 del prototipo)
corresponde a los capítulos 5 y 6 de la nueva memoria.

---

## Capítulos pendientes

Las filas se añaden en las fases siguientes (Fase 4 a Fase 9). Cualquier
nueva cifra que se introduzca debe quedar registrada aquí antes de
considerar cerrada la fase correspondiente.

| Cap. | Estado | Fase |
|---|---|---|
| 2 · Estado del arte | **cerrado** | Fase 3 |
| 3 · Datos y ontología (DermapixelAI 1.0) | **cerrado** | Fase 4 |
| 4 · Diseño experimental | **cerrado** | Fase 5 |
| 5 · Resultados y discusión | pendiente | Fase 6 |
| 6 · Caminos abiertos | pendiente | Fase 7 |
| 7 · Integración con DermApIxel | pendiente | Fase 8 |
| Resumen + revisión integrada | pendiente | Fase 9 |

---

## Capítulo 4 · Diseño experimental

Todas las cifras de este capítulo son **especificaciones de
diseño** (hardware, hiperparámetros, configuraciones), no resultados
experimentales. Los valores de rendimiento se reservan al cap. 5.

### Hardware y entorno de ejecución (§ 4.1)

| Cifra | Valor | Fuente |
|---|---|---|
| Equipo | NVIDIA DGX Spark, chip Grace Hopper GB10 | `tfg_uib_70pv2/Cap3_Maquinaria.tex:9`; `RESULTADOS_TFG.md:4` |
| Memoria unificada | 128 GB | ibid. |
| Arquitectura | aarch64 (ARM 64-bit) | ibid. |
| CUDA | 13.0 | ibid. |
| Precisión nativa | BF16 | `tfg_uib_70pv2/Cap3_Maquinaria.tex:11` |
| Python | 3.12.3 | `RESULTADOS_TFG.md:5` |
| PyTorch | 2.11.0 | ibid. |
| timm | 0.9.16 | ibid. |
| Modelos cargables simultáneamente en GPU | hasta ≈ 55 GB en BF16 | `tfg_uib_70pv2/Cap3_Maquinaria.tex:11` |
| Tiempo FT PanDerm Large HAM10000 (50ep, TTA) | ≈ 15 h | `tfg_uib_70pv2/Cap3_Maquinaria.tex:15` |
| Tiempo FT SAM2.1 ISIC2018 (50ep, LoRA) | ≈ 24 h | ibid. |
| Tiempo entrenamiento SAE Large (16 384 features) | ≈ 4 h | ibid. |
| Tiempo LP de un encoder por dataset | 1--3 min | derivado de `RESULTADOS_TFG.md:284`; `tfg_uib_70pv2/Cap3_Maquinaria.tex:15` |

### Modelos evaluados (§ 4.2)

| Modelo | Tamaño | Embedding | Origen / cita |
|---|---|---|---|
| PanDerm Base | ≈ 86 M params | 768 dim | `\cite{panderm2025}`; `tfg_uib_70pv2/Cap3_Maquinaria.tex:20` |
| PanDerm Large | ≈ 307 M params | 1 024 dim | ibid. |
| DINOv2 ViT-L/14 | ≈ 300 M params | 1 024 dim | `\cite{dinov2}` |
| ConvNeXt-Large | ≈ 198 M params | — | `tfg_uib_70pv2/Cap3_Maquinaria.tex:20` |
| EfficientNetV2-Large | ≈ 118 M params | — | ibid. |
| DermLIP v1 / v2 (PubMedBERT 256) | encoder visual PanDerm Base | — | `\cite{derm1m}`; `tfg_uib_70pv2/Cap3_Maquinaria.tex:24` |
| DermLIP original (GPT-2/CLIP 77) | encoder visual ViT-Base | — | `RESULTADOS_TFG.md:236` |
| BiomedCLIP | preentrenamiento ≈ 15 M pares | — | `\cite{biomedclip}` |
| SigLIP-Large SO400M | ≈ 878 M params | 1 152 dim | `\cite{siglip2023}`; memoria `project_ensemble_siglip` |
| SAM2.1-Large | ≈ 227 M params | máscara | `\cite{sam2}` |
| GPT-4o (OpenAI) | tamaño no público | API | — |
| Gemini 2.5 Pro (Google DeepMind) | tamaño no público | API | — |
| MedGemma 4B Vision (Google) | ≈ 4 mil M params | local | memoria `project_llm_providers` |
| MedGemma 27B Text (Google) | ≈ 27 mil M params | local BF16 | ibid. |
| BLIP-2 | arquitectura Q-Former | — | `\cite{blip2_2023}` |

### Hiperparámetros de los protocolos (§ 4.3 y § 4.4)

| Protocolo | Configuración | Fuente |
|---|---|---|
| LP — clasificador | LogisticRegression L-BFGS, L2, $C=1{,}0$, max_iter $5\,000$, `random_state=42` | `RESULTADOS_TFG.md:293`; memoria `project_fairness_5models` |
| FT — optimizador | AdamW, weight_decay $0{,}05$ | `RESULTADOS_TFG.md:107` |
| FT — learning rate | $5\times10^{-4}$ | ibid. |
| FT — scheduler | Cosine annealing + warmup 10 ep | ibid. |
| FT — layer decay | $0{,}65$ | `RESULTADOS_TFG.md:109` |
| FT — drop_path | $0{,}2$ | `RESULTADOS_TFG.md:110` |
| FT — label smoothing | $\epsilon = 0{,}1$ | `RESULTADOS_TFG.md:107` |
| FT — Mixup $\alpha$ | $0{,}8$ | ibid. |
| FT — CutMix $\alpha$ | $1{,}0$ | ibid. |
| FT — sampler | Weighted random sampler (1/freq) | `RESULTADOS_TFG.md:111` |
| FT — épocas | 50 | `RESULTADOS_TFG.md:103` |
| TTA — augmentaciones | 5 (flips H/V, rotación, color jitter) | `RESULTADOS_TFG.md:112`, `297` |
| Eficiencia etiquetas — submuestreos | 1 / 5 / 10 / 20 / 50 / 100 \% | `RESULTADOS_TFG.md:64--75` |
| Segmentación — optimizador | AdamW, lr $1\times10^{-4}$, weight_decay $0{,}05$ | `RESULTADOS_TFG.md:159` |
| Segmentación — batch | 4 | `RESULTADOS_TFG.md:163` |
| Segmentación — pérdida | CrossEntropy + Dice | `RESULTADOS_TFG.md:158` |
| Segmentación — épocas | 50 (referencia) y 100 (early stop) | `RESULTADOS_TFG.md:161,177,187` |
| Segmentación — LoRA rank | $r = 8$ | convención `peft` |
| Normalización ImageNet | $\mu=[0{,}485, 0{,}456, 0{,}406]$, $\sigma=[0{,}229, 0{,}224, 0{,}225]$ | `RESULTADOS_TFG.md:292` |
| Normalización segmentación | uniforme $(0{,}5, 0{,}5, 0{,}5)$ | ibid. |
| Normalización DermLIP | OpenAI CLIP | ibid. |
| Equidad Fitzpatrick17k — modelos | 5 (PanDerm L/B, DermLIP v2, DINOv2, BiomedCLIP) | memoria `project_fairness_5models` |
| Equidad — formulaciones | 114 patologías + 3 clases malignidad | ibid. |
| Equidad — subgrupos | 6 fototipos Fitzpatrick I-VI | ibid. |
| Ensemble safety — clasificadores | 3 (M1 = PanDerm L FT, M7 = unificado, SigLIP LP) | memoria `project_ensemble_siglip` |
| Ensemble safety — conjunto eval | HAM10000 test, 70 melanomas | ibid. |

### Reproducibilidad (§ 4.5)

| Cifra | Valor | Fuente |
|---|---|---|
| Seeds FT/segmentación (torch/numpy/random) | 0 | `RESULTADOS_TFG.md:291` |
| Seed LP/scikit-learn (`random_state`) | 42 | memoria `project_fairness_5models` |
| WANDB_MODE | disabled | `RESULTADOS_TFG.md:290` |
| CUDA_VISIBLE_DEVICES | 0 | ibid. |

**Referencias añadidas a `Bibliografia.tex` para el Cap. 4:**
ninguna nueva. Todas las claves citadas
(`panderm2025`, `derm1m`, `dinov2`, `biomedclip`, `siglip2023`,
`sam2`, `blip2_2023`, `isic2018`, `faiss2019`) ya estaban en la
bibliografía.

**Acrónimos añadidos a `Acronims.tex` por el Cap. 4:** AdamW, BF16,
CAE, DSC, IoU, L-BFGS, TTA.

---

## Capítulo 3 · Conjunto de datos y ontología

Las cifras de datasets externos se citan tal como se han registrado en
`RESULTADOS_TFG.md` (splits oficiales empleados en linear probing) y
en las publicaciones de cada dataset. Las cifras del corpus
DermapixelAI v3.1 provienen de
`research_post_tfg/reclassify_modality/POST_RECLASSIFICATION_REPORT.md`
y de `research_post_tfg/EDA_REPORT.md`. Las cifras de la ontología son
las del vocabulario canónico definido por el autor con revisión experta
de la Dra.~R.~Taberner.

### Cifras de los doce datasets externos (sección 3.1 y 3.2)

| Dataset | N test | Clases | Modalidad | Fuente |
|---|---:|---:|---|---|
| HAM10000 | 1 232 | 7 | Dermoscopia | `\cite{ham10000}` (Tschandl et al., Sci. Data 2018) |
| BCN20000 | 1 242 | 9 | Dermoscopia | `\cite{bcn20000}` (Combalia et al., arXiv 2019) |
| PAD-UFES-20 | 461 | 6 | Clínica móvil | `\cite{padufes}` (Pacheco et al., Data in Brief 2020) |
| DDI | 137 | 2 | Clínica diversa | `\cite{ddi}` (Daneshjou et al., Sci. Adv. 2022) |
| Dermnet | 4 002 | 23 | Clínica atlas | `\cite{dermnet}` (DermNet NZ Trust) |
| Derm7pt clínico | 168 | 2 | Clínica | `\cite{kawahara2019}` (Kawahara et al., IEEE JBHI 2019) |
| Derm7pt dermo | 225 | 2 | Dermoscopia | `\cite{kawahara2019}` |
| HIBA | 334 | 2 | Dermoscopia | Hospital Italiano de Buenos Aires (ISIC Archive) |
| MSKCC | 1 664 | 2 | Dermoscopia | Memorial Sloan Kettering Cancer Center (ISIC Archive) |
| WSI patches | 12 354 | 16 | Histopatología | Benchmark de evaluación (PanDerm) |
| ISIC2018 | 2 594 | binaria | Dermoscopia (segm.) | `\cite{isic2018}` (Codella et al., arXiv 2019) |
| Fitzpatrick17k | 16 577 | 114 + 6 FP | Clínica | `\cite{fitzpatrick17k}` (Groh et al., CVPR Workshops 2021) |
| SkinCon | 3 230 | 48 conceptos | Clínica | `\cite{skincon}` (Daneshjou et al., NeurIPS 2022) |

(Total: 12 datasets externos según la convención del trabajo, con
Derm7pt como una única entrada del corpus a pesar de sus dos variantes
clínica/dermatoscópica.)

### Cifras de la ontología jerárquica L1/L2/L3 (sección 3.3)

| Cifra | Valor | Fuente |
|---|---|---|
| Niveles de la ontología | 3 (L1 etiológico, L2 subcategoría, L3 diagnóstico) | Diseño autor + revisión Dra.~Taberner |
| L1 vocabulario completo | 4 (Patología inflamatoria, Patología tumoral, Patología infecciosa, Genodermatosis) | `tfg_uib_70pv2/Cap2_Datos.tex:96--105` |
| L2 vocabulario completo | 43 | `metadata/ontology.csv`; `EDA_REPORT.md` |
| L2 sin L3 asociado en el vocabulario | 5 (Esclerosis tuberosa, Neurofibromatosis tipo 1, Incontinentia pigmenti, Queratodermia palmo-plantar hereditaria, Pseudoxantoma elástico) | Inspección del fichero `metadata/ontology.csv` |
| L3 vocabulario completo | 367 | ibid. |
| Datasets externos mapeados a la ontología | 11 (todos los anteriores excepto SkinCon, que anota conceptos no diagnósticos) | `tfg_uib_70pv2/Cap2_Datos.tex:103` |
| Imágenes armonizadas tras el mapeo de los 11 datasets | 72 654 | `tfg_uib_70pv2/Cap2_Datos.tex:103`; `tfg_uib_70pv2/Cap5_Derivadas.tex:226` |

### Cifras de DermapixelAI v3.1 (secciones 3.4 y 3.5)

| Cifra | Valor | Fuente |
|---|---|---|
| Imágenes totales v3.1 | 1 089 | `POST_RECLASSIFICATION_REPORT.md:19` |
| Imágenes totales v3 (estado al cierre del TFG defendido) | 1 109 | `EDA_REPORT.md:32` |
| Casos catalogados en `cases.csv` | 698 | `EDA_REPORT.md:37` |
| Casos con al menos una imagen (v3.1) | 672 (de los 698) | ibid. |
| Casos huérfanos generados por la exclusión de las 20 not-derm | 3 | `POST_RECLASSIFICATION_REPORT.md` (Cap.~6) |
| Imágenes movidas de clinical a dermoscopy | 40 | ibid. (Cap.~1) |
| Imágenes excluidas a `images/_excluded/` | 20 | ibid. (Cap.~1) |
| Imágenes confirmadas en dermoscopy tras revisión visual (banderas amarillas) | 2 | ibid. (Cap.~1) |
| Distribución modalidad v3 → v3.1 (clinical) | 1 096 → 1 036 | ibid. (Cap.~1) |
| Distribución modalidad v3 → v3.1 (dermoscopy) | 9 → 49 | ibid. |
| Distribución modalidad v3.1 (histology · ultrasound · wood_lamp) | 2 · 1 · 1 | ibid. |
| Splits v3 → v3.1 (train) | 908 → 891 | ibid. (Cap.~5) |
| Splits v3 → v3.1 (val) | 160 → 157 | ibid. |
| Splits v3 → v3.1 (test) | 41 → 41 | ibid. |
| `case_id` con imágenes en más de un split | 0 (regla case-aware íntegra) | `EDA_REPORT.md` |
| `label_source = ontology` | 97,93 % | `EDA_REPORT.md:22` |
| `diagnosis_source = expert_v3` | 98,38 % | ibid. |
| `rosa_verified = True` | 82,96 % | ibid. |
| L1 efectivas en el corpus v3.1 | 4 | `EDA_REPORT.md:48`; `POST_RECLASSIFICATION_REPORT.md` |
| Distribución L1 v3.1 (inflamatoria · tumoral · infecciosa · genodermatosis · sin asignar) | 544 · 276 · 259 · 11 · 19 | ibid. |
| Porcentaje L1 v3.1 (inflamatoria) | 49,9 % | derivado |
| Porcentaje L1 v3.1 (tumoral) | 25,3 % | derivado |
| Porcentaje L1 v3.1 (infecciosa) | 23,8 % | derivado |
| Porcentaje L1 v3.1 (genodermatosis) | 1,0 % | derivado |
| Imágenes sin `ontology_l1` asignada (todas con `label_source = raw`) | 19 | `EDA_REPORT.md:51` |
| L2 efectivas en el corpus | 38 (39 raw con 2 variantes ortográficas de \emph{Trastornos queratinización}) | `EDA_REPORT.md:49` |
| L3 efectivas en el corpus v3.1 | 250 (de 367 del vocabulario; cobertura 68,1 %) | `EDA_REPORT.md:50`; `SAMPLING_REPORT.md:144` |
| L3 más frecuente | Psoriasis en placas, 38 imágenes | `EDA_REPORT.md` |
| Cola larga (L3 con $\le 5$ imágenes en `train`) | 178 | `EDA_REPORT.md:60` |
| Cola larga (L3 con 1 imagen en `train`) | 65 | ibid. |
| L2 sin representación en `val` | 11 | `EDA_REPORT.md:73--87` |
| L2 sin representación en `test` | 22 | ibid. |
| L1 sin representación en `test` | 1 (Genodermatosis) | ibid. |
| Longitud mediana de `case_text` | 223 palabras | `EDA_REPORT.md:126` |
| Cuartiles p25/p75 de `case_text` | 175 / 271 palabras | ibid. |
| Casos cuyo texto narrativo menciona "diagnóstico" o "diagnosticar" | 32 (4,6 %) | `EDA_REPORT.md:129` |
| Integridad técnica v3.1 (imágenes corruptas) | 0 | `EDA_REPORT.md:114` |
| Integridad técnica v3.1 (hashes MD5 discordantes tras la reclasificación) | 0 | `POST_RECLASSIFICATION_REPORT.md` |
| Cobertura temporal del corpus | 2011--2026, pico en 2016 | `EDA_REPORT.md:138` |

### Limitaciones del conjunto de datos (sección 3.6)

| Limitación | Cifras asociadas | Fuente |
|---|---|---|
| Solapamiento Derm1M | 3 datasets afectados (Dermnet, HIBA, MSKCC) | `INFORME_RECONOCIMIENTO.md` § 9 |
| Desbalance estructural por modalidad | ≈ 95 % clinical en v3.1 | derivado de `POST_RECLASSIFICATION_REPORT.md:19` |
| Cola larga | 178 L3 con $\le 5$ en `train` | `EDA_REPORT.md:60` |
| Cobertura ontológica | 250 / 367 L3 efectivas (68,1 %) | ibid. |
| L2/L1 sin cobertura en splits | 22 L2 sin test; 11 L2 sin val; 1 L1 sin test (Genodermatosis) | ibid. |
| Sesgo geográfico del material | 12 datasets externos mayoritariamente EE.UU., Australia, Europa central, Brasil | Síntesis propia |

**Referencias añadidas a `Bibliografia.tex` para el Cap. 3:**
`\cite{bcn20000}` (Combalia et al., arXiv:1908.02288). Todas las demás
referencias del capítulo (HAM10000, PAD-UFES, DDI, Dermnet, Derm7pt,
ISIC2018, Fitzpatrick17k, SkinCon, Derm1M, PanDerm) ya estaban en la
bibliografía heredada.

**Acrónimos añadidos a `Acronims.tex` por el Cap. 3:** BCN, CIE-10,
DDI, FP, HAM, HIBA, ISIC, MD5, MSKCC, PAD-UFES, SNOMED CT, WSI, ZS.

**Nota de creación del Anexo~E (post-cierre del Cap.~3):** se añade
un nuevo anexo *"Documento de entrega del corpus DermapixelAI 1.0"*
con formato \emph{Datasheet for Datasets}~\cite{datasheets2018}. El
anexo recoge identidad del dataset, procedencia y autoría compartida
(Contestí Coll \& Taberner, acuerdo formalizado por escrito en el
marco de la colaboración previa), licencia CC~BY-NC-SA~4.0, cita
recomendada en prosa y BibTeX, disponibilidad (plataforma pendiente
en la fecha de cierre del trabajo), datasheet con los siete bloques
estandarizados, uso responsable y limitaciones clínicas, privacidad
y consentimiento, y política de mantenimiento. Quedan separados los
dos niveles de documentación del corpus: el Anexo~C documenta el
proceso interno de construcción (pipeline + caracterización
cuantitativa); el Anexo~E documenta la entrega formal del dataset
como contribución pública. Se añade la referencia
`\cite{datasheets2018}` (Gebru et al., CACM 2021; arXiv:1803.09010)
a la bibliografía. Se actualiza la descripción de los anexos en el
§ 1.7 del Cap.~1.

**Nota de reorganización del Cap.~3 (post-cierre):** revisión
estructural posterior decide trasladar el detalle técnico y la
caracterización cuantitativa exhaustiva del corpus DermapixelAI 1.0
al anexo~\ref{anexo:pipeline}, y dejar en el cuerpo del Cap.~3
únicamente una descripción breve (sección~\ref{sec:dermapixel-summary})
con el mismo formato y nivel de detalle que el resto de datasets
descritos por familia en el § 3.2. Razón: el corpus propio no es
objeto de evaluación del trabajo (es contribución resultante);
mantenerlo en pie de igualdad con los datasets externos pero con dos
secciones dedicadas a su pipeline y caracterización rompía la
proporción del capítulo. Cambios derivados:

- Las secciones ``§ 3.4 Corpus DermapixelAI: origen y construcción''
  y ``§ 3.5 Caracterización de DermapixelAI 1.0'' del Cap.~3
  desaparecen; su contenido se traslada al anexo~\ref{anexo:pipeline}
  con la misma redacción.
- Se añade una nueva subsección breve
  ``§ 3.2.5 Corpus propio del trabajo: DermapixelAI 1.0'' (un
  párrafo) dentro del § 3.2 de datasets externos por familia.
- Las limitaciones del § 3.4 (antes § 3.6) se reorganizan: las
  limitaciones específicas del corpus propio (desbalance modalidad,
  cola larga, cobertura ontológica incompleta, splits parciales por
  subcategoría) se trasladan también al anexo~\ref{anexo:pipeline}.
  En el Cap.~3 quedan tres limitaciones del conjunto de datasets
  externos: solapamiento con Derm1M, sesgo geográfico y
  heterogeneidad de las taxonomías diagnósticas nativas.
- En el Cap.~1 (§ 1.7) se ajusta la descripción del Cap.~3 para
  reflejar que el corpus propio se introduce resumido en el cap. y
  que el detalle exhaustivo se desarrolla en el anexo~C.

**Nota de rebautizado del corpus propio (post-cierre del Cap. 3):**
el corpus DermapixelAI se denominaba internamente con versiones
sucesivas (v1, v2, v3, v3.1) que reflejaban las iteraciones del
pipeline durante la fase paralela al TFG. Para la memoria nueva se
adopta la denominación pública **DermapixelAI 1.0** como primera
versión estable y publicable del corpus, sin entrar en el detalle
de las iteraciones intermedias. Las cifras que la memoria reporta
para 1.0 coinciden con las que internamente correspondían a v3.1
(1\,089 imágenes, 1\,036 clinical + 49 dermoscopy + 2 histology + 1
ultrasound + 1 wood\_lamp, 672 casos con imagen, splits 891 / 157 /
41, 38 L2 efectivas, 250 L3 efectivas, 97{,}93\,\% `label\_source =
ontology`, 98{,}38\,\% `diagnosis\_source = expert\_v3`, 82{,}96\,\%
`rosa\_verified = True`). En consecuencia:

- Se elimina la subsección "Transición de v3 a v3.1" del Cap.~3 y
  se reescribe el pipeline (§3.4.2) como proceso iterativo paralelo
  al TFG que consolida la versión 1.0; el detalle de la operación
  de reclasificación de modalidad (40 imágenes movidas a
  dermoscopy, 20 excluidas como no dermatológicas, 3 casos
  huérfanos preservados en `cases.csv`) queda absorbido en el paso
  (iii) "Clasificación de modalidad" del pipeline.
- La tabla de modalidad (§3.5.1) pierde la columna de comparación
  v3/v3.1 y queda con una sola columna $N$.
- La tabla de splits (§3.5.5) pierde la columna v3 y queda con una
  sola columna $N$.
- Todas las menciones explícitas a "v3.1" en el Cap.~3 se sustituyen
  por "DermapixelAI 1.0" o por "el corpus" según convenga.
- En el Cap.~1 (§1.7) se actualiza la descripción del cap.~3 y de
  los anexos para citar "DermapixelAI 1.0" en lugar de "v3.1".
- Las cifras canónicas registradas en esta bitácora siguen siendo
  las de la versión 1.0 (= v3.1 interna); las entradas previas que
  citaban v3.1 explícitamente se interpretan ahora como referencia
  histórica al estado interno del corpus.
