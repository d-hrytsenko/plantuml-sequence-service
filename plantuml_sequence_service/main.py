import uvicorn
from fastapi import FastAPI

from plantuml_sequence_service.config import config
from plantuml_sequence_service.routes import messages, uml

app = FastAPI()
app.include_router(messages.router)
app.include_router(uml.router)


if __name__ == "__main__":
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT, log_level="critical")
