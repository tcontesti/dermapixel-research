"""Sustitución de refs a capítulos futuros en las copias _Tutor."""
import re
from pathlib import Path

# (patron_regex, reemplazo) - en reemplazo usar \\ para una sola barra
SUSTITUCIONES = [
    # Referencias a Cap2 (sí existe en la versión Tutor)
    (r"capítulo~\\ref\{cap:sota\}", "capítulo 2"),
    (r"\\ref\{cap:sota\}", "2"),

    # Capítulos futuros NO incluidos
    (r"capítulo~\\ref\{cap:metodos\}",
     "capítulo \\\\emph{Materiales y métodos} (en preparación)"),
    (r"capítulo~\\ref\{cap:resultados\}",
     "capítulo \\\\emph{Resultados} (en preparación)"),
    (r"capítulo~\\ref\{cap:discusion\}",
     "capítulo \\\\emph{Discusión} (en preparación)"),
    (r"capítulo~\\ref\{cap:limitaciones\}",
     "capítulo \\\\emph{Limitaciones} (en preparación)"),
    (r"capítulo~\\ref\{cap:conclusiones\}",
     "capítulo \\\\emph{Conclusiones} (en preparación)"),
    (r"capítulos~\\ref\{cap:resultados\} y~\\ref\{cap:anexoj\}",
     "capítulos \\\\emph{Resultados} y \\\\emph{Trabajo futuro} (en preparación)"),

    # Secciones del Cap7 (futuras)
    (r"secci\\'on~\\ref\{sec:lineas-abiertas\} del\s*\n?\s*capítulo~\\ref\{cap:conclusiones\}",
     "apartado \\\\emph{Líneas de investigación abiertas} (en preparación)"),
    (r"secci\\'on~\\ref\{sec:lineas-abiertas\}",
     "apartado \\\\emph{Líneas de investigación abiertas} (en preparación)"),

    # Anexos (todos futuros)
    (r"Anexos~\\ref\{cap:anexoa\}--?\\ref\{cap:anexoe\}",
     "Anexos A--E (en preparación)"),
    (r"Anexos~\\ref\{cap:anexof\}--?\\ref\{cap:anexoi\}",
     "Anexos F--I (en preparación)"),
    (r"Anexos~\\ref\{cap:anexof\}--?\\ref\{cap:anexoh\}",
     "Anexos F--H (en preparación)"),

    (r"Anexo~\\ref\{cap:anexoa\}",
     "Anexo \\\\emph{Tareas y reproducibilidad} (en preparación)"),
    (r"Anexo~\\ref\{cap:anexob\}",
     "Anexo \\\\emph{Tablas extendidas} (en preparación)"),
    (r"Anexo~\\ref\{cap:anexoc\}",
     "Anexo \\\\emph{Pipeline DermapixelAI} (en preparación)"),
    (r"Anexo~\\ref\{cap:anexod\}",
     "Anexo \\\\emph{Declaración uso IA} (en preparación)"),
    (r"Anexo~\\ref\{cap:anexoe\}",
     "Anexo \\\\emph{Entrega del dataset} (en preparación)"),
    (r"Anexo~\\ref\{cap:anexof\}",
     "Anexo \\\\emph{SAE y conceptos clínicos} (en preparación)"),
    (r"Anexo~\\ref\{cap:anexog\}",
     "Anexo \\\\emph{Comparación LLM extendida} (en preparación)"),
    (r"Anexo~\\ref\{cap:anexoh\}",
     "Anexo \\\\emph{Prototipo DermApIxel} (en preparación)"),

    # Secciones del Cap3 (futuras)
    (r"secci\\'on~\\ref\{sec:dermapixel\}",
     "apartado \\\\emph{Dataset DermapixelAI} (en preparación)"),
    (r"secci\\'on~\\ref\{sec:ontologia\}",
     "apartado \\\\emph{Ontología L1/L2/L3} (en preparación)"),
    (r"secci\\'on~\\ref\{sec:auditoria\}",
     "apartado \\\\emph{Auditoría de solapamiento} (en preparación)"),
]

for fname in ["Cap1_Introduccion_Tutor.tex", "Cap2_EstadoArte_Tutor.tex"]:
    p = Path(fname)
    if not p.exists():
        print(f"NO existe {fname}")
        continue
    s = p.read_text(encoding="utf-8")
    cnt = 0
    for pat, repl in SUSTITUCIONES:
        s, n = re.subn(pat, repl, s)
        cnt += n
    p.write_text(s, encoding="utf-8")
    print(f"{fname}: {cnt} sustituciones")
