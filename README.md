# Jarvondis Smart Chat

An advanced, safety-first smart chat system designed to model healthy, protected interaction between humans and technology — including kids.

## Features

- Safety filters and policy engine
- Persona layer (Captain / ceremonial / neutral)
- Memory module for preferences and context
- Task orchestrator for tools and actions
- API server (FastAPI) for integration

## Quick start

```bash
pip install -r requirements.txt
uvicorn jarvondis.api.server:app --reload
