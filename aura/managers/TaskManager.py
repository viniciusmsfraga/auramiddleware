from zeroless import (Client, Server)
import json
from aura.managers import SemanticManager as graph
from aura.managers import StorageManager as db
from aura.managers import helpers

zmq_device = Client()
zmq_device.connect_local(port=helpers.ports['device_manager'])
push_to_device = zmq_device.push()


def create_condition(condition):
    print("create_condition")
    # TaskManager -> StorageManager
    db.store('conditions', condition)


def update_condition():
    # TaskManager -> StorageManager
    print("update_condition")


def remove_condition():
    # TaskManager -> StorageManager
    print("remove_condition")


def send_command(device, command):
    # TaskManager -> DeviceManager
    print("send_command")


def get_available_commands():
    # TaskManager -> SemanticManager
    commands_query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX auraDevice: <https://raw.githubusercontent.com/viniciusmsfraga/auramiddleware/master/semantics/ontologies/AuraDevice#>
    PREFIX auraActuate: <https://raw.githubusercontent.com/viniciusmsfraga/auramiddleware/master/semantics/ontologies/AuraActuate#>

    SELECT DISTINCT ?variable ?device ?platform ?actuator
    WHERE {
        ?device auraDevice:hasPlatform ?platform .
  		?platform auraDevice:hasActuator ?actuator .
        ?actuator auraActuate:increases ?variable .
    }"""
    result = graph.query(commands_query)
    for row in result:
        print(row)

def get_available_conditions():
    conditions_query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX auraDevice: <https://raw.githubusercontent.com/viniciusmsfraga/auramiddleware/master/semantics/ontologies/AuraDevice#>
    PREFIX auraSense: <https://raw.githubusercontent.com/viniciusmsfraga/auramiddleware/master/semantics/ontologies/AuraSense#>

    SELECT DISTINCT ?variable ?device ?platform ?sensor
    WHERE {
        ?device auraDevice:hasPlatform ?platform .
  		?platform auraDevice:hasSensor ?sensor .
        ?sensor auraSense:canMeasure ?variable .
    }"""
    result = graph.query(conditions_query)
    for row in result:
        print(row)

def test_conditions(measurement):
    conditions = """
    """
    result = graph.query(conditions)


listen_for_push = Server(port=helpers.ports['task_manager']).pull()
for msg in listen_for_push:
    obj = json.loads(msg.decode())
    if obj['@type'] == 'Measurement':
        test_conditions(obj)
    else:
        print("i don't know what to do with this message")
