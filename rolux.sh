#!/bin/bash
# Navegar al directorio del proyecto
cd "/Volumes/MisApps/Documentos/www/rolux/"

# Activar entorno virtual usando ruta absoluta
source "/Volumes/MisApps/Documentos/www/rolux/utp/bin/activate"

# Ejecutar la aplicación
python3 "/Volumes/MisApps/Documentos/www/rolux/start.py" m=0
