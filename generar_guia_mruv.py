from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_cell_border(cell):
    """
    Helper function to set borders for a table cell.
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    # Add borders
    for border in ['top', 'bottom', 'left', 'right']:
        tag = f'w:{border}'
        element = OxmlElement(tag)
        element.set(qn('w:val'), 'single')
        element.set(qn('w:sz'), '4')
        element.set(qn('w:color'), 'auto')
        tcPr.append(element)

def generar_guia_mruv():
    # Datos de la guía (Contenido Pedagógico)
    datos = {
        "institucion": "Colegio de Excelencia Científica",
        "asignatura": "Física",
        "curso": "2do Medio / 11vo Grado",
        "fecha": "Junio 2026",
        "oa": "Comprender el Movimiento Rectilíneo Uniformemente Variado (MRUV), identificando la presencia de aceleración constante, interpretando gráficos posición–tiempo y velocidad–tiempo, y aplicando las ecuaciones fundamentales para describir y analizar el movimiento.",
        "instrucciones": "Lea atentamente cada sección. Utilice lápiz mina para los cálculos y pluma para las respuestas finales. No olvide incluir las unidades de medida en cada resultado.",

        "inicio": {
            "contexto": "Imagina que estás en el asiento del copiloto de un auto detenido en un semáforo. De repente, la luz cambia a verde y el conductor pisa el acelerador con fuerza. Sientes que tu cuerpo es empujado hacia el respaldo del asiento.",
            "pregunta": "¿Qué diferencia sientes en tu cuerpo cuando el auto arranca versus cuando viaja a una velocidad constante en la autopista? ¿Cómo describirías el cambio de velocidad en términos de 'aceleración'?"
        },

        "nivel_facil": [
            {"enunciado": "Un automóvil parte del reposo y alcanza una velocidad de 20 m/s en 4 segundos. ¿Cuál es la aceleración del vehículo?", "espacio": 3},
            {"enunciado": "Un objeto se desplaza con una aceleración constante de 2 m/s² durante 5 segundos, partiendo desde el reposo. ¿Cuál es su velocidad final?", "espacio": 3}
        ],

        "nivel_medio": [
            {
                "tipo": "grafico",
                "grafico_desc": "[INSERTAR GRÁFICO v-t: Línea recta ascendente desde (0,0) hasta (5,10)]",
                "enunciado": "Observa el gráfico de Velocidad vs Tiempo adjunto. a) Determina la aceleración del móvil mediante la pendiente. b) Calcula la distancia total recorrida usando el área bajo la curva.",
                "espacio": 5
            },
            {
                "tipo": "grafico",
                "grafico_desc": "[INSERTAR GRÁFICO x-t: Curva parabólica cóncava hacia arriba]",
                "enunciado": "Analiza la curva de Posición vs Tiempo. ¿Por qué la forma de parábola indica que el móvil tiene una aceleración constante y no una velocidad constante?",
                "espacio": 4
            }
        ],

        "nivel_dificil": [
            {"enunciado": "Un tren de alta velocidad viaja a 30 m/s y aplica los frenos produciendo una desaceleración constante de 1.5 m/s². ¿Cuánto tiempo tarda en detenerse y qué distancia de frenado recorre?", "espacio": 6},
            {"enunciado": "Dos vehículos, A y B, se mueven en la misma dirección. El vehículo A se mueve con velocidad constante de 10 m/s. El vehículo B parte del reposo con una aceleración de 0.5 m/s². Si B parte 20 metros detrás de A, ¿en cuánto tiempo y a qué distancia lo alcanzará?", "espacio": 8}
        ],

        "aplicacion": {
            "titulo": "El Desafío del Ingeniero Vial",
            "enunciado": "Estás diseñando una zona de seguridad en una carretera. Un camión de carga viaja a 80 km/h (convierte a m/s). Si el coeficiente de frenado permite una desaceleración máxima de 3 m/s², ¿cuál debe ser la longitud mínima de la pista de frenado para que el camión se detenga completamente antes de chocar con un muro?",
            "espacio": 8
        },

        "metacognicion": [
            "¿Cuál de los tres niveles de ejercicios te resultó más complejo y qué concepto específico te generó dificultad?",
            "¿En qué medida la interpretación de los gráficos te ayudó a visualizar el movimiento más allá de las fórmulas matemáticas?",
            "Si tuvieras que explicarle a un compañero la diferencia entre MRU y MRUV basándote en la aceleración, ¿cómo lo harías?"
        ]
    }

    doc = Document()

    # --- ESTILOS GENERALES ---
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(11)

    # --- 1. ENCABEZADO ---
    header = doc.add_paragraph()
    header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = header.add_run(datos["institucion"])
    run.bold = True
    run.font.size = Pt(16)

    # Tabla de Datos del Estudiante
    table_data = doc.add_table(rows=2, cols=2)
    table_data.style = 'Table Grid'
    table_data.cell(0, 0).text = f"Asignatura: {datos['asignatura']}"
    table_data.cell(0, 1).text = f"Curso: {datos['curso']}"
    table_data.cell(1, 0).text = "Estudiante: __________________________"
    table_data.cell(1, 1).text = f"Fecha: {datos['fecha']}"

    doc.add_paragraph("\n")

    # --- 2. OBJETIVO DE APRENDIZAJE ---
    doc.add_heading("Guía de Aprendizaje: Movimiento Rectilíneo Uniformemente Variado (MRUV)", level=1)

    # Recuadro para el OA
    table_oa = doc.add_table(rows=1, cols=1)
    table_oa.style = 'Table Grid'
    cell_oa = table_oa.cell(0, 0)
    cell_oa.text = f"Objetivo de Aprendizaje: {datos['oa']}"

    doc.add_paragraph(f"\nInstrucciones: {datos['instrucciones']}\n")

    # --- 3. INICIO: ACTIVACIÓN ---
    doc.add_heading("I. Activando Conocimientos", level=2)
    doc.add_paragraph(datos["inicio"]["contexto"])
    doc.add_paragraph(f"Pregunta: {datos['inicio']['pregunta']}")
    doc.add_paragraph("\n" * 3) # Espacio para respuesta

    # --- 4. DESARROLLO: EJERCICIOS ---
    doc.add_heading("II. Desarrollo y Aplicación", level=2)

    # NIVEL FÁCIL
    doc.add_heading("Nivel 1: Aplicación Directa", level=3)
    for i, ej in enumerate(datos["nivel_facil"], 1):
        doc.add_paragraph(f"{i}. {ej['enunciado']}")
        doc.add_paragraph("\n" * ej['espacio'])

    # NIVEL MEDIO
    doc.add_heading("Nivel 2: Análisis Gráfico", level=3)
    for i, ej in enumerate(datos["nivel_medio"], 1):
        doc.add_paragraph(f"{i}. {ej['enunciado']}")
        # Simulación de imagen
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_img = p_img.add_run(ej['grafico_desc'])
        run_img.italic = True
        run_img.font.color.rgb = None # Standard black

        doc.add_paragraph("\n" * ej['espacio'])

    # NIVEL DIFÍCIL
    doc.add_heading("Nivel 3: Análisis Complejo", level=3)
    for i, ej in enumerate(datos["nivel_dificil"], 1):
        doc.add_paragraph(f"{i}. {ej['enunciado']}")
        doc.add_paragraph("\n" * ej['espacio'])

    # --- 5. CIERRE: APLICACIÓN ---
    doc.add_heading("III. Desafío de Aplicación", level=2)
    p_challenge = doc.add_paragraph()
    run_ch = p_challenge.add_run(f"🚀 {datos['aplicacion']['titulo']}")
    run_ch.bold = True
    doc.add_paragraph(datos["aplicacion"]["enunciado"])
    doc.add_paragraph("\n" * datos["aplicacion"]["espacio"])

    # --- 6. METACOGNICIÓN ---
    doc.add_heading("IV. Reflexión sobre mi Aprendizaje", level=2)
    table_meta = doc.add_table(rows=len(datos["metacognicion"]), cols=1)
    table_meta.style = 'Table Grid'
    for i, question in enumerate(datos["metacognicion"]):
        cell = table_meta.cell(i, 0)
        cell.text = question
        # Agregar espacio debajo de cada pregunta dentro de la celda simulando líneas
        cell.paragraphs[0].add_run("\n\n\n")

    # --- 7. RÚBRICA ---
    doc.add_paragraph("\n")
    doc.add_heading("Criterios de Evaluación", level=2)
    rubrica_data = [
        ["Criterio", "Logrado", "En Proceso", "No Logrado"],
        ["Uso de Ecuaciones", "Aplica correctamente las fórmulas y despejes.", "Aplica fórmulas pero comete errores de despeje.", "No identifica la fórmula adecuada."],
        ["Análisis Gráfico", "Interpreta correctamente pendientes y áreas.", "Interpreta la tendencia pero falla en el cálculo.", "No logra extraer datos del gráfico."],
        ["Unidades de Medida", "Todas las respuestas incluyen unidades correctas.", "Algunas respuestas carecen de unidades.", "No utiliza unidades de medida."],
        ["Metacognición", "Reflexiona profundamente sobre su proceso.", "Responde de forma superficial.", "No completa la reflexión."]
    ]

    table_rub = doc.add_table(rows=len(rubrica_data), cols=4)
    table_rub.style = 'Table Grid'
    for r_idx, row_content in enumerate(rubrica_data):
        for c_idx, value in enumerate(row_content):
            table_rub.cell(r_idx, c_idx).text = value

    # Guardar documento
    filename = "Guia_MRUV_Profesional.docx"
    doc.save(filename)
    print(f"Documento generado exitosamente: {filename}")

if __name__ == "__main__":
    generar_guia_mruv()
