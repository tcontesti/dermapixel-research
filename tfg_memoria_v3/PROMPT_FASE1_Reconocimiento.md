# Prompt — Fase 1 · Reconocimiento del proyecto previo a la reescritura de la memoria del TFG

> Pegar este prompt en una sesión nueva de Claude Code abierta en
> `C:\Users\tonic\Desktop\proyectos\panderm\`. Esta sesión NO escribe
> ningún capítulo del TFG. Su único cometido es leer todo lo previo,
> entenderlo y devolver una síntesis estructurada que servirá como
> punto de partida para la reescritura capítulo a capítulo en
> sesiones posteriores.

---

## Contexto y motivación de la reescritura

Existen cuatro versiones previas de la memoria del TFG y un volumen muy
considerable de documentación auxiliar generada durante el desarrollo. El
autor ha recibido feedback en dos direcciones opuestas:

- Las primeras versiones eran **demasiado extensas** (≈ 154 páginas en
  `tfg_uib/`).
- Las más recientes (`tfg_uib_70pv2/`, `tfg_uib_75p/`) son
  **demasiado narrativas**, con tono de profesor explicando, títulos en
  forma de pregunta, e información no estrictamente validada.

La reescritura busca una versión final en **tono académico de artículo
científico**: neutral, objetiva, sin sobrepromesa, con títulos
declarativos, y centrada en lo que efectivamente se ha realizado y
validado. El alumno desarrollador ya no es el protagonista; lo es el
trabajo realizado.

## Reglas de tono y estilo que regirán la nueva memoria

1. **Tono académico, super aséptico.** Frases declarativas, voz pasiva
   o impersonal. Sin "queremos hacer", "vamos a ver", "como veremos a
   continuación", "es importante destacar", "interesante", "notable".
   Sin juicios de valor sobre el propio trabajo. El registro es el de
   un artículo científico, no el de un libro divulgativo.
2. **Títulos declarativos**, nunca interrogativos. *No*: "¿Cómo se
   evalúa el sesgo en piel oscura?". *Sí*: "Evaluación del sesgo por
   fototipo en Fitzpatrick17k".
3. **Información validada únicamente.** Cualquier cifra, hallazgo o
   afirmación que no esté respaldada por un experimento ejecutado en
   este proyecto, por un log existente, por un commit, o por una cita
   externa publicada se omite. Si es imprescindible mencionar algo no
   validado (p. ej. proyección), se marca explícitamente como
   "estimación no validada" o "trabajo previsto".
4. **DermApIxel no es el protagonista.** Es un trabajo previo del autor
   y la futura base de despliegue. El objeto del TFG es **desarrollar
   y caracterizar un modelo fundacional para dermatología clínica**;
   DermApIxel se menciona en antecedentes y se mencionará como destino
   de despliegue en el capítulo final.
5. **No se compite con PanDerm ni con ningún modelo fundacional
   existente.** Se hace una revisión del estado del arte para
   caracterizar lo disponible y se identifican brechas operativas
   (idioma castellano, dominio clínico específico, equidad por
   fototipo, integración hospitalaria). El TFG aporta evaluación
   empírica sobre un dominio propio, no un modelo nuevo.
6. **El dataset propio es el dominio del trabajo.** El conjunto
   DermapixelAI v3.1 es el aporte sustantivo: lo que el TFG sabe
   caracterizar, lo que permite reevaluar el estado del arte y lo que
   habilita los experimentos. El capítulo de datos no es un detalle de
   apéndice sino el eje del trabajo.
7. **Lenguaje sobre el experimento**: evitar la palabra "replicación"
   (sugiere reproducir un resultado ajeno y no es lo que se hace en
   este TFG). Usar "experimentación", "evaluación empírica", "estudio
   experimental", "comparación sobre dominio propio" según convenga.
8. **Resumen de una sola página** (≈ 250-300 palabras).
9. **Castellano académico**, sin emojis, sin jerga anglosajona
   innecesaria. Tecnicismos en inglés sólo cuando no exista
   equivalente consolidado (foundation model, dermoscopy, embedding).
10. **Estructura objetivo, secuencial: trabajo previo → evaluación de
    lo existente → caminos diferentes a explorar**:

    | Cap | Título tentativo                                                      | Páginas |
    |-----|-----------------------------------------------------------------------|---------|
    | —   | Resumen                                                               | 1       |
    | 1   | Introducción y antecedentes                                           | 4-6     |
    | 2   | Estado del arte                                                       | 6-9     |
    | 3   | Conjunto de datos y ontología                                         | 8-12    |
    | 4   | Diseño experimental (modelos, protocolos, métricas)                   | 8-12    |
    | 5   | Resultados y discusión                                                | 10-14   |
    | 6   | Caminos y trabajo por hacer                                           | 3-5     |
    | —   | Bibliografía + anexos                                                 | sin lím |

    Páginas tentativas: 40-60 sin contar anexos.

11. **El capítulo 1 (Introducción) NO contiene líneas futuras ni
    proyecciones**. Sólo motivación, antecedentes (incluido DermApIxel
    como trabajo previo del autor) y objetivos concretos del TFG. La
    discusión sobre lo que queda por hacer pertenece al capítulo 6.
12. **El capítulo 4 (Diseño experimental) describe explícitamente**:
    los modelos comparados (PanDerm Large, DermLIP v2, SigLIP LP,
    BiomedCLIP, BLIP-2, etc.), los protocolos seguidos en cada
    experimento (linear probing, zero-shot, fine-tuning, fairness por
    fototipo, etc.), y las métricas usadas (accuracy, BAcc, F1-macro,
    AUROC, recall por subgrupo, latencia). No mezclar resultados aquí;
    sólo cómo se ha medido.
13. **El capítulo 5 (Resultados y discusión) integra ambas partes**:
    cada resultado experimental se presenta con su métrica y su
    intervalo de confianza, y a continuación se discute brevemente su
    interpretación, los caveats y las comparaciones internas. La
    discusión no es un capítulo aparte sino la sección que cierra cada
    bloque de resultados.
14. **El capítulo 6 (Caminos y trabajo por hacer) lista honestamente**:
    lo iniciado y no concluido en el TFG (anotación de Rosa Taberner,
    fine-tuning SpanDerm, solicitud CEIC HUSLL), los caminos
    identificados pero no recorridos (federated learning, capa
    agéntica, validación clínica prospectiva), y el plan de
    integración con DermApIxel como producto. Se evita el cierre
    grandilocuente; cada camino lleva su pre-requisito y su grado de
    madurez actual.
15. **Capítulo de resultados es decisivo.** Solamente lo que se ha
    obtenido empíricamente, con métrica e intervalo o caveat. Cero
    claims sin medición. Tablas y figuras con caption autocontenido.
16. **Capítulo de datos es decisivo.** Caracterización exhaustiva de
    DermapixelAI v3.1 (1.089 imágenes, 49 dermo, ontología jerárquica
    4/38/250 efectivos), las versiones previas (v3.0), los datasets
    externos usados (HAM10000, Fitzpatrick17k, ISIC, Derm1M, SkinCon,
    según se haya hecho) y la trazabilidad completa de cómo se
    construyeron, anotaron y particionaron.

## Cometido específico de esta sesión (Fase 1)

Esta sesión **no escribe capítulos**. Su única salida es un documento de
síntesis llamado `tfg_memoria_v3/INFORME_RECONOCIMIENTO.md` que sirva
como base sólida para las sesiones siguientes (Fase 2 = capítulo 1,
Fase 3 = capítulo 2, etc., una por capítulo).

### Documentos a revisar

Ordenados por prioridad de lectura:

**Bloque A · Versiones previas de la memoria** (lectura comparativa, no
para copiar):

- `tfg_uib_75p/MemoriaTFG.pdf` y `tfg_uib_75p/*.tex` — versión más
  reciente, 4063 líneas. Identificar fortalezas a conservar y debilidades
  a corregir (tono novelado, títulos en pregunta).
- `tfg_uib_70pv2/MemoriaTFG.pdf` y `tfg_uib_70pv2/*.tex` — variante
  narrativa intermedia.
- `tfg_uib_70p/*.tex` — primera versión condensada 70p (978 líneas).
- `tfg_uib/MemoriaTFG.pdf` — versión extensa inicial (154 pág, 3633
  líneas). Útil para localizar contenido que se perdió en las
  versiones condensadas y puede ser canónico.

Por cada versión, anotar en el informe:
- Estructura de capítulos (índice).
- Cifras cuantitativas mencionadas (extraerlas todas a una tabla).
- Frases o párrafos con tono inapropiado (preguntas como título,
  hipérboles, primera persona excesiva). Listar muestras.

**Bloque B · Documentación auxiliar consolidada en la raíz del proyecto**:

- `DOCUMENTACION_TFG.md`, `TFG_MEMORIA.md`, `RESULTADOS_TFG.md` —
  documentos resumen previos.
- `ARCHITECTURE.md`, `ROADMAP.md`, `DEPLOYMENT.md`, `DATASETS_DERMATOLOGIA.md`, `DATASETS_ROADMAP.md` — contexto
  arquitectónico y plan.
- `AUDIT_REPORT.md`, `CODE_REVIEW.md`, `REVISION_CODIGO.md`,
  `DOC_REVIEW.md`, `TFG_REVIEW.md` — revisiones críticas previas (útil
  para no repetir errores).
- `COMPARATIVA_PAPER.md`, `SAE_DEEP_REVIEW.md`, `DERMFM_ZERO_COMPLETO.md`,
  `DERMFM_EVAL.md`, `UNIFIED_TRAINING_PLAN.md` — bloques temáticos
  específicos.
- `Segmentation.md` — descartar como bloque (no es eje del TFG).

**Bloque C · Investigación post-TFG** (`research_post_tfg/`):

- `EDA_REPORT.md` — caracterización exhaustiva v3 (cifras canónicas).
- `reclassify_modality/AUDIT_MODALITY_REPORT.md` y
  `POST_RECLASSIFICATION_REPORT.md` — transición v3 → v3.1.
- `sampling/SAMPLING_REPORT.md` — diseño del muestreo de 200 para Rosa.
- Notebooks y scripts asociados (no leer línea a línea, sólo conocer su
  existencia y cometido).

**Bloque D · Memoria persistente del proyecto** (sólo lectura del índice):

- `C:\Users\tonic\.claude\projects\C--Users-tonic-Desktop-proyectos-panderm\memory\MEMORY.md` —
  cada entrada es un puntero a un fichero hermano; leer el índice y los
  ficheros `project_*` para conocer las decisiones de diseño tomadas
  durante el desarrollo. Especialmente:
  - `project_tfg_70pv2_state_2026_05_09.md`
  - `project_dermapixel_v3_1.md`
  - `project_eda_dermapixel_v3.md`
  - `project_sampling_rosa_200.md`
  - `project_spanderm_design_decision_2026_05_23.md`
  - `project_post_tfg_research_kickoff_2026_05_22.md`

## Qué tiene que contener `INFORME_RECONOCIMIENTO.md`

Documento estructurado en las secciones siguientes. Castellano académico,
sin emojis, sin opiniones personales.

### 1 · Inventario versionado de las cuatro memorias previas

Tabla con: ruta · líneas .tex · páginas PDF · fecha de modificación ·
índice de capítulos resumido en una línea cada uno · estado (activo /
referencia / descartado).

### 2 · Estructura comparada de los índices

Tabla cruzada mostrando qué capítulo equivalente tiene cada versión.
Identificar capítulos que aparecen y desaparecen, y proponer la unión
mínima que conserva todo el contenido esencial.

### 3 · Cifras consolidadas y validadas

Recopilar **todas las cifras cuantitativas** que aparezcan en las
distintas versiones y en los informes post-TFG, y clasificarlas en tres
columnas:

- **Sólidas**: respaldadas por experimento, log, commit o referencia
  externa.
- **Frágiles**: aparecen en la memoria sin trazabilidad clara, o con
  variantes contradictorias entre versiones.
- **Descartadas**: cifras que se sabe que cambiaron (p. ej., 9 vs 49
  dermatoscopias antes y después de la reclasificación v3.1).

Cada cifra debe llevar su fuente exacta (fichero + sección).

### 4 · Catálogo de afirmaciones no validadas

Listado de claims encontrados en las versiones previas que NO están
respaldados por datos en este proyecto: hipérboles, comparaciones con
modelos externos sin haberlos ejecutado, generalizaciones clínicas
indebidas. Estas afirmaciones se eliminarán o reescribirán en la versión
nueva.

### 5 · Glosario de tono inapropiado

Muestras concretas (cita textual + fichero + línea aproximada) de:

- Títulos en forma de pregunta.
- Primera persona excesiva o tono de profesor.
- Hipérboles, juicios de valor, comparativas no objetivas.
- Información especulativa presentada como certeza.

Esto sirve de calibración negativa para la reescritura.

### 6 · Material reutilizable

Identificar bloques de texto (párrafos enteros, no copiar) de las
versiones anteriores que cumplen el tono académico buscado y pueden
servir como base. Citar ruta + líneas + tema.

### 7 · Propuesta de estructura para la nueva memoria

Índice detallado capítulo por capítulo, con:
- Título declarativo (no en pregunta).
- Resumen de 2-3 líneas sobre qué contendrá.
- Páginas estimadas.
- Dependencias con otras secciones.
- Origen del material (qué versión previa o qué documento
  post-TFG aporta el contenido base).

La estructura objetivo es la definida en la regla 10 (sección de tono).
Recordatorio sintético:

| Cap | Título tentativo                                                      | Páginas |
|-----|-----------------------------------------------------------------------|---------|
| —   | Resumen                                                               | 1       |
| 1   | Introducción y antecedentes                                           | 4-6     |
| 2   | Estado del arte                                                       | 6-9     |
| 3   | Conjunto de datos y ontología                                         | 8-12    |
| 4   | Diseño experimental (modelos, protocolos, métricas)                   | 8-12    |
| 5   | Resultados y discusión                                                | 10-14   |
| 6   | Caminos y trabajo por hacer                                           | 3-5     |
| —   | Bibliografía + anexos                                                 | sin lím |

Páginas totales tentativas: **40-60**, sin contar anexos. La narrativa
es secuencial y aséptica: **trabajo previo → evaluación de lo
existente sobre dominio propio → caminos diferentes a explorar**. Nada
de proyecciones en la introducción; nada de juicios de valor en los
resultados; el cierre del documento se concentra en el capítulo 6.

### 8 · Datos a destacar en el capítulo de datasets

Caracterización resumida de cada dataset usado, marcando claramente la
diferencia entre conjuntos propios (DermapixelAI v3 / v3.1) y externos
(HAM10000, Fitzpatrick17k, ISIC, etc.). Por cada dataset: origen,
tamaño, modalidad, distribución por clases, licencia, uso concreto en
el TFG.

### 9 · Resultados a destacar en el capítulo de resultados

Listado priorizado de los resultados experimentales con métrica y
caveat. Por cada uno: experimento, modelos comparados, métrica
principal, valor obtenido, intervalo de confianza si existe, dataset de
evaluación, fuente del log.

### 10 · Caminos y trabajo por hacer (material para el capítulo 6)

Listado para alimentar el capítulo 6 final. Tres columnas:

- **Iniciado y no concluido en el TFG**: anotación conceptual con la
  Dra. Taberner, fine-tuning SpanDerm sobre v3.1, solicitud CEIC para
  banco HUSLL, etc. Indicar grado de madurez (porcentaje de avance o
  artefacto entregado).
- **Identificado y no abordado**: federated learning entre hospitales
  de Baleares, capa agéntica con LLM clínico, validación clínica
  prospectiva, evaluación multilingüe del estado del arte, etc.
  Indicar pre-requisito necesario (datos, CEIC, infraestructura).
- **Integración con DermApIxel**: descripción seca del puente entre el
  modelo fundacional caracterizado en el TFG y el prototipo
  hospitalario existente. Sin grandilocuencia: qué módulo entra dónde
  y bajo qué supuestos técnicos.

El capítulo 6 cierra el documento sin sobrepromesa. Cada camino llega
con su pre-requisito explícito y su grado de avance actual. No es un
listado de buenas intenciones sino un inventario de trabajo identificado.

## Reglas operativas para esta sesión

1. **No escribir capítulos.** Sólo el informe.
2. **No abrir el PDF de las versiones previas** si se puede extraer el
   índice y el contenido necesario de los ficheros `.tex`. Si hace
   falta abrir un PDF, hacerlo con `Read` paginado y sólo páginas
   concretas (índice, capítulos puntuales).
3. **Cero opinión personal** en el informe. Si una afirmación es
   especulativa, marcarla como tal.
4. **Trazabilidad estricta.** Cada hallazgo del informe debe incluir
   ruta del fichero y línea o sección donde se encontró.
5. **Cuando se detecten contradicciones entre versiones**, listarlas
   sin resolverlas (la resolución es trabajo del autor, no del LLM).
6. **CPU only, sin acceso a Spark, sin lanzar nada.**
7. **Castellano académico**, sin emojis.

## Output esperable

```
tfg_memoria_v3/
├── PROMPT_FASE1_Reconocimiento.md         (este fichero)
└── INFORME_RECONOCIMIENTO.md               (entregable, 10 secciones)
```

Tras esta sesión, el autor revisará `INFORME_RECONOCIMIENTO.md` y
decidirá ajustes antes de pasar a Fase 2 (escritura del Resumen y
Capítulo 1).

## Resumen final esperado al cierre

8-10 líneas con:

- Número de versiones previas revisadas y su estado.
- Páginas del PDF más reciente analizado.
- Número total de cifras cuantitativas recopiladas (sólidas /
  frágiles / descartadas).
- Número de claims no validados identificados.
- Hallazgo principal sobre contradicciones entre versiones, si lo hay.
- Confirmación de que el índice propuesto sigue la estructura clásica
  académica y respeta las reglas de tono.
- Cualquier punto que requiera decisión del autor antes de Fase 2.
