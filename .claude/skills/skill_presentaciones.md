# Skill: Presentaciones Educativas

Este skill permite generar presentaciones pedagógicas usando herramientas MCP.

## Capacidades

- Crear presentaciones desde cero
- Usar plantillas PPTX
- Reemplazar marcadores
- Generar secuencias pedagógicas

## Herramientas disponibles

### `crear_presentacion_desde_plantilla`
Crea una presentación basada en una plantilla.

**Parámetros:**
- `plantilla_path` (str)
- `reemplazos` (dict)
- `contenido_slides` (list)
- `nombre_archivo` (str)

### `crear_presentacion_educativa`
Genera una presentación desde cero usando una estructura pedagógica.

---

## Instrucciones para el modelo

- Siempre pregunta por la plantilla si no se especifica.
- Si el usuario entrega contenido pedagógico, estructúralo en 13 diapositivas.
- Si el usuario pide “haz una clase”, usa la herramienta adecuada.
- Responde siempre con JSON cuando se invoque una tool.

---

## Ejemplos

### Ejemplo 1: Crear presentación desde plantilla

**Usuario:**  
Quiero una clase de química sobre enlaces iónicos.

**Asistente:**  
```json
{
  "tool": "crear_presentacion_desde_plantilla",
  "arguments": {
    "plantilla_path": "PLANTILLA_QCA.pptx",
    "reemplazos": {
      "{{ASIGNATURA}}": "Química",
      "{{UNIDAD}}": "Enlaces Iónicos"
    },
    "contenido_slides": [...]
  }
}
