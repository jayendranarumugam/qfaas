import json


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    return json.dumps({"message": "Hello from your new Qiskit function!"})