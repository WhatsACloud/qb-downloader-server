from django.shortcuts import render
import json
from intuitlib.exceptions import AuthClientError
import downloader.error_logger as logger
from config import CONTACT_DEV_MSG

def render_success(request, saved_companies_list, new_auth_url, msg=""):
    context = {
        "msg": msg,
        "auth_url": new_auth_url,
        "saved_companies_list": saved_companies_list,
    }
    return render(request, "success.html", context)

def get_err_msgs(err: AuthClientError):
    error = ""
    desc = ""
    try:
        loaded_json = json.loads(err.content)
        print(loaded_json)
        error = f'API error (status_code: {err.status_code}): {loaded_json["error"]}'
        desc = loaded_json["error_description"]
    except json.JSONDecodeError as _:
        error = f"Gateway error (status_code: {err.status_code})"
        desc = err.content
    return error, desc

    """if is API error, err.content should follow the following format:
    err.content = {
        "error": "error title",
        "error_description": "error description",
    }
    """
def render_error(request, err: AuthClientError, solution_list=[]):
    error, desc = get_err_msgs(err)
    logger.log_err(err.intuit_tid, f"err: {error} | desc: {desc}")
    solution_list.append("Disconnecting and reconnecting your company from the app (see 'How to disconnect an app' in https://quickbooks.intuit.com/learn-support/en-us/help-article/manage-users/transfer-app-ownership-disconnect-apps/L73ZAy899_US_en_US#:~:text=Select%20Disconnect.-,QuickBooks%20Online%20Accountant,Complete%20the%20short%20questionnaire.)")
    context = {
        "error": error,
        "error_desc": desc,
        "intuit_tid": err.intuit_tid,
        "solution_list": solution_list,
        "contact_developer_msg": CONTACT_DEV_MSG,
    }
    return render(request, "error.html", context)

    """Where err is AuthClientError and err.content follows this pattern: error message: b'{"error_description":"Incorrect or invalid refresh token","error":"invalid_grant"}'
    """
def render_invalid_grant_error(request, auth_url):
    context = {
        "auth_url": auth_url,
        "contact_developer_msg": CONTACT_DEV_MSG,
    }
    return render(request, "invalid_grant_error.html", context)