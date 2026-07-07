# Guion de defensa — TFG EPS0270 · Dermapixel

**Duración objetivo:** 30 min (Parte A investigación ≈ 20 min · Parte B prototipo ≈ 4 min + demo en vivo ≈ 5-6 min). ~28 diapositivas + demo.
*(Xavi sugirió 20; preparamos 30 = 20+10 y, si el tribunal acota a 20, se recorta con las palancas del final.)*
**Ritmo:** ~1 min/slide. Cada slide con **1-2 cifras clave**, no todas. La memoria queda para las preguntas.

## ★ MENSAJE PARA LLEVARSE (take-home) — la única frase que deben recordar
> **"Este trabajo evaluó de forma independiente los modelos fundacionales en dermatología, construyó el primer recurso clínico abierto en español —con texto narrativo de caso real— y demostró que, en IA médica, el principal factor que determina el rendimiento no es únicamente la arquitectura del modelo, sino la calidad de los datos sobre los que se entrena y se evalúa."**

Si dentro de una semana el tribunal recuerda **esto**, la defensa funcionó. La MISMA idea (los datos > la arquitectura) se planta **tres veces, en forma creciente**, no repetida literal: se **anuncia** conversacional al principio (slide 4), se **reformula** al cerrar la investigación (slide 21, *"los modelos fundacionales han cambiado la pregunta"*) y **culmina en forma universal y humana** como últimas palabras (slide 29, *"ningún modelo, en la actualidad, sustituye a unos datos de calidad, ni al conocimiento del especialista que los construye"*). El final es la idea aprendida, no el resumen del índice.
*Blindaje:* si preguntan "¿el primero?", responder que es el primero **de este tipo** —fotografía clínica en español con texto narrativo de caso real—, que la memoria documenta como prácticamente inexistente.
*Dos apuntes de futuro con los que también quieres que se queden:* la **interpretabilidad por SAE** tiene muchísimo potencial, y la **rama contrastiva en español** no falla por método sino por datos —con el banco del hospital, despega. Ambos confirman el mensaje central: el límite es el dato.

**Consejos de entrega:**
- **Habla mucho más despacio de lo que escribes.** Tú llevas un año dentro del proyecto; el tribunal no. Deja respirar cada término (PanDerm, LoRA, zero-shot, SAM): una frase, una pausa.
- **Una idea por diapositiva, muy visual, poco texto.** Los números en grande; tú los explicas. La calidad de la defensa dependerá más de cómo lo cuentes que del contenido, que ya es sólido.
- **No suavices el tono honesto** —"esto funcionó, esto no, aquí falta potencia estadística, esto necesita más datos". Es tu mayor activo: transmite que entiendes cómo se hace investigación, no solo cómo se entrenan modelos.
- Habla a los mensajes, no a los números: di *el* dato que importa y sigue.
- Ideas-ancla que sostienen el mensaje: (1) *"ningún modelo ni ninguna receta gana en todo"*; (2) *"el cuello de botella ya no es el modelo, es el dato"*; (3) *"las representaciones ya codifican conceptos clínicos sin que nadie se los enseñe"*.
- Mira al tribunal en las 3 entregas del mensaje (slides 4, 21, 32); baja el ritmo ahí.

---

# PARTE A — INVESTIGACIÓN (≈20 min)

## Slide 1 — Portada (20 s)
**VISUAL:** Título "Dermapixel: Evaluación de modelos fundacionales para Dermatología Clínica" · Autor · Tutor Dr. Javier Varona · Colaboración clínica Dra. Rosa Taberner · **Origen · blog dermapixel.blogspot.com** · Prototipo dermapixel.eu · UIB/EPS · EPS0270.
**LOCUCIÓN:**
> Buenos días. Soy Antonio Contestí y presento mi Trabajo de Fin de Grado: una evaluación de los modelos fundacionales aplicados a la dermatología clínica, dirigido por el Dr. Javier Varona y con la colaboración clínica de la Dra. Rosa Taberner, del Hospital Universitari Son Llàtzer. Y el nombre no es casual: *Dermapixel* es el blog de dermatología de la Dra. Taberner, una de las referencias divulgativas en español —la semilla de la que nace este trabajo.

## Slide 2 — El problema clínico (85 s)
**VISUAL:** Foto de lesión + curva supervivencia melanoma (99% estadio I → 25% estadio IV). Las **3 modalidades** en foco (clínica · dermatoscopia · histopatología) + al margen, en gris: "otras: imagen corporal completa · clínica+dermatoscopia (multimodal) → evolución futura".
**LOCUCIÓN:**
> Empiezo por el problema. La dermatología afronta una demanda creciente frente a un acceso al especialista limitado: se deriva desde primaria, pero la capacidad del circuito presencial no da abasto. Y en dermatología el tiempo es crítico: en un melanoma, la supervivencia a cinco años cae de cerca del 99% en estadio I a un 25% en estadio IV. Detectar a tiempo salva vidas. Todo esto motiva el interés por los sistemas de apoyo al diagnóstico por imagen. En este trabajo abarco las **tres modalidades sobre las que existen modelos fundacionales** —fotografía clínica, dermatoscopia e histopatología—, aunque el foco está en las dos primeras, y muy especialmente en la fotografía clínica, la menos explorada; la histopatología entra de forma marginal, solo como prueba de transferencia a un tejido muy distinto. Existen además otras aproximaciones —como la imagen corporal completa para el seguimiento de pacientes, o la combinación simultánea de fotografía clínica y dermatoscopia de una misma lesión, que suele mejorar el rendimiento diagnóstico. Nuestro dataset ya contiene algunos casos multimodales de ese tipo, pero esa línea queda fuera del alcance de este trabajo y la planteo como una evolución futura.

## Slide 3 — Un cambio de paradigma (70 s)
**VISUAL:** Dos generaciones enfrentadas → **1.ª generación:** "un modelo = una enfermedad" (melanoma sí/no · AUROC >0,95 en HAM10000 ≈ experto). **↓** **2.ª generación:** "un modelo fundacional = muchas enfermedades · modalidades · tareas" (preentrenado + adaptable con linear probing / LoRA).
**LOCUCIÓN:**
> Hasta hace pocos años, prácticamente todos los trabajos desarrollaban un modelo específico para una única tarea: melanoma sí o no, o clasificar un conjunto concreto de enfermedades sobre dermatoscopia. Y en esa tarea concreta los mejores sistemas ya funcionan muy bien: alcanzan AUROC por encima de 0,95 en benchmarks públicos como HAM10000, comparables a las de dermatólogos expertos. Por eso el reto ya no es mejorar unas décimas esa cifra. El reto es otro: disponer de un mismo modelo capaz de generalizar a muchas enfermedades, modalidades y tareas. Ahí cambia el paradigma: de la primera generación —un modelo, una enfermedad— a los modelos fundacionales, preentrenados sobre millones de imágenes y adaptables después a múltiples tareas con técnicas como linear probing o LoRA. La pregunta ya no es si un modelo detecta bien el melanoma, sino si **un mismo modelo puede servir de base para resolver muchas tareas dermatológicas distintas**. Y ahí es donde se sitúa mi trabajo.

## Slide 3B — El estado del arte: cinco familias (55 s) · el mapa del terreno
**VISUAL:** Cinco familias de modelos fundacionales en filas numeradas 01–05: **encoders visuales auto-supervisados** (PanDerm · DINOv2) · **vision-language contrastivo** (DermLIP · SigLIP) · **zero-shot nativo** (DermLIP · BiomedCLIP) · **segmentación promptable** (SAM2 · MedSAM2) · **LLMs multimodales generalistas** (GPT-4o · MedGemma). Cierre-puente: *"Las evalué todas → tres retos abiertos."*
**LOCUCIÓN:**
> Antes de señalar los retos, quería situar el mapa del terreno. Al revisar el estado del arte, agrupé los modelos fundacionales en cinco grandes familias. La primera son los **encoders visuales auto-supervisados**, como PanDerm, que aprenden representaciones a partir de millones de imágenes sin necesidad de etiquetas. La segunda, los modelos **vision-language contrastivos**, que aprenden alineando imagen y texto en un mismo espacio, al estilo de CLIP. La tercera son los modelos con **zero-shot nativo**, capaces de clasificar una lesión sin reentrenar, solo a partir de una descripción. La cuarta, la **segmentación promptable**, con arquitecturas como SAM o MedSAM2, que delimitan la lesión a partir de una simple indicación. Y la quinta, los grandes **modelos de lenguaje multimodales generalistas**, como GPT-4o o MedGemma, que razonan sobre la imagen en lenguaje natural. En este trabajo evalué las cinco familias. Y precisamente al ponerlas a prueba fue donde encontré tres retos abiertos.
*(Transición directa a la slide 4: enlaza "evalué las cinco familias" con "encontré tres retos abiertos".)*

## Slide 4 — Tres retos abiertos, la pregunta y el anuncio (90 s) · ★ una de las slides clave
**VISUAL:** Tres retos abiertos etiquetados: **metodológico** · **lingüístico** · **translacional**. Debajo, la pregunta. En banda inferior destacada: el anuncio de la conclusión. Marca ★.
**LOCUCIÓN:**
> Al revisar la literatura encontré tres retos abiertos. El primero es **metodológico**: la mayoría de modelos se evalúan con protocolos diferentes, datasets distintos e incluso métricas distintas, y eso dificulta saber cuál funciona realmente mejor. El segundo es **lingüístico**: la inmensa mayoría de datasets y modelos vision-lenguaje están construidos en inglés; encontrar fotografía clínica acompañada de narrativa médica real en español es excepcional. Y el tercero es **translacional**: una cosa es obtener buenos resultados en un benchmark, y otra muy distinta integrarlos en un flujo clínico real. De ahí la pregunta del trabajo: **¿qué modelos fundacionales generalizan realmente fuera de sus datos de entrenamiento, cómo se comportan en un entorno clínico en español, y qué papel desempeña el texto clínico?**
>
> *(pausa)* Y hay una idea que me gustaría que recordaran al terminar esta presentación. *(pausa)* Después de evaluar los modelos de forma independiente, construir un recurso clínico en español y trasladarlo a un prototipo funcional, la conclusión principal no es cuál es el mejor modelo. *(pausa)* La conclusión es que, en inteligencia artificial médica, **el principal factor que determina el rendimiento no es únicamente la arquitectura del modelo, sino la calidad de los datos sobre los que se entrena y se evalúa**.
*(★ Anuncio del mensaje para llevarse — conversacional, con pausas reales, mirando al tribunal. La versión literal se entrega en las slides 21 y 32.)*

## Slide 5 — Objetivos y aportaciones (80 s) · ★ el espíritu del TFG
**VISUAL:** Titular grande: **"Este trabajo no propone un modelo más; propone una forma de evaluarlos."** · Dos bloques enfrentados:
**Objetivos** — 1. Comparar de forma independiente los modelos fundacionales · 2. Evaluar las estrategias clave (LoRA · zero-shot · multimodalidad · interpretabilidad) · 3. Trasladar el reconocimiento sobre fotografía clínica a un prototipo clínico funcional.
**Aportaciones** — ✔ Benchmark independiente · ✔ DermapixelAI (recurso clínico en español) · ✔ Dermapixel R0 y evidencia metodológica · ✔ Prototipo funcional.
Pie: recuadro **Open** (pesos+código abiertos → reproducible + integrable en hospital; cerrados = referencia).
**LOCUCIÓN:**
> El trabajo persigue tres objetivos. Primero, comparar de forma independiente los principales modelos fundacionales dermatológicos. Segundo, evaluar qué estrategias aportan realmente valor —LoRA, la clasificación zero-shot, la multimodalidad o la interpretabilidad. Y tercero, trasladar el reconocimiento sobre fotografía clínica —la modalidad menos explorada— a un prototipo clínico funcional; es decir, demostrar la transferencia a un entorno clínico real. Pero, más allá de los objetivos, quiero destacar la idea que resume el espíritu del trabajo: **no propone un modelo más; propone una forma de evaluarlos**. De ahí sus cuatro aportaciones: un benchmark independiente; la creación de DermapixelAI como recurso clínico en español; evidencia metodológica sobre qué estrategias funcionan de verdad —incluida la adaptación Dermapixel R0—; y un prototipo funcional que integra todo. Y una precisión sobre el método: todas las comparaciones priorizan modelos con pesos y código abiertos. No fue una decisión casual —buscaba que cada experimento fuera reproducible y que los resultados pudieran trasladarse después a un entorno hospitalario. Los modelos cerrados, como GPT-4o, se usan únicamente como referencia comparativa.

## Slide 5B — El alcance del trabajo (20 s) · transición, números grandes
**VISUAL:** Solo cifras grandes, sin más texto: **14** modelos · **12** datasets · **72.654** imágenes · **3** modalidades · **4** protocolos experimentales · ontología propia · **DermapixelAI** · **Dermapixel R0** · prototipo funcional.
**LOCUCIÓN:**
> Antes de entrar en los resultados, quería situar el alcance del trabajo. No se trata de comparar dos o tres modelos, sino de un benchmark amplio: catorce modelos, doce datasets, más de setenta mil imágenes armonizadas y varios protocolos experimentales. Este volumen es lo que permite extraer conclusiones comparativas con cierta solidez. Y con ese alcance, la siguiente pregunta era cómo comparar todos esos modelos de forma justa.
*(Transición natural a la metodología —evita el "ahora explico la metodología". Enlaza con la slide 6.)*

## Slide 6 — Por qué PanDerm (60 s)
**VISUAL:** PanDerm en 3 ideas grandes: **2,1 M imágenes** · **4 modalidades** · **pesos + código + benchmarks públicos**. (En la figura, pequeño: ViT Base ~86M / Large ~307M · +10% sobre el estado del arte previo.)
**LOCUCIÓN:**
> Antes de presentar los experimentos necesito introducir las dos referencias principales del trabajo. La primera es **PanDerm**, considerado el primer modelo fundacional dermatológico abierto. Un modelo fundacional es un modelo preentrenado sobre un gran volumen de datos que después puede adaptarse a múltiples tareas con muy pocos datos adicionales. PanDerm se entrenó sobre **2,1 millones de imágenes** dermatológicas de cuatro modalidades, y sus autores reportan una mejora cercana al 10% sobre el estado del arte previo. Pero para este trabajo tenía una ventaja aún más importante: **publica sus pesos, su código y sus benchmarks**. Eso permitió una evaluación completamente independiente y reproducible. Por eso PanDerm constituye la referencia central de toda la comparación.

## Slide 7 — Por qué DermLIP (55 s)
**VISUAL:** Tabla comparativa (el tribunal entiende el porqué en 5 s):

| | PanDerm | DermLIP |
|---|---|---|
| Entrada | Imagen | Imagen + texto |
| Preentrenamiento | 2,1 M imágenes | 1 M pares imagen-texto |
| Ventaja principal | Representación visual | Alineamiento multimodal |
| Permite zero-shot | ✗ | ✓ |

**LOCUCIÓN:**
> La segunda referencia es **DermLIP**, que extiende PanDerm incorporando una rama textual mediante un entrenamiento contrastivo tipo CLIP. Para ello utiliza **Derm1M**, un corpus con más de un millón de pares imagen-texto organizados mediante una ontología dermatológica. La diferencia principal respecto a PanDerm es que ya no aprende únicamente representaciones visuales, sino también la relación entre la imagen y su descripción clínica. Esa alineación imagen-texto es la que hace posible tareas como la clasificación zero-shot o la recuperación semántica de casos —dos aspectos que evaluaremos más adelante. La pregunta que me planteé fue sencilla: **¿cómo se comportan realmente estos dos paradigmas cuando se evalúan de forma independiente y bajo un mismo protocolo?**

## Slide 8 — Evaluación sobre múltiples escenarios clínicos (75 s)
**VISUAL:** Cabecera grande: **12 datasets · >72.000 imágenes · 3 modalidades**. Tres bloques por modalidad (nombres en la figura, no en la voz):
- **Dermatoscopia:** HAM10000 · BCN20000 · HIBA · MSKCC
- **Fotografía clínica:** PAD-UFES-20 · DDI · DermNet · Fitzpatrick17k
- **Histopatología:** WSI patches

**LOCUCIÓN:**
> Para la evaluación construimos un banco común de doce datasets públicos, con más de setenta mil imágenes, que cubren las principales modalidades de la dermatología: dermatoscopia, fotografía clínica e incluso histopatología, con imágenes procedentes de hospitales, atención primaria y repositorios internacionales. En dermatoscopia usamos, por ejemplo, HAM10000 o BCN20000; en fotografía clínica, PAD-UFES, DDI o DermNet; y también incorporamos histopatología. La diversidad era intencionada: no buscábamos optimizar un modelo para un único conjunto de evaluación, sino comprobar hasta qué punto **generaliza** cuando cambia la modalidad, el dispositivo de adquisición, la población o el contexto asistencial. Todas las particiones de entrenamiento, validación y test se respetaron exactamente como fueron publicadas por los autores. Y precisamente esa heterogeneidad explica por qué, cuando más adelante muestre medias entre datasets, las interpreto solo como una **tendencia descriptiva, y nunca como un ranking absoluto** entre modelos.

## Slide 9 — Un lenguaje común: la ontología L1/L2/L3 (80 s) · ★ contribución propia
**VISUAL:** Pirámide **L1 = 4 familias · L2 = 43 subcategorías · L3 = 367 diagnósticos** (SNOMED CT + CIE-10 · validada con la Dra. Taberner · 72.654 imágenes armonizadas). Debajo, en grande:
> **Sin ontología común → ❌ no existe comparación justa entre datasets.**
**LOCUCIÓN:**
> Antes de poder comparar modelos apareció un problema fundamental: **cada dataset habla un idioma diferente**. Un mismo diagnóstico puede recibir nombres distintos, distintos niveles de detalle, o agruparse de otra forma según el dataset; y sin un vocabulario común, cualquier comparación entre modelos deja de ser justa. Para resolverlo construimos, junto con la Dra. Rosa Taberner, una **ontología jerárquica de tres niveles**: cuatro grandes familias etiológicas en el primer nivel, cuarenta y tres subcategorías clínicas en el segundo, y más de trescientos diagnósticos individuales en el tercero. Cada diagnóstico quedó además vinculado a SNOMED CT y CIE-10 para facilitar la interoperabilidad clínica. Y gracias a esta ontología pudimos **armonizar más de setenta y dos mil imágenes procedentes de once datasets diferentes bajo un único lenguaje clínico**. En el fondo, antes de comparar modelos, primero tuvimos que conseguir que todos hablaran el mismo idioma. Y esta ontología no termina aquí: más adelante volverá a aparecer, porque también es la base sobre la que se organiza el prototipo clínico.

## Slide 10 — Evaluación reproducible y sin sesgos (85 s) · ★ rigor metodológico
**VISUAL:** Dos mitades.
**Izquierda — 4 protocolos** (un icono cada uno, sin definir): Linear probing → calidad de la representación · Fine-tuning → rendimiento máximo · Segmentación → localización de la lesión · Zero-shot → clasificación guiada por texto.
**Derecha — Auditoría de contaminación (MD5):** 11 datasets limpios → **0 %** solapamiento · **DermNet → 100 %** (contaminado). Debajo: semillas fijas · predicciones persistidas · benchmark reproducible.
Banda inferior, en grande: **"Comparar modelos solo tiene sentido si todos juegan con las mismas reglas."**
**LOCUCIÓN:**
> Sobre este banco común aplicamos cuatro protocolos complementarios. Linear probing, para medir la calidad intrínseca de las representaciones aprendidas. Fine-tuning, para estimar el rendimiento máximo tras adaptación. Segmentación, para evaluar la localización de la lesión. Y zero-shot, para estudiar la clasificación guiada por texto sin entrenamiento específico.
>
> *(pausa)* Pero hay un aspecto metodológico del que estoy especialmente orgulloso. Antes de comparar modelos comprobamos si alguno de los datasets de evaluación ya había sido utilizado durante el preentrenamiento de esos modelos. La auditoría mediante hash MD5 reveló un único caso de solapamiento exacto: **DermNet, con un 100 % de coincidencias**; en el resto de datasets no encontramos ninguna coincidencia exacta. Eso nos permitió interpretar los resultados con transparencia y **señalar explícitamente qué comparaciones podían estar afectadas por contaminación de datos**. Además, todos los experimentos se ejecutaron con semillas fijas y las predicciones se almacenaron para garantizar la reproducibilidad completa del benchmark. Porque comparar modelos solo tiene sentido si antes garantizamos que todos juegan con las mismas reglas.

## Slide 11 — Resultado 1 · La ventaja de dominio depende del escenario (90 s)
**VISUAL:** Frase grande arriba: **"El preentrenamiento de dominio importa… ↓ …especialmente cuando el escenario se acerca a la práctica clínica real."** Debajo, barras LP PanDerm Large vs Base (+4,1 Acc / +9,0 BAcc / +3,6 AUROC pp). Nota: HAM SigLIP 90% acc · PAD PanDerm AUROC 0,949 · DDI PanDerm AUROC 0,860 (el 0,772 de PAD es accuracy, no AUROC — no mezclar). Chip sembrado: *"El mejor modelo depende del escenario."*
**LOCUCIÓN:**
> Entrando ya en los resultados, empezamos por la clasificación mediante linear probing —es decir, evaluando únicamente la calidad de las representaciones aprendidas por los modelos. Lo primero que observamos es que PanDerm Large mejora de forma consistente a PanDerm Base, con una ganancia media cercana a nueve puntos de balanced accuracy. Pero el resultado realmente interesante no es ese. La ventaja del preentrenamiento dermatológico **no es constante: aumenta a medida que el escenario se aleja de la dermatoscopia estandarizada y se acerca a la práctica clínica real**. En benchmarks muy estandarizados como HAM10000, modelos generalistas como SigLIP-Large alcanzan resultados comparables e incluso superiores, con un 90% de accuracy. Pero cuando pasamos a fotografía clínica, a imágenes tomadas con móvil o a cohortes más heterogéneas, PanDerm pasa a ser claramente el mejor modelo. La conclusión es que el beneficio del preentrenamiento de dominio no es universal: depende de la distancia entre el escenario de evaluación y los datos con los que el modelo fue entrenado. En una idea que reaparecerá varias veces hoy: **el mejor modelo depende del escenario**. Y esto nos llevó a preguntarnos si esa ventaja seguía existiendo cuando, en lugar de miles de imágenes anotadas, solo teníamos unas pocas decenas.

## Slide 12 — Resultado 2 · Eficiencia de etiquetas (75 s)
**VISUAL:** Izq: 📈 curva de saturación (AUROC vs % de datos). Der, en grande: **82 imágenes → 96 % del rendimiento** · **14 imágenes → 95 % del rendimiento**. Debajo, frase-resumen: **"La representación ya estaba aprendida."**
**LOCUCIÓN:**
> La siguiente pregunta fue: ¿cuántas imágenes etiquetadas hacen falta para aprovechar un modelo fundacional? Y, sinceramente, fue el resultado que más me sorprendió: muy pocas. Con solo el 1% de HAM10000 —es decir, 82 imágenes— PanDerm Large ya alcanza una AUROC de 0,918, muy próxima al rendimiento máximo. En PAD-UFES es todavía más llamativo: con únicamente 14 imágenes recupera cerca del 95% de la AUROC final. Esto significa que la capacidad de representación ya estaba aprendida durante el preentrenamiento; las pocas etiquetas adicionales no le enseñan dermatología al modelo, simplemente le indican cómo adaptar ese conocimiento a una tarea concreta. Eso sí, no todas las métricas saturan igual: la AUROC alcanza pronto un techo, mientras que la balanced accuracy sigue mejorando, porque las clases minoritarias necesitan más ejemplos para discriminarse bien. Es una primera evidencia de que, cuando disponemos de un buen modelo fundacional, **añadir más capacidad al modelo aporta menos que disponer de datos bien etiquetados**. Todo esto ocurre con el encoder congelado. Y si ya obteníamos estos resultados sin tocarlo, parecía lógico pensar que reentrenarlo por completo mejoraría aún más; precisamente eso fue lo que quisimos comprobar a continuación.
*(Nota de apoyo — por si preguntan "¿por qué la AUROC satura y la BAcc no?": la AUROC mide la capacidad de **ordenar** los casos, independiente del umbral → alta con pocos ejemplos porque PanDerm ya separa bien en el espacio de embeddings. La balanced accuracy es el **recall medio por clase**, con el mismo peso a cada clase → con el 1–5% de datos una clase rara tiene 0–2 ejemplos útiles, así que se aciertan las frecuentes y se fallan las raras; eso apenas mueve la AUROC pero hunde la BAcc. En corto: la AUROC dice que la representación ya es discriminativa con muy poca etiqueta; la BAcc recuerda que para las clases minoritarias hacen falta ejemplos etiquetados de esas clases.)*

## Slide 13 — Resultado 3 · No hay una estrategia de adaptación universal (70 s)
**VISUAL:** Dos columnas.
**Dataset pequeño:** ❌ Fine-tuning · ✔ Adaptación ligera (Linear Probing / LoRA)
**Dataset grande:** ✔ Fine-tuning
Barras de apoyo: HAM +47,1 pp (BAcc 0,852, Acc 0,920) · PAD +19,4 pp · DDI −2,1 pp (sobreajuste). Abajo, en grande: **"No existe una estrategia de adaptación universal."**
**LOCUCIÓN:**
> La siguiente pregunta fue: ¿merece la pena adaptar completamente el modelo? La respuesta vuelve a depender del tamaño del dataset. Cuando disponemos de muchos datos, el fine-tuning aporta una mejora muy importante: en HAM10000 la balanced accuracy aumenta cerca de 47 puntos y alcanzamos un 92% de accuracy. Pero cuando el conjunto de entrenamiento es pequeño ocurre justo lo contrario: en DDI, con unas cuatrocientas imágenes de entrenamiento, el fine-tuning empeora el rendimiento por sobreajuste —el modelo deja de generalizar y aprende demasiado la distribución del entrenamiento. La conclusión práctica es clara y la recupero luego en la discusión: **no existe una estrategia de adaptación universal**. Con muchos datos, el fine-tuning merece la pena; pero con pocos datos, las **estrategias de adaptación ligera** son preferibles al reentrenamiento completo. Y eso abre una tercera vía: una técnica intermedia entre el linear probing y el fine-tuning, llamada **LoRA**, que explicaré en detalle más adelante y que es la base de nuestra adaptación **Dermapixel R0**.

## Slide 14 — Resultado 4 · Segmentación: adaptación eficiente con SAM2 (65 s)
**VISUAL:** Imagen original → máscara. **Dice 0,947 (ISIC2018)** · supera la referencia PanDerm (0,921) · generaliza sin reentrenar (ISIC2017 0,945 / PH2 0,960). **MedSAM2-tiny → 0,9556 / 26 ms**.
**LOCUCIÓN:**
> El siguiente bloque aborda la segmentación automática de la lesión. Utilizamos SAM2, un modelo fundacional diseñado para segmentación general, y lo adaptamos al dominio dermatológico entrenando únicamente su decodificador y manteniendo congelado el encoder visual. El resultado fue uno de los más destacados del trabajo: un **Dice de 0,947 sobre ISIC2018**, superando la referencia publicada por PanDerm y generalizando prácticamente sin pérdida a otros dos datasets. Quisimos ir más allá y comparar distintas arquitecturas promptables: evaluamos cinco modelos, y el mejor compromiso entre precisión y velocidad fue **MedSAM2-tiny**, con un Dice de 0,9556 y un tiempo de inferencia de apenas 26 milisegundos por imagen. *(pausa)* Sin embargo, el hallazgo más interesante no fue qué arquitectura ganaba.

## Slide 15 — Resultado 5 · Segmentación: qué factor gobierna el rendimiento (85 s)
**VISUAL:** Barras de importancia de cada factor: Arquitectura **+1 pp** · Preentrenamiento **+1 pp** · **Bounding box +7,5 pp**. Debajo: Dermatólogo vs Dermatólogo **0,728** · Modelo vs Consenso **0,915** (98% dentro de la variabilidad humana). Chip: **SAM2 → prototipo (M2)**.
**LOCUCIÓN:**
> Lo realmente importante fue descubrir **qué factor condiciona el rendimiento**. Pensábamos que la diferencia estaría en la arquitectura o en el preentrenamiento médico. Pero no. La arquitectura explica alrededor de un punto de Dice; el preentrenamiento médico, otro punto. En cambio, **eliminar la caja que localiza la lesión hace caer el rendimiento siete puntos y medio**. Es decir, la información de localización pesa entre seis y siete veces más que la elección del segmentador. La conclusión práctica es muy clara: en un sistema clínico merece mucho más la pena invertir esfuerzo en **detectar correctamente la lesión** que en cambiar continuamente de segmentador.
>
> Además quisimos responder a otra pregunta: ¿hasta dónde puede mejorar realmente un segmentador? Para ello lo comparamos con el propio desacuerdo entre dermatólogos. Dos expertos solo coinciden en torno a un Dice de **0,728** al dibujar el borde de una lesión; nuestro modelo alcanza **0,915** respecto al consenso y permanece dentro de la variabilidad humana en el **98%** de los casos. Esto significa que el margen de mejora restante ya no viene tanto del algoritmo como de la propia **incertidumbre de la anotación clínica**. Por eso SAM2 es el segmentador que finalmente incorporamos al prototipo.
*(Nota de apoyo — si preguntan por robustez de la caja: aflojarla es seguro (−2,8 pp al +10%), pero apretarla es catastrófico (−15 pp al −20%); por eso en producción usamos cajas generosas. Robustez confirmada con validación cruzada 5-fold, IC95% muy estrecho.)*

## Slide 16 — Resultado 6 · El texto también importa (90 s)
**VISUAL:** Barras zero-shot: 0,366 → 0,516 → **0,854** (**+48,8 pp**). Al lado: **MISMA IMAGEN** · ✔ cambia el tokenizador · ✔ cambia el prompt → **+48,8 pp AUROC**. Debajo, el caso: ES 🇪🇸 carcinoma → 2.ª opción · ↓ · EN 🇬🇧 carcinoma → 1.ª opción.
**LOCUCIÓN:**
> El siguiente resultado cambia la forma de entender los modelos multimodales. Hasta ahora hablábamos de la imagen; aquí nos preguntamos qué papel juega el texto. Un apunte rápido para situarnos: en estos modelos, imagen y texto se proyectan a un mismo espacio de representaciones, y cuanto mejor alineados están ambos, mejor funciona la clasificación zero-shot. Pues bien: manteniendo exactamente la misma imagen y el mismo encoder visual, modificamos únicamente la rama textual. El resultado fue espectacular: la AUROC pasó de 0,366 a 0,854, una mejora de casi **49 puntos**. ¿Qué había cambiado? El modelo seguía siendo el mismo; lo único distinto era el tokenizador y la forma de representar el texto. La conclusión es que, en modelos vision-language, **el cuello de botella puede estar tanto en la imagen como en la alineación entre imagen y texto**.
>
> Y eso tiene una consecuencia inmediata para nuestro trabajo: como estos modelos se entrenaron principalmente con texto en inglés, el castellano queda peor alineado con el espacio visual. En un caso real de carcinoma, con las etiquetas en español el modelo priorizaba melanoma; simplemente traduciéndolas al inglés —sin cambiar la imagen ni reentrenar nada— el carcinoma pasaba a la primera posición. **La imagen nunca cambió: lo único que cambió fue el idioma con el que describíamos esa imagen.** Es decir, en zero-shot no basta con elegir un buen modelo: también hay que saber **cómo hablar con él**.

## Slide 17 — Resultado 7 · ¿Puede un LLM sustituir a un modelo especializado? (75 s)
**VISUAL:** Escalera: Especialista **92%** ↓ MedGemma+LoRA **81%** ↓ GPT-4o **49%** (BLIP-2 y otros ~azar, solo en la figura). Debajo, en grande: **"Más parámetros ≠ mejor rendimiento clínico."** Nota: gap 43,5 pp · LoRA +13,7 pp.
**LOCUCIÓN:**
> Una pregunta inevitable era si los grandes modelos multimodales, como GPT-4o o MedGemma, podían competir con los modelos especializados en dermatología. La respuesta, en el escenario evaluado y con los prompts utilizados, fue clara: no. Sobre HAM10000, el mejor modelo especializado alcanzó un **92% de accuracy**, mientras que el mejor modelo multimodal generalista se quedó en torno al **49%** —una diferencia de más de cuarenta puntos. Intentamos además adaptar MedGemma con LoRA: la mejora fue importante, casi catorce puntos, pero seguía quedando once por debajo del especialista. Otros modelos multimodales generalistas obtuvieron rendimientos próximos al azar. *(pausa)* La conclusión no es que los modelos de lenguaje sean malos. Es que, para una tarea tan específica de imagen médica, **lo que marca la diferencia no es tener más parámetros, sino haber aprendido dermatología**. Y esto define su papel en el prototipo: el modelo fundacional dermatológico realiza la clasificación, y el modelo de lenguaje se usa únicamente para generar explicaciones y apoyar la interacción con el usuario. Cada modelo tiene su papel.

## Slide 18 — Resultado 8 · Equidad y validación estadística (90 s)
**VISUAL:** Dos mitades.
**Izq (equidad):** Fototipo ↑ → todos empeoran · **BiomedCLIP: gap pequeño PERO peor rendimiento** → "el gap solo no mide equidad".
**Der (DeLong, sobre malignidad):** **PanDerm ≈ DermLIP** (sin diferencia significativa) · ambos **> generalistas** (significativo).
Banda inferior: **"En IA médica no basta una métrica: hay que interpretar el conjunto de la evidencia."**
**LOCUCIÓN:**
> El último resultado evalúa un aspecto especialmente importante en IA médica: la equidad. Analizamos el rendimiento de los modelos según el fototipo cutáneo, sobre Fitzpatrick17k. Todos empeoran cuando aumenta el fototipo, es decir, funcionan peor sobre pieles oscuras. Pero encontramos un resultado interesante: **BiomedCLIP presenta el menor gap entre fototipos y, sin embargo, es el modelo con peor rendimiento global**. Esto demuestra que un modelo puede parecer muy equitativo simplemente porque funciona igual de mal en todos los grupos. Por tanto, la equidad no puede evaluarse únicamente con el gap: siempre debe interpretarse junto al rendimiento global.
>
> Y, por último, quisimos comprobar si las diferencias observadas eran realmente significativas o podían deberse al azar. Para ello aplicamos el test estadístico de DeLong sobre la detección de malignidad. El resultado fue que **PanDerm Large y DermLIP v2 no presentan diferencias significativas entre sí**, mientras que **ambos sí superan de forma significativa a los modelos generalistas**. Eso sí: en los conjuntos de evaluación más pequeños no siempre hay suficiente tamaño muestral para distinguir a los mejores modelos; y eso no significa que sean equivalentes, sino simplemente que el estudio no tiene potencia estadística suficiente para diferenciarlos. En el fondo, este análisis refuerza una idea que ha aparecido durante toda la presentación: en IA médica no basta con mirar una única métrica; hay que interpretar siempre el conjunto de la evidencia.

## Slide 19 — Resultado 9 · Interpretabilidad: ¿qué ha aprendido el modelo? (90 s)
**VISUAL:** Cadena: **PanDerm → Sparse Autoencoder → conceptos latentes → Concept Bottleneck → 7 criterios dermatoscópicos → diagnóstico**. Al lado: ✔ Interpretabilidad · **AUROC 0,891 ≈ 0,890** (convencional). Debajo, en grande: **"Interpretabilidad sin pérdida de rendimiento."** Chip: matriz de Rosa 37×15 (en curso).
**LOCUCIÓN:**
> Hasta ahora hemos medido cuánto aciertan los modelos. La siguiente pregunta fue: ¿podemos entender **por qué** toman una decisión? Para responderla utilizamos un Sparse Autoencoder, que descompone la representación interna de PanDerm en más de dieciséis mil **features latentes**. Y lo interesante es que, sin supervisión explícita, muchas de ellas se alinean con conceptos clásicos de la dermatoscopia, como los criterios de la Lista de los Siete Puntos. Es decir —y esta es la idea que quiero destacar—: **el modelo ha aprendido conceptos dermatológicos sin que nadie se los enseñe explícitamente**.
>
> A continuación usamos esos conceptos como un **Concept Bottleneck**: en lugar de pasar directamente de la imagen al diagnóstico, el modelo primero predice los siete criterios dermatoscópicos y luego decide a partir de ellos. Deja de ser una caja negra y razona mediante conceptos clínicos intermedios que el dermatólogo puede inspeccionar. Hacer explícito ese razonamiento tiene un coste en precisión; pero con un ajuste multitarea alcanzamos el mejor compromiso: el modelo predice a la vez los siete criterios y el diagnóstico **casi sin pérdida de rendimiento** —una AUROC de 0,891 frente a 0,890 del modelo convencional. En una frase: **explicar no empeora el resultado**.
>
> Y esto ya no es solo un experimento: ese vocabulario dermatológico ya está **definido en el proyecto** —una matriz de conceptos construida con la Dra. Rosa Taberner— y la interpretabilidad basada en conceptos ya está **integrada como un módulo del propio prototipo**. Porque el objetivo final no es solo que el modelo acierte, sino que sea capaz de **justificar sus decisiones con el mismo lenguaje que un dermatólogo**.

## Slide 20 — De evaluar a crear: tres contribuciones propias (120 s) · ★ slide clave · aquí se explica LoRA (1.ª vez)
**VISUAL:** Tres bloques.
**DermapixelAI 1.0** — ✔ dataset **multimodal** (imagen + texto + caso) · ✔ español · ✔ casos reales · 672 casos / 1.089 imgs / 223 palabras mediana · auditado (0 solape) · licencia abierta.
**Dermapixel R0** — ✔ LoRA (punto intermedio) · ✔ **0,17%** params (524 K) · ✔ ≈ DermLIP v2.
**Próximo paso** — ✔ retrieval clínico en español · ✔ banco hospitalario.
**LOCUCIÓN:**
> Hasta ahora he hablado de evaluar modelos existentes. Pero el trabajo no se queda ahí: también aporta **tres contribuciones propias**. *(pausa)*
>
> La primera es **DermapixelAI 1.0**. Durante el trabajo vimos que casi todos los recursos disponibles estaban en inglés y centrados en dermatoscopia; faltaba un recurso clínico en español con texto narrativo real. Por eso lo construimos a partir del archivo de la Dra. Rosa Taberner: 672 casos, 1.089 imágenes y textos clínicos reales, con una mediana de 223 palabras por caso. Y quiero subrayar algo: **no es simplemente un dataset de imágenes, es un dataset multimodal** —imagen, texto y caso clínico. Además se documentó formalmente, se auditó frente a Derm1M —cero solapamiento— y se liberó bajo licencia abierta.
>
> La segunda es **Dermapixel R0**, nuestra adaptación de PanDerm al castellano. Para conseguirlo usamos LoRA. Habíamos visto dos extremos: congelar del todo el modelo, o reentrenarlo entero; LoRA es el punto intermedio —mantiene congelado el modelo y solo añade unas pequeñas matrices entrenables sobre algunas capas. Es como si el modelo ya hubiera estudiado toda la dermatología y, en lugar de reescribir el libro entero, le añadiéramos unas pocas páginas con lo específico de nuestra tarea. Entrenamos solo **524.000 parámetros, el 0,17% del modelo** —y, aun así, R0 alcanza prácticamente el mismo rendimiento que DermLIP v2 en la clasificación clínica en español. Esto **valida una de las conclusiones de antes**: con pocos datos, las adaptaciones eficientes son preferibles al fine-tuning completo.
>
> La tercera no es un resultado positivo, sino uno **igualmente útil**. Comprobamos que la recuperación semántica en español —buscar casos por texto libre— es técnicamente viable, pero que el volumen actual de datos todavía es insuficiente para generalizar. Lejos de ser un fracaso, es una **hipótesis validada en parte**: la arquitectura funciona, el cuello de botella ya no es el método —es el volumen de datos clínicos en español. Y nos marca con claridad el siguiente paso: integrar el banco de imágenes del hospital para escalar esa búsqueda clínica en español. De hecho, ya lo hemos empezado a comprobar —**fuera del alcance de esta memoria**—: al ampliar el dataset con material clínico cedido por el Dr. Alex Llambrich, y validando con varias semillas, la **clasificación mejora**, pero la **búsqueda por texto en español todavía no**; justo lo que anticipábamos, el límite es el dato, no el método.
>
> En conjunto, estas tres contribuciones **transforman un benchmark en una plataforma**: un recurso abierto en español, un modelo adaptado al dominio clínico, y una línea clara de evolución hacia un sistema asistencial.

## Slide 20B — Limitaciones asumidas (55 s) · honestidad antes de concluir
**VISUAL:** Cinco limitaciones en filas numeradas 01–05: **Semilla única** · **Potencia estadística** (DeLong solo con potencia en Fitzpatrick17k) · **Contaminación: solo exacta** (MD5 no detecta near-duplicates) · **Datos en español** (672 casos) · **Sin validación prospectiva** (prototipo, no producto certificado). Cierre en grande: *"declaradas, no ocultas — ninguna invalida las conclusiones, pero marcan hasta dónde llegan"*.
**LOCUCIÓN:**
> Antes de concluir, quiero ser honesto con las limitaciones, porque son limitaciones **declaradas, no errores ocultos**. Primera, estadística: gran parte de los experimentos usan una sola semilla; el bootstrap acota la incertidumbre de los datos, pero no la variabilidad entre inicializaciones —aun así, la magnitud de los efectos, nueve puntos, cuarenta y tres, excede esa variabilidad esperable. Segunda, la potencia: en los datasets pequeños no hay tamaño muestral para separar a los mejores modelos, así que el cierre con DeLong solo lo hago donde hay positivos suficientes, en Fitzpatrick17k; falta de potencia no es lo mismo que ausencia de efecto. Tercera, la auditoría de contaminación por MD5 solo detecta duplicados exactos, no reescalados ni recortes. Cuarta, el dato en español todavía es limitado: con 672 casos, la recuperación por texto aún no generaliza. Y quinta, esto es un prototipo, no un producto validado clínicamente: sin cohorte prospectiva ni marcado CE, y los modelos cerrados por API no son plenamente reproducibles. Reconocerlas es parte del rigor: ninguna invalida las conclusiones, pero marcan hasta dónde llegan.
*(Tono sereno y honesto —es tu mayor activo—. Puente natural a Conclusiones.)*

## Slide 21 — Conclusiones de la investigación · tres descubrimientos (90 s)
**VISUAL:** Tres mensajes encadenados: **(1) No existe un modelo universal** ↓ **(2) El cuello de botella son los datos** ↓ **(3) La IA empieza a ser explicable**. Abajo, muy grande: **"Los modelos fundacionales cambian la tecnología; los datos cambian la medicina."** (Sin objetivos en pantalla.)
**LOCUCIÓN:**
> Si tuviera que resumir todo este trabajo en tres ideas, serían estas. La primera: **no existe un modelo universalmente superior** —los modelos fundacionales se especializan según la tarea, el nivel de la ontología y el tipo de datos. La segunda, y probablemente la más importante: una vez alcanzado el nivel actual de estos modelos, **el cuello de botella deja de ser la arquitectura**; lo que realmente determina el rendimiento es la calidad, la diversidad y la cobertura de los datos con los que los entrenamos y los evaluamos. Y la tercera: los modelos ya no solo clasifican —**empiezan a aprender conceptos clínicos** que podemos interpretar y usar para explicar sus decisiones, acercando la IA al razonamiento del dermatólogo. Con ello considero cumplidos los tres objetivos que planteé al inicio: evaluar de forma independiente los modelos fundacionales, construir un recurso clínico abierto en español, y trasladar ese conocimiento a un prototipo funcional.
>
> Y si tuviera que dejarlo en una sola idea: **los modelos fundacionales han cambiado la pregunta**. Hoy el reto ya no es únicamente construir modelos más grandes, sino construir **mejores datos** sobre los que esos modelos puedan aprender. Por eso este trabajo no termina con un benchmark, sino que continúa como una **plataforma abierta** para seguir construyendo inteligencia artificial clínica en español. Y esa plataforma es el prototipo que os enseño ahora.
*(★ Refuerzo del mensaje en forma evolucionada —"han cambiado la pregunta"— y puente a la Parte B. La entrega literal del take-home se reserva para la slide 29. Objetivos: mencionados de pasada, nunca leídos ni al final.)*

---

# PARTE B — EL PROTOTIPO (≈10 min: ~4 min slides + ~5-6 min demo en vivo)

> **Filosofía de la Parte B (Xavi + tú):** tras 20 min de ciencia, el tribunal quiere *ver que funciona*. Slides breves (3 ideas) → **demostración real**. Una buena demo es más memorable que diez capturas, y ante un tribunal de Informática demuestra que sabes convertir investigación en producto.

## Slide 22 — Del benchmark al producto (45 s)
**VISUAL:** Captura dermapixel.eu + esquema simple: Frontend → Backend (**nunca ejecuta modelos**) →[red privada]→ Servidor GPU (inferencia). Etiquetas: *desacoplado · resiliente*.
**LOCUCIÓN:**
> Hasta ahora hemos hablado de investigación. Quería comprobar si todo ese conocimiento podía trasladarse a un sistema real. Ese sistema es Dermapixel, disponible en dermapixel.eu. Un único apunte de arquitectura: está **desacoplada** —el backend nunca ejecuta modelos directamente; toda la inferencia ocurre en un servidor GPU independiente, lo que permite escalar y mantener la resiliencia, de modo que si la GPU falla el servicio se degrada con elegancia en lugar de caerse.

## Slide 23 — Once módulos (30 s)
**VISUAL:** Rejilla M1–M11 (solo nombres, muy visual).
**LOCUCIÓN:**
> El prototipo integra **once módulos** de inteligencia artificial, muchos desarrollados durante este trabajo. No voy a recorrerlos uno a uno —porque los vais a ver funcionando en un caso real dentro de un momento.

## Slide 24 — El veredicto: consenso, jerarquía e incertidumbre (60 s)
**VISUAL:** Captura "Detalle del análisis": veredicto determinista + L1/L2/L3 + banner de discrepancia.
**LOCUCIÓN:**
> Tres ideas que quiero que veáis en el sistema. Primera, el veredicto: **no lo genera un modelo de lenguaje**, es una síntesis determinista y auditable del consenso de cinco clasificadores —misma entrada, mismo resultado, siempre— y nunca rebaja la urgencia. Segunda, el diagnóstico es **jerárquico y coherente**: familia, subcategoría y diagnóstico, sin combinaciones imposibles —es la ontología de la investigación garantizando sentido clínico. Y tercera, cuando los módulos discrepan, el sistema **lo dice**: no oculta la incertidumbre, la muestra y recomienda valoración presencial.

## Slide 25 — La investigación, funcionando (60 s)
**VISUAL:** Cascada U-Net → MedSAM2 (segmentación) + casos similares del archivo (M4-bis, imagen→imagen).
**LOCUCIÓN:**
> Aquí veis la investigación funcionando. La segmentación aplica el hallazgo de que **lo que manda es la caja**: una U-Net localiza la lesión y MedSAM2 traza la máscara, que el clínico acepta o corrige. Y el sistema recupera **casos parecidos del propio archivo de la Dra. Taberner**, por similitud visual, devolviendo casos reales con su diagnóstico y su texto. Un detalle coherente con lo que conté: aquí desplegamos la búsqueda imagen-imagen, no la contrastiva por texto —porque esa todavía no generaliza. La investigación decide qué se despliega.

## Slide 26 — Explicabilidad y seguridad clínica (60 s)
**VISUAL:** M5: 3 modos + guardarraíl "la urgencia nunca baja por IA" + RAG con citas + 7 puntos (Argenziano).
**LOCUCIÓN:**
> Sobre ese veredicto, un modelo de lenguaje añade el razonamiento clínico —pero con una regla innegociable: **la IA puede subir la urgencia, nunca bajarla**; asiste, no decide, y si no hay claridad vuelve al veredicto determinista. El asistente responde con recuperación aumentada sobre el archivo, **citando siempre sus fuentes**, y declina si no tiene contexto. Y sobre dermatoscopia aplica la Lista de los Siete Puntos con la puntuación de Argenziano. La idea clave: el sistema está diseñado con criterios de **seguridad clínica y trazabilidad**, no solo de precisión.

## Slide 27 — El experto en el bucle (30 s)
**VISUAL:** Annotation Studio → aprendizaje activo.
**LOCUCIÓN:**
> Y el círculo se cierra con el experto: la Dra. Taberner valida y anota cada caso, y esas correcciones realimentan el entrenamiento. El sistema no pretende sustituir al dermatólogo: aprende de él. *(pausa)* Y ahora, en lugar de más capturas, os lo enseño **funcionando en directo**.

## Slide 28 — ★ DEMOSTRACIÓN EN VIVO (5-6 min)
**Antes de empezar:** cambia de las diapositivas al **navegador ya abierto en dermapixel.eu** (sesión iniciada). Ten el **vídeo backup** en una pestaña contigua y el **móvil desbloqueado** con la foto lista.
**Frase de entrada:** *"Voy a hacer exactamente lo que haría un dermatólogo."*

**FLUJO A — Análisis web (~2,5 min):**
1. **Subo** una imagen de melanoma (`demo_1_melanoma.jpg`).
2. El sistema **segmenta** la lesión → señalo la máscara automática.
3. Aparece el **veredicto** → señalo: consenso de 5 clasificadores + diagnóstico jerárquico L1/L2/L3 (y el banner de discrepancia si sale: "muestra la incertidumbre").
4. Abro **casos similares** → casos reales del archivo con su diagnóstico y texto.
5. Abro el **razonamiento clínico** → el LLM explica, con citas.

**FLUJO B — Voz + móvil (~3 min · lo que NO se ve en el vídeo):**
6. Activo el **canal de voz**. Por voz: *"¿Qué medicación se utiliza para el melanoma?"* → el sistema responde (razonamiento + fuentes citadas).
7. Por voz: *"Quiero enviar una foto."* → el sistema **abre un formulario y sincroniza con el móvil** (QR / enlace).
8. Desde el **móvil**, envío la foto de la lesión.
9. El sistema **recibe la foto, la analiza y devuelve el diagnóstico** en el mismo hilo. Remate: *"Esto es lo que ve el médico, esté donde esté."*

**Cierre de la demo (frase puente):** *"Y todo lo que acabáis de ver usa, por dentro, los mismos modelos que he evaluado en la primera parte."* → volver a las diapositivas (Slide 29).

**★ RED DE SEGURIDAD (imprescindible):**
- **Backup grabado** de este flujo exacto, abierto en pestaña contigua. Si a los ~10 s algo no responde: *"os lo enseño con una grabación que hice antes"* → saltar al vídeo. Sin dramatismo.
- **Hotspot 4G/5G propio** (nunca el wifi de la sala). Prototipo pre-cargado y con sesión. Micro probado en esa sala.
- Si la **voz** falla: hago solo el Flujo A y **comento** el B con una captura. La demo no depende de un solo canal.
- **Cronometrar ≤ 6 min.** Ensayar el flujo completo ≥10 veces.

## RUNBOOK de pre-vuelo (los 10 min antes de entrar)
- [ ] Hotspot propio encendido y probado; portátil y móvil conectados a él.
- [ ] dermapixel.eu abierto, sesión iniciada, en la vista de subir imagen.
- [ ] Vídeo backup abierto en pestaña contigua (posición 0:00).
- [ ] Móvil desbloqueado, brillo alto, con `demo_1_melanoma.jpg` accesible; notificaciones en silencio.
- [ ] Micrófono probado en la sala (una prueba de voz real).
- [ ] Volumen del portátil audible; segunda pantalla/espejo comprobado.
- [ ] Plan B decidido en voz alta: qué frase digo y a qué salto si falla.

## Slide 28B — Líneas futuras (55 s) · el futuro es el dato
**VISUAL:** Cinco líneas numeradas 01–05: **Explotar los conceptos** (SAE + matriz de Rosa → Concept Bottleneck) · **Datos propios de procedencia conocida** (banco HUSLL, preentrenar sobre datos controlados, no LoRA sobre corpus web opaco) · **Un modelo por tarea** (curar datos por tarea, no un monolito) · **IA agéntica clínica** (agentes especializados, razonamiento en 2 pasos del dermatólogo, estilo Anthropic/AMIE-DeepMind) · **Desarrollo de Dermapixel** (de prototipo a producto validado: despliegue, validación prospectiva, marcado CE). Cierre: *"mejores datos para cada tarea — el límite ya no es el modelo"*.
**LOCUCIÓN:**
> Y esto abre las líneas futuras, todas en la misma dirección: el dato. Primera, **explotar los conceptos**: llevar el Sparse Autoencoder y la matriz de la Dra. Taberner a un Concept Bottleneck operativo, un diagnóstico que razona con conceptos que el clínico puede inspeccionar. Segunda, **datos propios de procedencia conocida**: construir el corpus del banco del hospital en español, con trazabilidad total, y preentrenar sobre datos controlados, en lugar de solo adaptar con LoRA sobre un corpus web opaco. Tercera, **un modelo por tarea**: detectar y curar los datos específicos de cada tarea y entrenar el mejor modelo para cada una, en vez de un único modelo monolítico. Cuarta, **IA agéntica clínica**: agentes especializados, verificables y combinados bajo control del médico, que reproducen el razonamiento en dos pasos del dermatólogo —localizar y describir primero, decidir después—, en la línea de los sistemas multiagente de Anthropic o AMIE de DeepMind. Y quinta, el **desarrollo del propio Dermapixel**: llevarlo de prototipo a producto clínico validado, con despliegue hospitalario, validación prospectiva y ruta a marcado CE. Todas comparten la misma conclusión: el límite ya no es el modelo, es el dato.
*(Puente natural al cierre: enlaza "el límite es el dato" con la reflexión final.)*

## Slide 29 — Cierre (110 s) · una historia, no un resumen
**VISUAL:** Minimal. Beca AEDV (10.000 €, *validación externa*) · 4 agradecimientos · y, resaltada, la frase final: **"Ningún modelo, en la actualidad, sustituye a unos datos de calidad, ni al conocimiento del especialista que los construye."** (Sin resumen del índice.)
**LOCUCIÓN:**
> **[Impacto]** Antes de terminar, me gustaría comentar que este proyecto ha recibido la **Beca de Innovación e Inteligencia Artificial de la Academia Española de Dermatología**, dotada con diez mil euros para continuar su desarrollo y llevarlo hacia producción clínica. Lo digo no como un premio personal, sino como una **validación externa** de que esta línea merece la pena.
>
> **[Futuro]** Y, curiosamente, todas las líneas futuras apuntan en la misma dirección: **disponer de mejores datos**. Más casos en español, más validación clínica prospectiva, y una mayor integración con el banco de imágenes del hospital para seguir mejorando los modelos y su capacidad de explicación.
>
> **[Agradecimientos]** Quiero agradecer al Dr. Javier Varona la dirección de este trabajo; a la Dra. Rosa Taberner, su confianza y el archivo clínico que ha hecho posible DermapixelAI; al Dr. Siyuan Yan, por publicar PanDerm y DermLIP como modelos abiertos; y al Dr. Alex Llambrich, por su colaboración en el nuevo dataset.
>
> **[Reflexión personal]** Y permítanme terminar con una reflexión personal. *(pausa)* Cuando empecé este trabajo pensaba que la pregunta era cuál era el mejor modelo fundacional. Después de más de un año comparándolos, creo que la pregunta correcta es otra. *(pausa)* ¿Cómo construimos mejores datos para que todos esos modelos puedan ayudar de verdad a los clínicos? *(pausa)*
>
> **[Cierre]** La tecnología seguirá cambiando muy deprisa: probablemente dentro de dos años existan modelos mejores que PanDerm o DermLIP. Pero creo que la conclusión principal de este trabajo seguirá siendo válida: **ningún modelo, en la actualidad, sustituye a unos datos de calidad, ni al conocimiento del especialista que los construye.** *(pausa)* Muchas gracias por su atención. Quedo a su disposición para las preguntas.
*(★ Últimas palabras: NO se repite el take-home literal —ya se dijo en la 21—. Se cierra con la idea universal + humana. Dilo todo despacio, con las pausas marcadas; que la última frase no vaya sobre PanDerm ni AUROC, sino sobre lo que has aprendido.)*

---

## Resumen de tiempos
- Parte A · investigación (slides 1–21): ≈ 20 min
- Parte B · prototipo (slides 22–27): ≈ 4 min
- **Demo en vivo (slide 28):** ≈ 5-6 min
- Cierre (slide 29): ≈ 1,5 min
- **Total ≈ 30 min.**

## Palancas para ajustar
- **Si acotan a 20 min:** funde 12+13 (fine-tuning + etiquetas), 14+15 (segmentación); en la Parte B, salta la demo en vivo y usa el **vídeo** en su lugar (2-3 min), fundiendo 24-26.
- **Si la demo se complica el día D:** salta directamente al vídeo backup (slide 28 lo contempla) —no pierdes nada del relato.
- **Si sobra tiempo:** alarga la demo (más módulos en vivo) o añade una slide de "matriz dermatoscópica de Rosa" ampliada.

## Preguntas probables del tribunal (prepara respuesta de 30 s)
- *¿Por qué no DermFM-Zero / modelos cerrados?* → reproducibilidad + integración hospitalaria; pesos no públicos; los cerrados entran como comparadores por API.
- *¿"El primer recurso en español"?* → el primero **de este tipo**: fotografía clínica en español con texto narrativo de caso real (la memoria lo documenta como inexistente).
- *Semilla única / potencia estadística* → asumido como limitación; el cierre formal (DeLong) se reserva a Fitzpatrick17k, único endpoint con positivos suficientes.
- *Solapamiento Derm1M* → auditoría MD5; solo Dermnet contaminado (100%); por eso su zero-shot se lee con cautela.
- *¿El prototipo está validado clínicamente?* → no; es un prototipo en producción, sin cohorte prospectiva ni marcado CE; es la línea de futuro.
- *Eso del Dr. Llambrich / escalar datos, ¿está en la memoria?* → "No: es trabajo posterior al depósito, ya en el marco del doctorado, y por eso lo presento explícitamente como preliminar y fuera del alcance evaluado. Lo menciono porque confirma la hipótesis de la memoria —al añadir datos, la clasificación mejora, pero la recuperación por texto en español todavía no—, es decir, el límite es la cantidad y diversidad de datos clínicos en español, no el método. El dataset del Dr. Llambrich se cedió únicamente para entrenamiento."
- *¿Por qué la AUROC satura con pocas etiquetas pero la balanced accuracy sigue subiendo?* → "La AUROC mide la capacidad de **ordenar**: si las imágenes de una clase reciben más probabilidad que las que no lo son, con independencia del umbral. Como PanDerm ya separa bien las lesiones en el espacio de embeddings, esa capacidad de ordenar es alta con muy pocos ejemplos. La balanced accuracy, en cambio, es el **recall medio por clase**, y da el mismo peso a cada clase: con el 1–5% de los datos, una clase rara puede tener 0, 1 o 2 ejemplos útiles, así que el clasificador lineal aprende bien las clases frecuentes pero falla las raras —lo que apenas afecta a la AUROC ni a la accuracy global, pero hunde la balanced accuracy. En una frase: la AUROC dice que la representación ya contiene información discriminativa con muy pocas etiquetas; la balanced accuracy recuerda que, para reconocer bien las clases minoritarias, no basta con una buena representación: hacen falta suficientes ejemplos etiquetados de esas clases."
- *¿Qué hiciste en histopatología?* → "Entra de forma marginal: solo como una prueba de transferencia en linear probe, sobre un dataset de parches WSI —donde, por cierto, PanDerm alcanza una AUROC de 0,99, mostrando que la representación transfiere incluso a tejido teñido. No hice fine-tuning, ni segmentación, ni zero-shot en histopatología; no era el foco. El foco es la fotografía clínica."
- *¿Y la fusión clínica + dermatoscopia? / ¿cuál sería un siguiente paso?* → "Una de las primeras líneas sería precisamente explotar la información complementaria de la fotografía clínica y la dermatoscopia mediante modelos multimodales. DermapixelAI ya incorpora algunos casos con ambas modalidades, así que la infraestructura y el dato empiezan a estar preparados para esa evolución. No diseñé experimentos de fusión en este trabajo, por eso no afirmo haberla evaluado —queda como trabajo futuro." *(Encaja con la filosofía del TFG: construir una base sólida para investigaciones futuras, no solo comparar modelos.)*

---

## PROMPT para la Parte 2 (generar el PowerPoint / web-deck)
> Genera una presentación de ~28 diapositivas a partir de este guion (`GUION_DEFENSA_TFG.md`), con el **mismo diseño visual que la landing** de dermapixel.eu / el repo (tipografía, paleta ink/neutros, estilo editorial minimalista, reglas finas, numeración de índice). Formato: **HTML autocontenido tipo slides** (una sección por diapositiva, navegable con teclado, 16:9), para mostrar en navegador y exportar a PDF/PPTX. Cada diapositiva: título, los elementos VISUAL del guion como bullets/figuras, y las notas de LOCUCIÓN en las *speaker notes* (no visibles en pantalla). La **slide 28 es una demostración en vivo**: hazla una diapositiva-portada sobria ("Demostración en vivo") con el runbook solo en las notas. Usa las capturas del prototipo de `screenshots/` para la Parte B y las figuras de resultados (`fig_lp_per_dataset`, `fig_seg_examples`, `fig_llm_comparison`, `figura_fairness_5models`) para la Parte A. Mantén 1-2 cifras por slide, sin saturar. Marca visualmente las slides 4, 21 y 29 (mensaje para llevarse).
