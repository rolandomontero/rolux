import servidor_mcp

__all__ = ["TOOL_IMPL", "OLLAMA_TOOLS"]

TOOL_IMPL = {
    "generar_clase_ppt": servidor_mcp.crear_presentacion,
    "read_file": servidor_mcp.read_file,
    "generar_correos_ausentes": servidor_mcp.generar_correos_ausentes,
}

OLLAMA_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "generar_clase_ppt",
            "description": "Crea una presentación de PowerPoint usando una plantilla .pptx y contenido adicional.",
            "parameters": {
                "type": "object",
                "properties": {
                    "plantilla_path": {
                        "type": "string",
                        "description": "Ruta al archivo de plantilla .pptx.",
                    },
                    "reemplazos": {
                        "type": "object",
                        "description": "Diccionario con los marcadores que deben estar en llaves dobles {{MARCADOR}} y sus valores.",
                        "items": {
                            "{{NC}}": {
                                "type": "string",
                                "description": "Número de clase, por ejemplo 'Clase 01', 'Clase 02', etc.",
                            },
                            "{{CURSO}}": {
                                "type": "string",
                                "description": "Nivel o curso, por ejemplo '2° Medio'.",
                            },
                            "{{FECHA}}": {
                                "type": "string",
                                "description": "Fecha de la clase en formato 'dd-mm-yyyy', por ejemplo '24-09-2015'.",
                            },
                            "{{ASIGNATURA}}": {
                                "type": "string",
                                "description": "Asignatura, por ejemplo 'Química', 'Física', 'Matemáticas'.",
                            },
                            "{{UNIDAD}}": {
                                "type": "string",
                                "description": "Unidad curricular, opcional.",
                            },
                            "{{CONTENIDOS}}": {
                                "type": "string",
                                "description": "Tema central de la clase, por ejemplo 'Enlaces iónicos'.",
                            },
                            "{{HABILIDADES}}": {
                                "type": "string",
                                "description": "Habilidades a desarrollar, opcional.",
                            },
                            "{{OA}}": {
                                "type": "string",
                                "description": "Objetivos de aprendizaje, obligatorio.",
                            },
                            "{{OC}}": {
                                "type": "string",
                                "description": "Objetivos de clase, obligatorio.",
                            },
                        },
                    },
                    "contenido_slides": {
                        "type": "array",
                        "description": "Lista de diapositivas con título y contenido.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "titulo": {"type": "string"},
                                "cuerpo": {
                                    "oneOf": [
                                        {"type": "string"},
                                        {"type": "array", "items": {"type": "string"}},
                                    ]
                                },
                            },
                            "required": ["titulo", "cuerpo"],
                        },
                    },
                    "nombre_archivo": {
                        "type": "string",
                        "description": "Nombre del archivo de salida [<número de clase> CLASE <fecha:<yy><mm><dd>> - <tema>].pptx.",
                    },
                },
                "required": ["plantilla_path", "reemplazos", "contenido_slides"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Lee el contenido de un archivo local y lo devuelve como texto. Úsala solo si el usuario pide leer, mostrar o analizar el archivo; no la uses para cargar una plantilla de correo en generar_correos_ausentes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Ruta al archivo a leer.",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generar_correos_ausentes",
            "description": "Genera borradores o envía correos de evaluaciones atrasadas desde una planilla Excel. Para alumnos ausentes, recuperaciones o pruebas atrasadas, usa esta herramienta directamente y pasa cualquier archivo de plantilla mediante el parámetro plantilla; no leas la plantilla con read_file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fecha": {
                        "type": "string",
                        "description": "Fecha de la evaluación: AAAA-MM-DD, DD/MM/AAAA o DD-MM-AAAA.",
                        "default": "2026-08-26",
                    },
                    "excel": {
                        "type": "string",
                        "description": "Ruta de la planilla Excel.",
                        "default": "AUSENTE.xlsx",
                    },
                    "plantilla": {
                        "type": "string",
                        "description": "Ruta de la plantilla de correo.",
                        "default": "carta_ausentes.txt",
                    },
                    "plantilla_talento": {
                        "type": "string",
                        "description": "Plantilla para filas cuya columna Talento, Talentoso o Talentos indique sí/si, true, 1, x o talento.",
                        "default": "carta_talento.txt",
                    },
                    "remitente": {
                        "type": "string",
                        "description": "Cuenta de Outlook que se usará como remitente.",
                        "default": "rolando.montero@colsanjavier.cl",
                    },
                    "enviar": {
                        "type": "boolean",
                        "description": "Envía los correos. Usar true solo con autorización explícita.",
                        "default": False,
                    },
                    "borradores": {
                        "type": "boolean",
                        "description": "Guarda los mensajes como borradores.",
                        "default": True,
                    },
                },
                "required": [],
            },
        },
    },
]
