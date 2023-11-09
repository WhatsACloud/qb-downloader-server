import requests
import json
import downloader.utils as utils
from enum import Enum
import downloader.auth_client as auth_client
from intuitlib.exceptions import AuthClientError

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

def is_gateway_err(status_code):
    return not (status_code == 200 or status_code == 400)

def is_auth_err(status_code):
    return status_code == 401

msg_dict = {
    302: "Resource redirect or resource has moved",
    401: "Unauthenticated access: application authentication failed due to invalid or expired tokens",
    403: "Forbidden access: authorization specific, application authorization failed due to insufficient user access role",
    403: "Resource not found: routing error, access or configuration on the  Gateway, or incorrect endpoint requested",
    405: "Method not allowed: attempt to request other than GET/POST requests",
    429: "Too many requests: request is throttled as it exceeded the throttle policy.",
    500: "Internal Server Error: missing POST body or other exceptions within application, or a service outage",
    502: "Bad Gateway: Infrastructure misconfiguration, propagates response from downstream, or a service outage",
    503: "Service unavailable: Outage",
    504: "Service timeout: Outage",
}

def get_msg(status_code):
    if status_code in msg_dict:
        return msg_dict[status_code]
    raise ValueError(f"Status code {status_code} does not exist.")

def get_res(url, headers):
    data = None
    response = None
    for count in range(RES_LIMIT):
        # response = requests.get(url, {"false headers": "blah"})
        response = requests.get(url, headers=headers)
        if not is_gateway_err(response.status_code):
            data = json.loads(response.content)
            if utils.is_api_err(data):
                err = AuthClientError(response)
                err.content = json.dumps({
                    "error": data["Fault"]["Error"][0]["Message"],
                    "error_description": data["Fault"]["Error"][0]["Detail"],
                })
                # err.content = data["Fault"]["Error"][0]["Message"]
                raise err
            break
        if is_auth_err(response.status_code):
            auth_client.client.refresh()
        if count + 1 >= RES_LIMIT:
            err = AuthClientError(response)
            err.content = get_msg(err.status_code)
            raise err
    # if get_error_code(data) > 0:
    #     intuit_tid = get_intuit_tid(response.headers)
    return data