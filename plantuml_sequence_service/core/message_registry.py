from copy import copy

from plantuml_sequence_service.models.message import Message


class MessageRegistry:
    def __init__(self):
        self._storage = {}

    def add(self, message: Message):
        self._storage[message.trace_id] = message

    def clear(self):
        self._storage.clear()

    def as_dict(self):
        return copy(self._storage)


requests_registry = MessageRegistry()
responses_registry = MessageRegistry()
