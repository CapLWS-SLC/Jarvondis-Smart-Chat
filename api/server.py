# api/server.py

from fastapi import FastAPI

app = FastAPI()

@app.post("/chat")
def chat(request):
    return engine.process(request.message)
