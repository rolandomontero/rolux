#!/bin/bash

export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_API_KEY=
export ANTHROPIC_MODEL=gemma4:31b-cloud

# Activate virtual environment
source "/Volumes/MisApps/Documentos/www/rolux/utp/bin/activate"

python3 cliente_claude.py

# Keep terminal open
exec $SHELL
