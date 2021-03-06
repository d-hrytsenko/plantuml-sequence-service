# PlantUML Sequence Service
This service has been written in order to get a helicopter view on an interaction between 10 microservices (legacy Flask project) in short terms,
taking into account that there was no proper logging implemented or documentation available.
The main idea was to receive a sequence diagrams of requests/responses between services, after executing some user scenarios.

Adding a couple of lines into each service will allow sending requests/responses data to the PlantUML Sequence Service,
which will process the gathered data and generate a sequence diagram of calls.

## Running the service
1) There is a config with address:human-readable name mapping (to make the sequence diagram more readable), that can be filled before starting the service:
```bash
cd config
cp EXAMPLE.service_names.yml service_names.yml
# Fill the mapping for the needed services
```
2) Install the requirements
```shell
pip3 install -r requirements.txt
```
3) Run the service
```shell
python3 -m plantuml_sequence_service.main
```

## Update the services for which the sequence diagram is needed
Before running the needed services, set the following environment variables:
```bash
# Optional, host and port of PlantUML Sequence Service:
export UML_APP_HOST=127.0.0.1
export UML_APP_PORT=8000
# Mandatory:
# port used for starting Flask application
export FLASK_PORT=<SERVICE_FLASK_PORT>
# update the python path
export PYTHONPATH=$PYTHONPATH:<PATH_TO_THIS_REPOSITORY>.
```
Modify the service code, adding the following lines after the Flask app created:
```python
# Assumed that 'requests' lib used for requests execution,
# the library will be patched to add 'Origin' header to all requests
from plantuml_sequence_service.utils import patch_requests
# Add two callbacks for the endpoints, which will send requests and responses to the PlantUML Sequence Service
from plantuml_sequence_service.utils import uml_flask
uml_flask.init(app)
```
Now, the needed services can be run.

## Generating the sequence diagram
1) Ensure that PlantUML Sequence Service and needed services are running
2) Make some interaction, that should trigger the communication between services. It might be some end-user action, like login, for example
3) Open the http://127.0.0.1:8000/docs url and execute the endpoint `/uml_text`.
![](https://raw.githubusercontent.com/d-hrytsenko/plantuml-sequence-service/master/docs/uml_text_docs.png)
4) In the response body, there will be a PlantUML sequence generated, that can be viewed, for example, using the https://plantuml-editor.kkeisuke.com/ website.
![](https://raw.githubusercontent.com/d-hrytsenko/plantuml-sequence-service/master/docs/sequence_example.png)

If there is a need to capture other calls, `/reset` endpoint can be called - it will delete all already captured http messages.