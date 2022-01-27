from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from plantuml_sequence_service.core.message_registry import requests_registry, responses_registry
from plantuml_sequence_service.core.uml_generator import PlantUMLGenerator

router = APIRouter()


@router.get("/uml_text/", response_class=PlainTextResponse)
async def generate_uml_sequence_text():
    """
    Generate and get the sequence diagram as at text
    """
    generator = PlantUMLGenerator(requests_registry, responses_registry)
    uml = generator.generate_text()
    return uml
