# Consultar una planilla de Google y detectar cambios

`google_sheets_monitor.py` accede a la hoja usando OAuth de la cuenta Google
del usuario. Así puede leer archivos compartidos con esa cuenta sin compartir
la planilla con una cuenta de servicio. Solo solicita permiso de lectura.

## Preparación (una vez)

1. Inicia sesión en [Google Cloud Console](https://console.cloud.google.com/) con
   la cuenta laboral. Selecciona un proyecto o crea uno.
2. Ve a **APIs y servicios → Biblioteca**, busca **Google Sheets API** y pulsa
   **Habilitar**. Este programa solo usa Sheets API; no necesita Drive API.
3. Ve a **Google Auth Platform** (o **APIs y servicios → Pantalla de
   consentimiento OAuth**) y configura la aplicación:
   - Si la organización ofrece **Interna**, úsala para limitar el acceso al
     dominio laboral.
   - Si debes elegir **Externa** y dejar la app en modo **Prueba**, agrega tu
     cuenta de trabajo como usuario de prueba. En modo de prueba, Google puede
     hacer caducar el token de actualización a los 7 días; vuelve a autorizar
     si el script lo solicita.
   - La organización puede bloquear aplicaciones OAuth nuevas. En ese caso,
     pide a TI que autorice el cliente o proyecto; no intentes usar credenciales
     personales para eludir esa política.
4. En **Google Auth Platform → Clientes → Crear cliente**, elige **Aplicación
   de escritorio**. Descarga el JSON del cliente.
5. En Finder, mueve el archivo descargado al directorio raíz de este proyecto y
   cámbiale el nombre a `credentials.json`. No pegues su contenido en chats ni
   lo subas a Git. El repositorio ya excluye ese archivo, así como `.google_sheets/`.
6. Confirma que la cuenta laboral tenga al menos permiso de **Lector** en la
   planilla. Si está en una unidad compartida, el permiso debe estar concedido
   a esa misma cuenta.
7. Si todavía no están instalados, ejecuta en la terminal del proyecto:
   `utp/bin/python -m pip install google-api-python-client==2.200.0 google-auth-oauthlib==1.4.1`.

La primera ejecución abrirá el navegador. Elige explícitamente la cuenta de
trabajo que tiene acceso a la hoja y acepta el permiso de solo lectura. La
sesión se guarda localmente en `.google_sheets/token.json`; no compartas ni
subas ese archivo. Si se autoriza una cuenta equivocada, elimina ese token y
vuelve a ejecutar para escoger la cuenta laboral.
La referencia `.google_sheets/snapshot.json` también contiene los valores
descargados de la hoja; mantenla en un equipo y ubicación autorizados por tu
organización. `.gitignore` evita que Git la incluya, pero no evita la
sincronización de carpetas por otros servicios.

## Uso

Usa la URL de Google Sheets o el ID que aparece entre `/d/` y `/edit`.
Indica el nombre de pestaña y el rango A1, por ejemplo `Datos!A:Z`:

`utp/bin/python google_sheets_monitor.py 'https://docs.google.com/spreadsheets/d/ID/edit' --range 'Datos!A:Z'`

Para buscar un curso y un RUT y obtener los valores de las columnas H y K:

`utp/bin/python google_sheets_monitor.py 'https://docs.google.com/spreadsheets/d/ID/edit' --range 'Datos!A:K' --curso '1A' --rut '12.345.678-9'`

La primera fila debe contener los encabezados `Curso` y `RUT`. La salida es una
línea JSON por coincidencia, con el número de fila y los valores `H` y `K`.

Para filtrar todas las filas del curso `1EM-A` y guardarlas en NumPy:

`utp/bin/python google_sheets_monitor.py 'https://docs.google.com/spreadsheets/d/1o_RJX87N5u1wD5czzztli-RAt-sFYF_k/' --range 'A:K' --curso '1EM-A' --salida-curso 'google_sheets/curso_1EM-A.npz'`

El archivo `.npz` contiene `encabezados` y `datos`. Para abrirlo:

`datos = np.load('google_sheets/curso_1EM-A.npz', allow_pickle=True)`

- Primera ejecución: guarda la referencia inicial, sin marcar cambios.
- Ejecuciones siguientes: compara los valores y enumera las filas con cambios.
- Para ver valores anteriores y actuales, agrega `--details`. Úsalo con cuidado
  si la hoja contiene información personal.
- Tras revisar y procesar las novedades, ejecuta con `--accept-current` para
  aceptar la versión actual como referencia.
- Para impedir que una tarea automatizada continúe cuando encuentra cambios,
  agrega `--fail-on-change`; el proceso termina con código 1. El código 0
  significa que no se detectaron cambios (o que aún no existía referencia).

La comparación detecta cambios en valores y contenido de celdas, no cambios
solo de formato. Las filas se comparan por su posición; si se insertan o
reordenan filas, se reportarán las posiciones cuyo contenido cambió.

## Integración desde otro código Python

Importa `verificar_cambios` y comprueba `resultado.has_changes` antes de iniciar
la tarea. Si es `True`, detén la tarea para revisar las filas reportadas; solo
acepta la referencia una vez procesadas las novedades. La primera consulta crea
la referencia y devuelve `has_changes == False`.