# Skill: Notificación de Ausencia a Evaluación

## Propósito

Usa la herramienta `generar_correos_ausentes` para preparar notificaciones de
alumnos ausentes a una evaluación desde `AUSENTE.xlsx`.

La herramienta envía al alumno, padre y madre, y agrega en copia los contactos
`PJ`, `JD` y `crojas@colsanjavier.cl`.

## Selección de plantilla

- Usa `AUSENTE.xlsx` como planilla predeterminada.
- Usa `carta_ausentes.txt` para las filas normales.
- Usa `carta_talento.txt` para las filas cuyo valor de talento sea verdadero.
- La columna de talento debe llamarse `Talento`, `Talentoso` o `Talentos`.
- Considera verdadero: `sí`, `si`, `s`, `true`, `1`, `x` o `talento`, sin distinguir
  mayúsculas ni minúsculas.
- La columna `S` no indica talento: se usa para sustituir `[S]` por `hijo` o
  `hija`.

Si el Excel no tiene una columna de talento, informa que todas las filas usarán
`carta_ausentes.txt` y recomienda agregar una columna `Talento` con valores
`si` o `no`.

## Flujo de uso

1. Identifica la fecha mencionada por el usuario y conviértela a un formato
	aceptado, como `2026-08-26` o `26-08-2026`.
2. Llama directamente a `generar_correos_ausentes`; no uses `read_file` para
	leer las plantillas.
3. Pasa estos valores salvo que el usuario indique otros:

```json
{
  "fecha": "2026-08-26",
  "excel": "AUSENTE.xlsx",
  "plantilla": "carta_ausentes.txt",
  "plantilla_talento": "carta_talento.txt",
  "remitente": "rolando.montero@colsanjavier.cl",
  "enviar": false,
  "borradores": true
}
```

4. Antes de enviar mensajes reales, muestra que se usará `enviar: true` y
	solicita autorización explícita. Para una primera prueba usa
	`enviar: false` y `borradores: false`.
5. No llames a `read_file` para una plantilla que será usada por la herramienta;
	solo úsalo si el usuario pide leer o analizar su contenido.


