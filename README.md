# Jarvondis Smart Chat

An advanced, safety-first smart chat system designed to model healthy, protected interaction between humans and technology — including kids.

## Features

- ✅ Safety filters and policy engine
- ✅ Persona layer (customizable tone/personality)
- ✅ Memory module for preferences and context
- ✅ Task orchestrator for tools and actions
- ✅ FastAPI server with REST endpoints
- ✅ Interactive web interface
- ✅ Support for web search, math, summarization, keyword extraction

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/CapLWS-SLC/Jarvondis-Smart-Chat.git
cd Jarvondis-Smart-Chat

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
# Start the API server
uvicorn api.server:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`

### Accessing the Web Interface

Open `static/index.html` in your browser or navigate to a static server:

```bash
# Using Python's built-in server
cd static
python -m http.server 8080
```

Then open `http://localhost:8080` in your browser.

## API Endpoints

### Chat
```
POST /chat
{
  "message": "Hello!",
  "user_id": "user123"
}
```

### Web Search
```
POST /search
{
  "message": "Python programming tips"
}
```

### Math Calculation
```
POST /calculate
{
  "message": "2 + 2 * 5"
}
```

### Text Summarization
```
POST /summarize
{
  "message": "Long text to summarize..."
}
```

## Architecture

```
jarvondis/
├── core/
│   └── engine.py          # Main processing engine
├── safety/
│   └── filters.py         # Safety validation
├── policy/
│   └── policy_engine.py   # Access control policies
├── persona/
│   └── persona_engine.py  # Personality/tone styling
├── memory/
│   └── memory_engine.py   # Context and preference storage
└── orchestrator/
    └── tools/             # Extensible tool system
        ├── web.py         # Web search (DuckDuckGo)
        ├── math.py        # Safe math evaluation
        ├── nlp.py         # NLP utilities
        ├── system.py      # System info
        └── tool_registry.py

api/
└── server.py              # FastAPI application

static/
└── index.html             # Web interface
```

## Safety Features

- **Input Validation**: Multi-layer safety checks for harmful content
- **Sandboxed Execution**: Math and system operations run in restricted environments
- **Whitelist-Based**: Web requests only to approved domains
- **Policy Engine**: Configurable access control rules
- **Child-Safe**: Checks for content endangering minors

## Extending with New Tools

1. Create a new tool class in `orchestrator/tools/`:

```python
class MyTool:
    def run(self, query: str) -> str:
        # Implement your tool logic
        return result
```

2. Register in `tool_registry.py`:

```python
from .my_tool import MyTool

self.tools["my_tool"] = MyTool()
```

3. Handle in `task_engine.py`:

```python
if msg.startswith("my_command "):
    cmd = msg.replace("my_command ", "")
    return self.registry.get("my_tool").run(cmd)
```

## Development

### Running Tests
```bash
pip install pytest
pytest
```

### Code Style
```bash
pip install black
black jarvondis/ api/ orchestrator/
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Safety & Accessibility

This project prioritizes:
- Safe interactions for all ages
- Accessible design principles
- Privacy-first architecture
- Transparent safety policies

## Contact

For questions or concerns, please open an issue on GitHub.
