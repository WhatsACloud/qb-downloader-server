import requests
import json
from enum import Enum

RES_LIMIT = 3

class ResType(Enum):
    Success    = 0
    GatewayErr = 1
    ServiceErr = 2

def get_intuit_tid(headers):
    return headers["intuit_tid"]

def is_error(data: dict):
    if data.get("Fault"):
        return True
    return False

    """_summary_ returns 0 if request is successful
    """
def get_error_code(data):
    if is_error(data):
        return int(data["Fault"]["Error"][0]["code"])
    return 0

# def check_err(status_code):
#     if status

def get_res(url, headers):
    count = 0
    response = requests.get(url, headers=headers)
    if response.status_code == 401:
        print("Authentication failed")
        print(response.content)
    data = json.loads(response.content)
    if get_error_code(data) > 0:
        intuit_tid = get_intuit_tid(response.headers)
        print("oh no! error!")
    return data