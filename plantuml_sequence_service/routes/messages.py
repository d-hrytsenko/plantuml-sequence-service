from fastapi import APIRouter

from plantuml_sequence_service.core.message_registry import requests_registry, responses_registry
from plantuml_sequence_service.models.message import RequestMessage, ResponseMessage

router = APIRouter()


@router.post("/reset/")
async def reset():
    requests_registry.clear()
    responses_registry.clear()


@router.post("/requests/")
async def add_request(message: RequestMessage):
    """
    Add a request message to the registry
    """
    print(f">>> {message}")
    requests_registry.add(message)


@router.post("/responses/")
async def add_response(message: ResponseMessage):
    """
    Add a response message to the registry
    """
    print(f"<<< {message}")
    responses_registry.add(message)
