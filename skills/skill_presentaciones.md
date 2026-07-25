# Skill: Presentaciones Educativas

Este skill permite generar presentaciones pedagógicas usando herramientas MCP.

## Capacidades

- Crear presentaciones desde cero
- Usar plantillas PPTX
- Reemplazar marcadores {{MARCADOR}}
- Generar secuencias pedagógicas

## Herramientas disponibles

### `generar_clase_ppt`

Crea una presentación basada en una plantilla.

**Parámetros:**

- `plantilla_path` (str)
- `reemplazos` (dict)
- `contenido_slides` (list)
- `nombre_archivo` (str)

## Instrucciones para el modelo

- Siempre pregunta por la plantilla si no se especifica.
- Si el usuario entrega contenido pedagógico, estructúralo en 13 diapositivas.
- Si el usuario pide “haz una clase”, usa la herramienta adecuada.
- Responde siempre con una reflexión cuando se invoque una tool.

---

## Ejemplos

### Ejemplo 1: Crear presentación desde plantilla

**Usuario:**
Quiero una clase de química sobre enlaces iónicos.

**Asistente:**
Llamada a la herramienta 'generar_clase_ppt'
📋 Datos de institucionalización

| Campo       | Valor                                                                                                                                                                                                                                                                                   |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| NC          | Clase N°20                                                                                                                                                                                                                                                                             |
| Curso       | 2º Medio                                                                                                                                                                                                                                                                               |
| Fecha       | Martes 09 de junio de 2026                                                                                                                                                                                                                                                              |
| Asignatura  | Química                                                                                                                                                                                                                                                                                |
| Unidad      | Solubilidad y disoluciones                                                                                                                                                                                                                                                              |
| OA          | Comprender cómo varía la solubilidad de diferentes solutos según la temperatura y su naturaleza química, clasificando soluciones como insaturadas, saturadas y sobresaturadas, y explicando fenómenos asociados como la cristalización fraccionada y la solubilidad de los gases. |
| OC          | Clasificar, analizar curvas, explicar fenómenos.                                                                                                                                                                                                                                       |
| Habilidades | Análisis, clasificación, explicación, aplicación.                                                                                                                                                                                                                                   |
| Virtud      | Curiosidad científica                                                                                                                                                                                                                                                                  |

---

✅ Reflexión pedagógica

Decisiones de diseño instruccional:

1. Activación significativa: Partir de una pregunta cotidiana (azúcar en café)
   conecta el conocimiento previo con el nuevo, favoreciendo el aprendizaje
   anclado (Ausubel).
2. Progresión conceptual: Desde definición → factores → clasificación →
   aplicación → fenómenos especiales (cristalización y gases). Esto respeta la
   taxonomía de Bloom, ascendiendo de comprensión a aplicación y análisis.
3. Práctica dual: La práctica guiada (slide 8) reduce la carga cognitiva
   modelando el procedimiento, y la independiente (slide 9) verifica la
   transferencia.
4. Ticket de salida (slide 11) funciona como evaluación formativa de baja
   stakes, permitiendo ajustar la siguiente clase.
5. Diferenciación sólido/gas: Se aborda explícitamente para combatir la
   concepción alternativa de que "todo se disuelve más con calor".
6. Habilidad transversal: La virtud institucional (Curiosidad científica) se
   trabaja explícitamente en la motivación y la retroalimentación, fortaleciendo
   el perfil de egreso.

>> Archivo destino sugerido: 2DO MEDIO
>> QUIMICA\2MEDIO_QCA_Solubilidad_Clase20_09jun2026.pptx
