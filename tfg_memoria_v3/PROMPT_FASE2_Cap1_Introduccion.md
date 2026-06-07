# Prompt — Fase 2 · Redacción del Capítulo 1 "Introducción y antecedentes"

> Pegar en una sesión nueva de Claude Code abierta en
> `C:\Users\tonic\Desktop\proyectos\panderm\`. Esta sesión redacta
> únicamente el Capítulo 1 de la nueva memoria. No escribe el Resumen
> (se redacta en la Fase 9 cuando todos los capítulos estén cerrados),
> no escribe el Capítulo 2 ni ningún otro material.

---

## Posición en el plan de fases

```
[ Fase 1 · Reconocimiento ]                       hecho (INFORME_RECONOCIMIENTO.md)
[ Fase 2 · Cap 1 Introducción y antecedentes ]    ← esta sesión
  Fase 3 · Cap 2 Estado del arte
  Fase 4 · Cap 3 Datos y ontología (v3.1)
  Fase 5 · Cap 4 Diseño experimental
  Fase 6 · Cap 5 Resultados y discusión
  Fase 7 · Cap 6 Caminos abiertos
  Fase 8 · Cap 7 Integración con DermApIxel
  Fase 9 · Resumen + revisión integrada + bibliografía consolidada
```

## Inputs canónicos heredados

- `tfg_memoria_v3/PROMPT_FASE1_Reconocimiento.md` — reglas de tono 1-17.
- `tfg_memoria_v3/INFORME_RECONOCIMIENTO.md` — material previo
  sintetizado, cifras consolidadas, glosario de tono inapropiado,
  estructura propuesta.
- `tfg_uib_70pv2/Introduccio.tex:1-51` — material base del cap. 1 a
  reescribir, no a copiar.

## Decisiones bloqueantes consolidadas tras Fase 1

Se incorporan como restricciones de redacción de este capítulo y de
todos los siguientes.

1. **Versión del dataset citada**: **DermapixelAI v3.1** (1.089 imágenes,
   1.036 clinical + 49 dermoscopy + 2 histology + 1 ultrasound + 1
   wood_lamp). La transición v3 → v3.1 se describe en el capítulo 3,
   no aquí.
2. **Título de la portada y del trabajo**: *"Evaluación de modelos
   fundacionales para Dermatología Clínica"*. La nueva memoria
   abandona el título *"DermApIxel: modelo fundacional para
   dermatología clínica"* que figuraba en `tfg_uib_70pv2`.
3. **Tratamiento del prototipo DermApIxel**: capítulo 7 separado con
   título declarativo nuevo (p. ej. *"Integración del modelo en el
   entorno operativo: prototipo DermApIxel"*). En el cap. 1 se cita
   como antecedente del autor, sin describir su arquitectura ni
   sus métricas.
4. **Giro Rosa**: la sesión presencial con la Dra. R. Taberner sobre
   razonamiento diagnóstico real **no aparece en el Resumen**. En el
   cap. 1 se menciona el hecho factual de la colaboración (curso
   formativo, definición de 34 conceptos) como antecedente; la
   discusión sobre cómo ese hecho desplaza el horizonte del trabajo
   hacia paradigmas agénticos se desarrolla en el cap. 6 (Caminos
   abiertos), no aquí.

## Reglas heredadas de Fase 1 (recordatorio compacto)

1. Tono académico, **super aséptico**. Sin "queremos hacer", "vamos a
   ver", "el lector acompaña", "como veremos a continuación", "es
   importante destacar", "interesante", "notable", "una idea que
   conviene anunciar".
2. **Títulos declarativos**, nunca interrogativos ni narrativos. No:
   "La pregunta concreta", "La grieta", "La revelación", "La afirmación
   dura". Sí: "Objetivos del trabajo", "Pregunta de investigación".
3. Información validada únicamente. Cifras con trazabilidad explícita
   o cita publicada.
4. DermApIxel = trabajo previo del autor + futura base de despliegue.
   No es el objeto del TFG.
5. No se compite con PanDerm. Se caracteriza el estado del arte y se
   identifican brechas operativas.
6. DermapixelAI v3.1 es el dominio del trabajo (regla 6 Fase 1).
7. Sin "replicación" en títulos ni en encabezados. Usar
   "experimentación", "evaluación empírica", "estudio experimental".
8. Castellano académico, sin emojis, sin jerga anglosajona
   innecesaria. Tecnicismos en inglés solo cuando no exista
   equivalente consolidado.
9. Resumen del cap. 1 anclado a hechos. Sin proyecciones.
10. **Cap. 1 NO contiene líneas futuras ni proyecciones** (regla 11
    Fase 1). Cualquier mención prospectiva se desplaza a cap. 6.
11. **Paja cero, contenido suelto** (regla 17 Fase 1). Cada párrafo
    aporta al menos uno de: una cifra medida, una decisión
    metodológica trazable, una observación experimental, una
    limitación cuantificada, una referencia bibliográfica con anclaje
    específico. Si un párrafo no cumple ninguno, se elimina aunque ya
    estuviera escrito en el material previo.

## Cometido específico de esta sesión

Redactar el contenido completo del Capítulo 1 de la nueva memoria, en
LaTeX, listo para incorporar al documento maestro. Páginas indicativas
**5-7** del cuerpo (sin contar figuras grandes si las hubiera).
Lectura del rango:

- Si el capítulo cierra **por debajo de 5 páginas**, es señal de que
  falta sustancia (revisar contenido obligatorio § 5).
- Si rebasa **7 páginas**, podar redundancia con el material previo
  (la lista de espera, la integración con IB-Salut, el blog de
  Dermapixel suelen reiterarse en versiones anteriores).

## Estructura propuesta del Capítulo 1

Numeración de secciones tentativa. Los títulos son declarativos,
ningún signo de interrogación, ningún sustantivo abstracto solitario
("la grieta", "la revelación", "la pregunta concreta").

### 1.1 · Contexto sanitario y diagnóstico dermatológico asistido

- Encuadre del problema: lista de espera de teledermatología en Son
  Llàtzer (HUSLL) y derivación desde atención primaria por imagen
  fotográfica. Cifra de archivo de imágenes dermatológicas no
  estructuradas (> 300 000, `tfg_uib_70pv2/Introduccio.tex:18`).
- Impacto del retraso diagnóstico en melanoma como justificación
  clínica (supervivencia I → IV).
- Rol previsto de los modelos fundacionales: apoyo al cribado, no
  sustitución del razonamiento dermatológico.

### 1.2 · Antecedentes del proyecto Dermapixel

- Blog Dermapixel: 15+ años de actividad altruista por la Dra. R.
  Taberner, dermatóloga clínica del HUSLL. Archivo de > 700 casos
  comentados con imagen clínica, dermoscopia (si procede), historia y
  diagnóstico.
- Colaboración previa entre el autor y la Dra. Taberner en el marco de
  un proyecto institucional del IB-Salut sobre teledermatología.
- Hecho factual de la sesión formativa con la Dra. Taberner sobre
  razonamiento diagnóstico melanocítico vs no melanocítico, con
  consecuencia tangible: definición de 34 conceptos clínicos
  (16 dermatoscópicos + 8 distribución + 10 forma/color/textura) que
  articularán el bloque de interpretabilidad de los capítulos 4 y 5.
  **Sin proyectar implicaciones futuras del curso** (eso va al cap. 6).

### 1.3 · Trabajo previo del autor: el prototipo DermApIxel

- Mención del prototipo DermApIxel como aplicación clínica desarrollada
  por el autor previamente al TFG y desplegada en producción local el
  2026-04-12 (`MEMORY.md` `project_dermapixel_production_status`).
- Posición del prototipo en el trabajo: **base de despliegue** para los
  módulos derivados del TFG, no objeto del TFG. La caracterización
  arquitectónica completa se desarrolla en el cap. 7.
- Esta sección debe ser **breve** (un párrafo, máximo dos). No
  enumera los 8 módulos ni describe la pila tecnológica; eso es
  cap. 7.

### 1.4 · Modelos fundacionales en dermatología: contexto inmediato

- Encuadre del giro reciente de la disciplina hacia modelos
  fundacionales: encoders visuales auto-supervisados (PanDerm,
  Yan et al. 2025), modelos vision-lenguaje contrastivos (Derm1M y
  familia DermLIP), modelos integrados visión-lenguaje con zero-shot
  nativo (DermFM-Zero, sin pesos públicos en la fecha de cierre del
  trabajo).
- Esta sección **no es el estado del arte**; el desarrollo completo
  por familias y comparativas se reserva al cap. 2. Aquí se introduce
  el porqué del marco de trabajo elegido (PanDerm + DermLIP como
  modelos con código y pesos públicos), pero sin entrar en cifras
  comparativas.

### 1.5 · Objetivos del trabajo

Redactados en presente de indicativo, declarativos, **sin pregunta
retórica**. Tres bloques operativos:

- **O1 · Evaluación empírica del estado del arte sobre dominio
  propio.** Aplicar los protocolos estándar de la literatura (linear
  probing, fine-tuning supervisado, segmentación, zero-shot
  multimodal, comparación con modelos generalistas) sobre los modelos
  con código y pesos públicos, sobre datasets canónicos y sobre el
  corpus propio del autor (DermapixelAI v3.1).
- **O2 · Caracterización del corpus propio y de su ontología.**
  Construir, depurar y publicar internamente DermapixelAI v3.1, con
  una ontología jerárquica L1/L2/L3 validada por revisión experta;
  documentar la trazabilidad del corpus, su distribución y sus
  limitaciones.
- **O3 · Integración en un sistema operativo.** Demostrar que los
  módulos derivados del TFG son integrables en un prototipo clínico
  funcional (DermApIxel), entendido como vehículo de despliegue y no
  como contribución académica del trabajo. Detalle en el cap. 7.

### 1.6 · Alcance y restricciones del trabajo

- Cinco frentes experimentales: replicación con LP/FT, segmentación
  con SAM2.1, evaluación cruzada en el set downstream de Derm1M,
  zero-shot multimodal, comparación con LLMs generalistas (GPT-4o,
  Gemini, MedGemma).
- Cinco derivadas: ontología y clasificador unificado, ensemble de
  seguridad para melanoma, equidad por fototipo en Fitzpatrick17k,
  interpretabilidad con SAE + Concept Bottleneck, recuperación visual
  densa sobre Derm1M.
- Restricciones explícitas: hardware no estándar (DGX Spark
  NVIDIA GB10 Grace Hopper, sistema aarch64); datasets internos del
  grupo de Monash no accesibles; pesos de DermFM-Zero no públicos a
  la fecha de cierre.
- Lo que el TFG **no aborda**: entrenamiento de un modelo fundacional
  propio desde cero; validación clínica prospectiva; integración
  PACS hospitalaria operativa; reentrenamiento multilingüe. Estos
  elementos figuran en el cap. 6 como caminos identificados.

### 1.7 · Estructura del documento

- Una página o media, descripción seca capítulo por capítulo (1-7) y
  anexos A-D. **Sin recurso retórico** del tipo "el documento está
  dispuesto para leerse en orden" o "el lector acompaña". Frase
  declarativa.

## Contenido vetado en el Capítulo 1

- Cualquier formulación prospectiva ("la línea principal de
  continuación", "abre el camino hacia", "se proyecta hacia").
- Cualquier valoración del propio trabajo ("apuesta deliberada",
  "decisión inesperada", "consecuencia inesperada", "comparación
  incómoda pero inevitable").
- Descripción detallada del prototipo DermApIxel (módulos M1-M8,
  arquitectura técnica, métricas operativas). Eso es cap. 7.
- Cifras de resultados (FT 0,919 acc, BAcc 0,852, AUROC 0,978, etc.).
  Eso es cap. 5.
- Tablas comparativas de modelos. Eso es cap. 2 (estado del arte)
  y cap. 5 (resultados).
- Discusión sobre el atractor semántico del granuloma piogénico,
  Sparse Autoencoders, RAG visual. Eso es cap. 5.
- El "curso de la Dra. Taberner reorientó cómo había que aplicar la
  replicación" (`Introduccio.tex:13`). Hecho factual sí (curso
  formativo, 34 conceptos derivados); juicio sobre la reorientación,
  no.
- Cualquier mención a "la línea de inteligencia artificial agéntica"
  como horizonte. Eso es cap. 6.

## Material base: notas de qué eliminar de `Introduccio.tex:1-51`

| Línea | Contenido | Tratamiento |
|---|---|---|
| 4-9 | Sección "Dermapixel" con párrafo de apertura novelado | Reescribir aséptico. Contenido (blog + Dra. Taberner + colaboración IB-Salut) se conserva en sección 1.2 de la nueva estructura. |
| 13 | Párrafo sobre "consecuencia inesperada", "curso presencial individualizado" y reorientación hacia paradigmas agénticos | **Desplazar** la parte de "reorientación" al cap. 6. Conservar como hecho factual: existió un curso formativo con la Dra. Taberner que dio lugar a la definición de 34 conceptos. |
| 15-24 | Sección "La lista de espera de teledermatología" con tres párrafos | Conservar contenido en sección 1.1 + 1.2 nueva, eliminando vocativos ("una idea que conviene anunciar"). |
| 22-24 | Pasaje extenso sobre "imagen + texto + contexto" como vertebración del trabajo | Comprimir a un párrafo: el corpus DermapixelAI se construye como tripletas (imagen, texto clínico, diagnóstico) por decisión de diseño; la explotación experimental del componente lingüístico se acota a DermLIP y se acota a cap. 5. Sin dejar caer "la tensión recorre, en segundo plano, todo el documento". |
| 26-37 | Sección "Los modelos fundacionales aparecen en escena" | Reducir a un párrafo o dos (sección 1.4 nueva). El desarrollo extenso del estado del arte va al cap. 2. |
| 39-46 | Sección "La pregunta concreta" con cinco frentes y seis derivadas | Reformular como sección 1.5 (Objetivos) + sección 1.6 (Alcance), con tres objetivos operativos declarativos y la enumeración de los cinco frentes + cinco derivadas (no seis: `MEMORY.md` no documenta el sexto hilo independiente del corpus). |
| 48-51 | Sección "Estructura del documento" | Conservar como sección 1.7. Eliminar la metáfora "está dispuesto para leerse en orden". |

## Fuentes adicionales que se pueden citar en el cap. 1

- `MEMORY.md` `project_dermapixel_production_status` (despliegue prototipo 2026-04-12).
- `project_sampling_rosa_200.md` (34 conceptos clínicos resultado de la sesión formativa con la Dra. Taberner).
- Referencia bibliográfica `\cite{panderm2025}` (Yan et al. Nature Medicine).
- Referencia bibliográfica `\cite{derm1m}` (Yan et al. Derm1M + DermLIP).
- Referencia bibliográfica `\cite{dermfmzero2026}` (DermFM-Zero; pesos no liberados).

## Salidas esperadas

```
tfg_memoria_v3/
├── PROMPT_FASE2_Cap1_Introduccion.md         (este fichero)
└── Cap1_Introduccion.tex                      ← entregable principal
```

Adicional: actualizar `tfg_memoria_v3/BITACORA_CIFRAS.md` (crear si no
existe). Una fila por cada cifra citada en este capítulo con
columnas:

```
| cifra | valor | cap. + sección | fuente primaria | fecha de la fuente |
```

Esto sirve como bitácora de trazabilidad para que las fases siguientes
no introduzcan contradicciones numéricas.

## Reglas operativas para esta sesión

1. **Sólo redactar el Cap. 1.** No tocar otros capítulos, no escribir
   el Resumen, no crear el Cap. 2 o el Cap. 7 ni esbozar nada de
   ellos.
2. **No modificar `INFORME_RECONOCIMIENTO.md` ni `PROMPT_FASE1_*`.**
   Son la línea base estable.
3. **Compilar mentalmente, no en LaTeX.** No es necesario verificar
   que el `.tex` compila en esta sesión; la integración con el
   documento maestro será trabajo de la Fase 9.
4. **Cero opinión del LLM en el capítulo.** Si una formulación es
   especulativa, se omite. No se marca como "aspecto interesante"
   ni se etiqueta con observaciones del modelo.
5. **Trazabilidad completa.** Cada cifra del capítulo en
   `BITACORA_CIFRAS.md`.
6. **Si una cifra del material previo no aparece en el `INFORME_RECONOCIMIENTO.md`
   como sólida**, NO se incluye en el cap. 1, salvo que se cite como
   "trabajo previo del autor publicado en X" con referencia.
7. **Castellano académico**, sin emojis.

## Resumen final esperado al cierre de la sesión

8-10 líneas con:

- Páginas estimadas del Cap. 1 (verificación contra rango 5-7).
- Número de cifras nuevas introducidas y registradas en
  `BITACORA_CIFRAS.md`.
- Decisiones de redacción no triviales que se hayan tomado (p. ej.,
  cómo se ha resuelto la mención al curso de la Dra. Taberner sin
  caer en narrativización).
- Cualquier discrepancia detectada entre el material previo y el
  `INFORME_RECONOCIMIENTO.md` que pueda afectar a fases posteriores.
- Cualquier punto que requiera decisión del autor antes de Fase 3.
