import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="1B365D"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
                <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
                <w:left w:val="none"/>
                <w:right w:val="none"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/>
                <w:insideV w:val="none"/>
            </w:tblBorders>
        ''')
        tblPr[0].append(borders)

doc = Document()

# Page Margins
for section in doc.sections:
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.6)
    section.right_margin = Inches(0.6)

# Header Paragraph
p_hdr = doc.add_paragraph()
p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_hdr.paragraph_format.space_after = Pt(2)
p_hdr.paragraph_format.space_before = Pt(0)

r = p_hdr.add_run("COLEGIO SAN FRANCISCO JAVIER\n")
r.bold = True
r.font.size = Pt(11)
r.font.color.rgb = RGBColor(27, 54, 93)

r = p_hdr.add_run("DEPARTAMENTO DE CIENCIAS — FÍSICA Y ASTRONOMÍA\n")
r.bold = True
r.font.size = Pt(9)
r.font.color.rgb = RGBColor(100, 100, 100)

p_t = doc.add_paragraph()
p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_t.paragraph_format.space_after = Pt(2)
p_t.paragraph_format.space_before = Pt(2)

r = p_t.add_run("PRUEBA UNIDAD 3: \"EL UNIVERSO\" (FORMA B)")
r.bold = True
r.font.size = Pt(12.5)
r.font.color.rgb = RGBColor(27, 54, 93)

p_st = doc.add_paragraph()
p_st.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_st.paragraph_format.space_after = Pt(6)

r = p_st.add_run("Estructuras y distancias cósmicas — Origen y evolución del universo — Ciclo estelar")
r.italic = True
r.font.size = Pt(9)
r.font.color.rgb = RGBColor(90, 90, 90)

# Metadata Table
table_meta = doc.add_table(rows=3, cols=4)
table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(table_meta, "1B365D")

meta_fields = [
    [("NOMBRE:", True), ("", False), ("PUNTAJE ESPERADO:", True), ("25 PUNTOS", True)],
    [("CURSO:", True), ("", False), ("PUNTAJE OBTENIDO:", True), ("", False)],
    [("FECHA:", True), ("___ / ___ / 2026", False), ("NOTA:", True), ("", False)]
]

for row_idx, row in enumerate(meta_fields):
    for col_idx, (text, is_bold) in enumerate(row):
        cell = table_meta.rows[row_idx].cells[col_idx]
        set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        r = p.add_run(text)
        r.font.size = Pt(8.5)
        r.font.name = "Calibri"
        if is_bold:
            r.bold = True
            r.font.color.rgb = RGBColor(27, 54, 93)
            if col_idx in [0, 2]:
                set_cell_background(cell, "F0F4F8")

widths = [Inches(1.3), Inches(2.5), Inches(1.8), Inches(1.4)]
for row in table_meta.rows:
    for idx, w in enumerate(widths):
        row.cells[idx].width = w

doc.add_paragraph().paragraph_format.space_after = Pt(3)

# Objectives and Instructions Table
table_info = doc.add_table(rows=1, cols=2)
table_info.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(table_info, "CCCCCC")

c0 = table_info.rows[0].cells[0]
c0.width = Inches(4.2)
set_cell_background(c0, "FAFAFA")
set_cell_margins(c0, top=60, bottom=60, left=80, right=80)

p0 = c0.paragraphs[0]
p0.paragraph_format.space_after = Pt(2)
r = p0.add_run("OBJETIVOS DE APRENDIZAJE:\n")
r.bold = True
r.font.size = Pt(8.5)
r.font.color.rgb = RGBColor(27, 54, 93)

r = p0.add_run(
    "• Evaluar la comprensión de las estructuras cósmicas, unidades astronómicas (UA, ly, pc) y jerarquía del universo.\n"
    "• Analizar la teoría del Big Bang, corrimiento al rojo (redshift), CMB y nucleosíntesis primordial.\n"
    "• Explicar las etapas del ciclo estelar, equilibrio hidrostático y remanentes finales según la masa."
)
r.font.size = Pt(8)

c1 = table_info.rows[0].cells[1]
c1.width = Inches(2.8)
set_cell_background(c1, "FAFAFA")
set_cell_margins(c1, top=60, bottom=60, left=80, right=80)

p1 = c1.paragraphs[0]
p1.paragraph_format.space_after = Pt(2)
r = p1.add_run("INSTRUCCIONES GENERALES:\n")
r.bold = True
r.font.size = Pt(8.5)
r.font.color.rgb = RGBColor(27, 54, 93)

r = p1.add_run(
    "1. Lea atentamente cada pregunta y marque solo UNA alternativa.\n"
    "2. Tiempo disponible: 70 minutos.\n"
    "3. Responder únicamente con lápiz pasta azul o negro.\n"
    "4. En preguntas con cálculo, incluya el procedimiento al costado.\n"
    "5. Nota 4,0 se asigna al 60% (15 puntos)."
)
r.font.size = Pt(8)

doc.add_paragraph().paragraph_format.space_after = Pt(3)

# Grade Scale Table
table_scale = doc.add_table(rows=2, cols=13)
table_scale.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(table_scale, "CCCCCC")

# Set Scale values
pts_row = ["Pts"] + [str(i) for i in [0, 2, 4, 6, 8, 10, 12, 14, 15, 18, 21, 25]]
nota_row = ["Nota"] + ["1.0", "1.6", "2.2", "2.8", "3.4", "3.8", "3.9", "4.0", "4.9", "5.8", "7.0"]

for c_idx in range(13):
    cell_p = table_scale.rows[0].cells[c_idx]
    cell_n = table_scale.rows[1].cells[c_idx]
    
    set_cell_margins(cell_p, top=30, bottom=30, left=30, right=30)
    set_cell_margins(cell_n, top=30, bottom=30, left=30, right=30)
    
    set_cell_background(cell_p, "F0F4F8")
    
    pp = cell_p.paragraphs[0]
    pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rp = pp.add_run(pts_row[c_idx] if c_idx < len(pts_row) else "")
    rp.font.size = Pt(7.5)
    rp.bold = True
    rp.font.color.rgb = RGBColor(27, 54, 93)
    
    pn = cell_n.paragraphs[0]
    pn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rn = pn.add_run(nota_row[c_idx] if c_idx < len(nota_row) else "")
    rn.font.size = Pt(7.5)

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# Section Title Builder
def add_sec_title(title, pts=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    
    r = p.add_run(title)
    r.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(27, 54, 93)
    
    if pts:
        r_pts = p.add_run(f" ({pts})")
        r_pts.bold = True
        r_pts.font.size = Pt(10)
        r_pts.font.color.rgb = RGBColor(180, 50, 50)

# MCQ Builder
def add_mcq(num, q_text, opts, is_calc=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.keep_with_next = True
    
    r1 = p.add_run(f"{num}. ")
    r1.bold = True
    r1.font.size = Pt(9)
    r1.font.color.rgb = RGBColor(27, 54, 93)
    
    if is_calc:
        r_calc = p.add_run("[ 🧮 CÁLCULO ] ")
        r_calc.bold = True
        r_calc.font.size = Pt(8.5)
        r_calc.font.color.rgb = RGBColor(180, 50, 50)
        
    r2 = p.add_run(q_text)
    r2.font.size = Pt(9)
    
    for let, text in opts:
        po = doc.add_paragraph()
        po.paragraph_format.left_indent = Inches(0.25)
        po.paragraph_format.space_before = Pt(0.5)
        po.paragraph_format.space_after = Pt(0.5)
        po.paragraph_format.keep_with_next = True
        
        ro1 = po.add_run(f"{let}) ")
        ro1.bold = True
        ro1.font.size = Pt(8.5)
        
        ro2 = po.add_run(text)
        ro2.font.size = Pt(8.5)

# --- ÍTEM SELECCIÓN MÚLTIPLE (25 PUNTOS) ---
add_sec_title("ÍTEM SELECCIÓN MÚLTIPLE", "25 PUNTOS")

p_inst_item = doc.add_paragraph()
p_inst_item.paragraph_format.space_after = Pt(4)
r = p_inst_item.add_run("Marca la alternativa que consideres correcta. Cada pregunta equivale a 1 punto. En las preguntas señaladas con [ 🧮 CÁLCULO ], adjunta el desarrollo matemático al costado o en hoja de borrador.")
r.font.size = Pt(8.5)
r.italic = True

mcq_questions = [
    (1, "¿Cuál de las siguientes opciones ordena correctamente las estructuras del cosmos en sentido ASCENDENTE (de menor a mayor escala espacial)?",
     [("A", "Planeta → Estrella → Galaxia → Cúmulo de galaxias → Supercúmulo"),
      ("B", "Estrella → Planeta → Cúmulo de galaxias → Galaxia → Supercúmulo"),
      ("C", "Planeta → Cúmulo de galaxias → Galaxia → Estrella → Supercúmulo"),
      ("D", "Supercúmulo → Cúmulo de galaxias → Galaxia → Estrella → Planeta")], False),

    (2, "¿Qué estructura cósmica está constituida por un conjunto de galaxias unidas entre sí por la acción de su propia atracción gravitacional?",
     [("A", "Nebulosa planetaria"),
      ("B", "Cúmulo de galaxias"),
      ("C", "Sistema planetario"),
      ("D", "Protoestrella")], False),

    (3, "Un astrónomo desea medir la distancia promedio entre el Sol y el planeta Neptuno (~4.500 millones de kilómetros). ¿Cuál es la unidad de medida astronómica más idónea y práctica para expresar esta escala interplanetaria?",
     [("A", "Parsec (pc)"),
      ("B", "Año luz (ly)"),
      ("C", "Unidad Astronómica (UA)"),
      ("D", "Kilómetros enteros sin notación científica")], False),

    (4, "La estrella Alfa Centauri B se ubica a una distancia aproximada de 4,37 años luz de la Tierra. Si aplicas la constante de conversión 1 ly ≈ 9,46 × 10¹² km, ¿cuál es la distancia de Alfa Centauri B expresada en kilómetros en notación científica?",
     [("A", "4,13 × 10¹³ km"),
      ("B", "4,13 × 10¹² km"),
      ("C", "9,46 × 10¹³ km"),
      ("D", "4,37 × 10¹¹ km")], True),

    (5, "¿Cuál de los siguientes grupos representa a los planetas gaseosos o gigantes jovianos del Sistema Solar ordenados en forma creciente según su distancia desde el Sol?",
     [("A", "Mercurio, Venus, Tierra, Marte"),
      ("B", "Júpiter, Saturno, Urano, Neptuno"),
      ("C", "Saturno, Júpiter, Neptuno, Urano"),
      ("D", "Tierra, Marte, Júpiter, Saturno")], False),

    (6, "La luz emitida por el Sol tarda aproximadamente 8,3 minutos en recorrer 1 UA hasta la Tierra. Si una sonda espacial explora el planeta Marte a una distancia de 1,5 UA del Sol, ¿cuánto tiempo tarda la luz solar en alcanzar dicho planeta?",
     [("A", "8,3 minutos"),
      ("B", "12,45 minutos"),
      ("C", "16,6 minutos"),
      ("D", "24,9 minutos")], True),

    (7, "¿Cuál es el postulado central que describe la Teoría del Big Bang respecto al origen y desarrollo del Universo?",
     [("A", "El Universo ha permanecido estático e inmutable en estado estacionario desde el infinito."),
      ("B", "El Universo se originó a partir de una condición inicial extremadamente densa y caliente, experimentando una expansión continua del espacio."),
      ("C", "Los planetas y estrellas se forman continuamente a partir del colapso instantáneo de agujeros negros primordiales."),
      ("D", "El Sistema Solar es el centro físico de una explosión gravitacional en constante contracción.")], False),

    (8, "¿Qué observación astronómica decisiva realizada por Edwin Hubble proporcionó la evidencia empírica directa de que el Universo se está expandiendo?",
     [("A", "El corrimiento hacia el rojo (redshift) en las líneas espectrales de galaxias lejanas."),
      ("B", "La existencia de manchas y erupciones en la superficie solar."),
      ("C", "El descubrimiento de cráteres de impacto en la Luna y Marte."),
      ("D", "La presencia de anillos formados por hielo alrededor de Saturno.")], False),

    (9, "Un análisis espectroscópico de una galaxia en el espacio profundo muestra que sus líneas de absorción están desplazadas hacia longitudes de onda más largas (frecuencias más bajas). ¿Cómo se explica físicamente este fenómeno?",
     [("A", "La galaxia se mueve rápidamente hacia la Tierra comprimiendo sus ondas de luz."),
      ("B", "El tejido del espacio intergaláctico se está expandiendo, alejando a la galaxia y estirando la longitud de onda de la luz recibida."),
      ("C", "La galaxia está colapsando bajo su propia gravedad para convertirse en un agujero negro."),
      ("D", "La luz de la galaxia ha perdido su temperatura al atravesar la atmósfera terrestre.")], False),

    (10, "Observaciones astrofísicas revelan que la galaxia de Andrómeda presenta un corrimiento hacia el azul (blueshift) respecto a la Vía Láctea. ¿Cómo se interpreta correctamente este dato dentro del marco cosmológico actual?",
     [("A", "Refuta la teoría del Big Bang, demostrando que el Universo en su conjunto se está contrayendo."),
      ("B", "Es un caso particular donde la atracción gravitacional mutua entre galaxias cercanas supera la velocidad de expansión del espacio a escala local."),
      ("C", "Demuestra que la luz en Andrómeda viaja a una velocidad muy superior a 300.000 km/s."),
      ("D", "Indica que Andrómeda está compuesta exclusivamente por estrellas enanas blancas de alta frecuencia.")], False),

    (11, "Durante una investigación se registran dos galaxias distantes: la Galaxia 'A' con una velocidad de recesión de 2.000 km/s y la Galaxia 'B' con una velocidad de recesión de 8.000 km/s. De acuerdo con la Ley de Hubble-Lemaître (v = H₀ · d), ¿qué se deduce sobre sus distancias desde la Tierra?",
     [("A", "La Galaxia 'A' está cuatro veces más lejos que la Galaxia 'B'."),
      ("B", "La Galaxia 'B' se encuentra cuatro veces más distante de la Tierra que la Galaxia 'A'."),
      ("C", "Ambas galaxias están situadas a la misma distancia de la Tierra."),
      ("D", "La Galaxia 'B' se está acercando a la Tierra cuatro veces más rápido que la Galaxia 'A'.")], True),

    (12, "¿Qué es la Radiación de Fondo de Microondas (CMB)?",
     [("A", "La luz brillante emitida por las estrellas jóvenes recién nacidas en las nebulosas."),
      ("B", "El remanente térmico fotosférico o 'luz fósil' liberado cuando el Universo primitivo tenía ~380.000 años y se volvió transparente a los fotones."),
      ("C", "La radiación de alta energía emitida continuamente por la rotación de los agujeros negros supermasivos."),
      ("D", "Las ondas de radio emitidas por los núcleos de hierro de los planetas telúricos.")], False),

    (13, "La radiación CMB fue emitida originalmente a una temperatura cercana a los 3.000 K (luz visible e infrarroja). Hoy en día es detectada en el rango de microondas a una temperatura de 2,725 K. ¿A qué mecanismo físico se debe esta severa disminución térmica?",
     [("A", "Los fotones perdieron masa por colisionar contra el polvo estelar intergaláctico."),
      ("B", "El estiramiento continuo del espacio debido a la expansión del Universo aumentó la longitud de onda de los fotones, reduciendo su energía y temperatura equivalente."),
      ("C", "El calor inicial fue absorbido por la formación de enanas blancas en el Universo temprano."),
      ("D", "La materia oscura congeló los fotones a medida que se formaban las primeras galaxias.")], False),

    (14, "Durante la nucleosíntesis primordial (ocurrida en los primeros 3 minutos tras el Big Bang), el Universo produjo principalmente Hidrógeno (~75%) y Helio (~25%). ¿Por qué este proceso fue INCAPAZ de sintetizar elementos más pesados como Carbono (C) u Oxígeno (O)?",
     [("A", "Porque no existían protones ni neutrones en el plasma primordial."),
      ("B", "Porque la rápida expansión provocó un veloz descenso en la temperatura y densidad del Universo, impidiendo que ocurrieran reacciones de fusión nuclear más complejas."),
      ("C", "Porque la fuerza de gravedad era tan elevada que colapsó todos los núcleos pesados en agujeros negros."),
      ("D", "Porque los elementos pesados solo se forman durante el enfriamiento de las enanas blancas.")], False),

    (15, "¿En qué lugar del Universo ocurren de manera natural los procesos de nucleosíntesis estelar capaces de crear elementos químicos como el Carbono, Oxígeno, Silicio y Hierro?",
     [("A", "En las atmósferas frías de los planetas gigantes gaseosos."),
      ("B", "En el interior caliente y denso de las estrellas durante sus etapas de fusión nuclear."),
      ("C", "En el espacio intergaláctico vacío mediante colisiones de radiación CMB."),
      ("D", "En el núcleo de los cometas y asteroides del Sistema Solar exterior.")], False),

    (16, "¿Qué mecanismo físico interno garantiza que una estrella en la fase de Secuencia Principal mantenga un tamaño constante y estable sin colapsar ni explotar (Equilibrio Hidrostático)?",
     [("A", "El equilibrio entre la presión térmica hacia afuera (generada por la fusión nuclear de H) y la fuerza gravitacional hacia adentro (que atrae la masa)."),
      ("B", "La fuerza magnética generada por la rotación del núcleo de hierro alrededor del eje de la galaxia."),
      ("C", "El empuje de radiación procedente de la combustión química de gases en la superficie estelar."),
      ("D", "La atracción gravitacional ejercida por los planetas que orbitan a la estrella.")], False),

    (17, "¿Cuál es el combustible nuclear primario que fusionan las estrellas en su núcleo durante toda su permanencia en la Secuencia Principal?",
     [("A", "Fusión de Helio para formar Carbono"),
      ("B", "Fusión de Hidrógeno para formar Helio"),
      ("C", "Fisión nuclear de Uranio"),
      ("D", "Combustión endotérmica de Hierro")], False),

    (18, "¿Por qué las estrellas de gran masa (masivas) consumen su combustible nuclear en un período de tiempo mucho MÁS CORTO que las estrellas de masa baja como las enanas rojas?",
     [("A", "Porque las estrellas masivas contienen un porcentaje menor de hidrógeno inicial en sus núcleos."),
      ("B", "Porque su enorme masa ejerce una gravedad gigantesca, requiriendo temperaturas y presiones extremadamente altas en el núcleo que queman el combustible a tasas aceleradas."),
      ("C", "Porque las estrellas masivas no poseen núcleo y disipan su gas directamente al espacio intergaláctico."),
      ("D", "Porque se desplazan a mayor velocidad sufriendo un envejecimiento por efecto Doppler.")], False),

    (19, "¿Cuál es la secuencia evolutiva correcta para el ciclo de vida de una estrella de masa media (similar a la masa de nuestro Sol, ~1 M⊙)?",
     [("A", "Nebulosa → Protoestrella → Secuencia Principal → Gigante Roja → Nebulosa Planetaria → Enana Blanca"),
      ("B", "Nebulosa → Secuencia Principal → Supergigante Roja → Supernova → Agujero Negro"),
      ("C", "Protoestrella → Gigante Roja → Supernova → Estrella de Neutrones"),
      ("D", "Nebulosa → Enana Blanca → Secuencia Principal → Gigante Roja → Agujero Negro")], False),

    (20, "¿Qué fenómeno marca el final de la vida de una estrella de alta masa (masiva, con más de 8-10 masas solares) cuando agota todo su combustible nuclear en el núcleo?",
     [("A", "Una expansión pacífica hacia una nebulosa planetaria dejando una enana blanca."),
      ("B", "Una explosión cataclísmica violenta conocida como Supernova."),
      ("C", "La transformación paulatina de la estrella en un planeta rocoso telúrico."),
      ("D", "La condensación directa de gas en una nube de hidrógeno primordial.")], False),

    (21, "El Hierro (Fe) es considerado el 'límite de fusión' en el núcleo de una estrella masiva antes de su colapso. ¿Cuál es la razón física fundamentales de este límite?",
     [("A", "El hierro es el elemento más liviano del cosmos y flota fuera del núcleo estelar."),
      ("B", "La fusión nuclear del hierro es una reacción endotérmica (absorbe energía en lugar de liberarla), destruyendo el soporte de presión térmica que sostenía a la estrella."),
      ("C", "El hierro refleja la gravedad de la estrella impidiendo el nacimiento de neutrones."),
      ("D", "El hierro solo se sintetiza durante la fase de secuencia principal del Sol.")], False),

    (22, "¿En qué evento astronómico extremo se alcanzan las temperaturas y presiones extraordinarias requeridas para sintetizar naturalmente los elementos más pesados que el hierro (como el Oro, Platino y Uranio)?",
     [("A", "En la fase de protostar en el interior de una nebulosa fría."),
      ("B", "Durante la nucleosíntesis primordial en los primeros segundos del Big Bang."),
      ("C", "Durante las reacciones cataclísmicas de una explosión de Supernova y fusiones de estrellas de neutrones."),
      ("D", "En la superficie de una enana blanca enfriada.")], False),

    (23, "¿Qué remanente estelar extremada y densamente empacado se origina tras el colapso del núcleo de una estrella supermasiva (con masa progenitora superior a ~20-25 masas solares)?",
     [("A", "Enana blanca"),
      ("B", "Planeta telúrico"),
      ("C", "Agujero negro"),
      ("D", "Nebulosa planetaria")], False),

    (24, "Si 1 año luz (ly) equivale aproximadamente a 9,46 × 10¹² km, ¿a cuántos kilómetros corresponden 5 años luz de distancia?",
     [("A", "4,73 × 10¹² km"),
      ("B", "4,73 × 10¹³ km"),
      ("C", "9,46 × 10¹³ km"),
      ("D", "4,73 × 10¹¹ km")], True),

    (25, "¿Cuál de las siguientes descripciones representa de manera más precisa el nacimiento o génesis de una estrella?",
     [("A", "La explosión cataclísmica de una enana blanca en el espacio intergaláctico."),
      ("B", "El colapso gravitacional de regiones densas e inestables en el interior de una nebulosa de gas y polvo."),
      ("C", "El choque directo de dos planetas gigantes gaseosos en órbita solar."),
      ("D", "La condensación de la radiación CMB al enfriarse a 2,7 K.")], False)
]

for num, q_text, opts, is_calc in mcq_questions:
    add_mcq(num, q_text, opts, is_calc)

# --- PREGUNTAS OPCIONALES (ÓPTICA GEOMÉTRICA) ---
add_sec_title("PREGUNTAS OPCIONALES — ÓPTICA GEOMÉTRICA Y VISIÓN", "PUNTOS EXTRA")

p_opt_inst = doc.add_paragraph()
p_opt_inst.paragraph_format.space_after = Pt(4)
r = p_opt_inst.add_run("Las siguientes preguntas son de carácter opcional y permiten sumar puntos adicionales a la evaluación. Si el estudiante alcanza la puntuación máxima en las preguntas obligatorias, los aciertos no se contabilizan y se consideran puntos acumulativos.")
r.font.size = Pt(8.5)
r.italic = True

opt_questions = [
    (26, "Los espejos retrovisores laterales de los automóviles utilizan espejos convexos. ¿Qué tipo de imagen producen siempre estos espejos y cuál es su ventaja práctica?",
     [("A", "Imágenes reales, invertidas y de mayor tamaño que aumentan el detalle."),
      ("B", "Imágenes virtuales, derechas y reducidas que otorgan un mayor campo de visión al conductor."),
      ("C", "Imágenes reales, derechas y de igual tamaño que el objeto observado."),
      ("D", "Imágenes virtuales, invertidas y aumentadas que eliminan los puntos ciegos.")], False),

    (27, "Un objeto se coloca delante de un espejo cóncavo a una distancia mayor que el centro de curvatura (C). ¿Cuáles son las características de la imagen formada por el espejo?",
     [("A", "Real, invertida y de menor tamaño que el objeto."),
      ("B", "Virtual, derecha y de mayor tamaño."),
      ("C", "Real, derecha y de igual tamaño."),
      ("D", "Virtual, invertida y reducida.")], False),

    (28, "La miopía es un defecto visual en el cual los rayos de luz provenientes de objetos lejanos se enfocan delante de la retina. ¿Con qué tipo de lente se corrige esta condición?",
     [("A", "Lente convergente"),
      ("B", "Lente divergente"),
      ("C", "Lente cilíndrica"),
      ("D", "Espejo cóncavo")], False),

    (29, "Cuando se utiliza una lupa (lente convergente) para observar un objeto cercano ubicado entre el foco (F) y la lente, ¿qué características tiene la imagen observada?",
     [("A", "Real, invertida y reducida"),
      ("B", "Virtual, derecha y de mayor tamaño (aumentada)"),
      ("C", "Real, derecha y de igual tamaño"),
      ("D", "Virtual, invertida y reducida")], False),

    (30, "La hipermetropía ocurre cuando las imágenes de objetos cercanos se proyectan detrás de la retina. ¿Qué tipo de lente permite corregir esta anomalía en el enfoque?",
     [("A", "Lente divergente"),
      ("B", "Lente convergente"),
      ("C", "Lente cilíndrica neutra"),
      ("D", "Lente cóncava")], False)
]

for num, q_text, opts, is_calc in opt_questions:
    add_mcq(num, q_text, opts, is_calc)

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# --- AUTOEVALUACIÓN Y PAUSA RECREATIVA ---
add_sec_title("SECCIÓN DE AUTOEVALUACIÓN Y PAUSA RECREATIVA")

p_auto_hdr = doc.add_paragraph()
p_auto_hdr.paragraph_format.space_after = Pt(2)
r = p_auto_hdr.add_run("Responde con sinceridad marcando con una X según tu desempeño personal en esta unidad:")
r.font.size = Pt(8.5)

tbl_auto = doc.add_table(rows=4, cols=4)
tbl_auto.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(tbl_auto, "CCCCCC")

auto_headers = ["Indicador de Autoevaluación", "SÍ", "NO", "A VECES"]
for idx, h_text in enumerate(auto_headers):
    cell = tbl_auto.rows[0].cells[idx]
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(h_text)
    r.bold = True
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(27, 54, 93)

auto_rows = [
    "Tengo mi cuaderno al día, con toda la materia e información de la asignatura.",
    "Tengo realizadas todas mis guías de trabajo y ejercicios prácticos.",
    "Pregunto frecuentemente mis dudas al profesor durante las clases."
]

widths_auto = [Inches(4.5), Inches(0.8), Inches(0.8), Inches(0.9)]

for r_idx, row_text in enumerate(auto_rows):
    row_cells = tbl_auto.rows[r_idx+1].cells
    set_cell_margins(row_cells[0], top=40, bottom=40, left=60, right=60)
    p = row_cells[0].paragraphs[0]
    r = p.add_run(row_text)
    r.font.size = Pt(8)
    
    for c_idx in range(1, 4):
        set_cell_margins(row_cells[c_idx], top=40, bottom=40, left=40, right=40)
        p = row_cells[c_idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run("[   ]")
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(150, 150, 150)

for row in tbl_auto.rows:
    for idx, w in enumerate(widths_auto):
        row.cells[idx].width = w

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# Reflection questions
p_refl = doc.add_paragraph()
p_refl.paragraph_format.space_before = Pt(4)
p_refl.paragraph_format.space_after = Pt(2)
r = p_refl.add_run("Responde a las siguientes preguntas:\n"
                   "• Las horas que dediqué a estudiar para esta prueba es: __________ hrs.\n"
                   "• La nota que obtendré en esta prueba es: __________")
r.font.size = Pt(8.5)
r.italic = True

p_relax = doc.add_paragraph()
p_relax.paragraph_format.space_before = Pt(8)
p_relax.paragraph_format.space_after = Pt(4)
p_relax.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_relax.add_run("¡SI TERMINASTE, RELÁJATE UN POCO Y REVISA TUS RESPUESTAS!")
r.bold = True
r.font.size = Pt(9)
r.font.color.rgb = RGBColor(27, 54, 93)

# Save Document
doc_path = "Evaluacion_Universo_Forma_B_Seleccion_Unica.docx"
doc.save(doc_path)
print(f"Document saved successfully as {doc_path}")