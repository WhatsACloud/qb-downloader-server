from django.shortcuts import render
from intuitlib.exceptions import AuthClientError
import json

def render_success(request, saved_companies_list, new_auth_url, msg=""):
    context = {
        "msg": msg,
        "auth_url": new_auth_url,
        "saved_companies_list": saved_companies_list,
    }
    return render(request, "success.html", context)

def render_error(request, err: AuthClientError, msg):
    loaded_json = json.loads(err.content)
    context = {
        "error": loaded_json["error"],
        "error_desc": loaded_json["error_description"],
        "msg": msg
    }
    return render(request, "error.html", context)