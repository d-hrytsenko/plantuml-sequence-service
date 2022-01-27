from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    """
    Base class for a HTTP request/response method representation
    """
    timestamp: float
    trace_id: str
    headers: dict
    body: Optional[dict] = None


class RequestMessage(Message):
    path: str
    method: str
    host: str
    remote_addr: str


class ResponseMessage(Message):
    status: str
