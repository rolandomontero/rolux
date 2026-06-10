# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Environment Setup
- Activate Virtual Environment: `utp\Scripts\activate.bat`
- Quick Start (Local): Run `inicio.bat`
- Quick Start (Cloud): Run `inicio_cloud.bat`

### Running the Server
- Start MCP Server: `python servidor_mcp.py`

## Architecture & Structure

### High-Level Architecture
The project implements a Model Context Protocol (MCP) server using the `FastMCP` framework. It provides a set of tools that allow an LLM to interact with the local system and generate educational content in PowerPoint format.

### Key Components
- **MCP Server (`servidor_mcp.py`)**: The core server implementation. It defines tools for:
    - System utilities: Time retrieval (`obtener_hora`), file listing (`listar_archivos`), and simple math (`calcular_suma`).
    - PowerPoint Generation: Tools to create educational presentations from scratch (`crear_presentacion_educativa`) or based on templates (`crear_presentacion_desde_plantilla`) using the `python-pptx` library.
- **Clients (`cliente.py`, `cliente_claude.py`)**: Test clients used to interact with and verify the MCP server's functionality.
- **Knowledge Base**:
    - `agentes/`: Contains markdown definitions for educational agents (e.g., `agente_educativo.md`).
    - `skills/`: Contains markdown files defining specific skills and pedagogical structures for presentations.
- **Virtual Environment (`utp/`)**: Contains the project's Python dependencies and environment configuration.

### Dependencies
- `fastmcp`: For the MCP server implementation.
- `python-pptx`: For manipulating and creating PowerPoint files.
- `ollama` (External): Used as the LLM provider as configured in the startup scripts.
