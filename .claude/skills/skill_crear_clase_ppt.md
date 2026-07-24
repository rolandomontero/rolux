# Skill: Generador de Clases PPT Educativas

Este skill permite que el agente genere **clases completas en PowerPoint** usando las herramientas del servidor MCP, especialmente `crear_presentacion_desde_plantilla`.

---

## 🎯 Propósito del Skill
- Transformar una instrucción del docente en una **clase completa** lista para usar.
- Usar plantillas `.pptx` con placeholders.
- Construir automáticamente la estructura pedagógica (inicio – desarrollo – cierre).
- Llamar a la tool `crear_presentacion_desde_plantilla` con los parámetros correctos.

---

## 🧠 Comportamiento del Skill

El agente debe:

1. **Interpretar la solicitud del docente**, por ejemplo:  
   - “Genera una clase de química sobre enlaces covalentes para 2° medio”.
   - “Haz una presentación de matemáticas sobre funciones lineales”.

2. **Construir automáticamente**:
   - Diccionario `reemplazos` para la plantilla.
   - Lista `contenido_slides` con la estructura pedagógica de 13 diapositivas.

3. **Llamar a la tool MCP**:

crear_presentacion_desde_plantilla(
plantilla_path: str,
reemplazos: dict,
contenido_slides: list,
nombre_archivo: str
)


4. **Devolver al usuario**:
   - Confirmación del archivo generado.
   - Nombre del archivo.
   - Sugerencias de uso.

---

## 🧩 Estructura esperada por el Skill

### 1. Placeholders esperados en la plantilla
El agente debe generar un diccionario como:

```json
{
  "{{NC}}": "10",
  "{{CURSO}}": "2do Medio",
  "{{FECHA}}": "2026-05-26",
  "{{ASIGNATURA}}": "Química",
  "{{UNIDAD}}": "Unidad 2: Enlaces Químicos",
  "{{CONTENIDOS}}": "Enlaces Iónicos y Estructuras de Lewis",
  "{{HABILIDADES}}": "Análisis, Representación Gráfica",
  "{{VIRTUD}}": "ORDEN",
  "{{OA}}": "Objetivo de aprendizaje…",
  "{{OC}}": "Objetivo de clase…"
}
