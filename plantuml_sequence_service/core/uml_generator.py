from plantuml_sequence_service.config.config import (
    SERVICE_NAMES, REQUEST_STEP_TEMPLATE,
    RESPONSE_STEP_TEMPLATE, BODY_DISPLAY_LIMITER
)
from plantuml_sequence_service.core.message_registry import MessageRegistry
from plantuml_sequence_service.models.message import RequestMessage


class PlantUMLGenerator:
    def __init__(self, requests: MessageRegistry, responses: MessageRegistry):
        self._requests = requests
        self._responses = responses

    def generate_text(self) -> str:
        """
        Generate a PlantUML sequence diagram based on captured requests and responses
        :return: PlantUML sequence diagram as a string
        """
        result = "@startuml\n"
        # Get already captured requests and responses
        requests = self._requests.as_dict()
        responses = self._responses.as_dict()

        # Iterate according to timestamps through captured requests + responses
        for message in sorted(
                list(requests.values()) + list(responses.values()), key=lambda d: d.timestamp
        ):
            # Determine client and server addresses
            request = requests.get(message.trace_id)
            server = request.host
            client = request.headers.get("Origin", "").replace("http://", "")
            if not server or not client:
                continue
            # Try to convert to human readable names
            server = SERVICE_NAMES.get(server, server)
            client = SERVICE_NAMES.get(client, client)

            # Prepare a step
            if isinstance(message, RequestMessage):
                step_template = REQUEST_STEP_TEMPLATE
            else:
                step_template = RESPONSE_STEP_TEMPLATE
            step = step_template.format(**locals())
            # Add a body, which will be displayed on a diagram as a link with a tooltip
            if message.body:
                if len(str(message.body)) > BODY_DISPLAY_LIMITER:
                    step += " [[Body{%s...}]]" % str(message.body)[:BODY_DISPLAY_LIMITER]
                else:
                    step += " [[Body{%s}]]" % str(message.body)
            # Add a step to the result
            result = f'{result}{step}\n'

        result = f'{result}\n@enduml'
        return result
