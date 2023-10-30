from django.http import HttpResponse
# from django.shortcuts import render
import sys
import base64
import webbrowser
import os
import shutil
import atexit
import utils
sys.path.append("downloader")
from config import temp_folder_name, csv_folders, scopes
from auth_client import auth_client
from url_list import company_list

def save_as_zip():
    response = None
    shutil.make_archive(f"{temp_folder_name}/totalzip", 'zip', csv_folders)
    with open(f"{temp_folder_name}/totalzip.zip", "rb") as f:
        response = HttpResponse(f.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=totalzip.zip'
        f.close()
        print("Finished!")
    return response

def index(request):
    if request.method == "GET":
        code = request.GET.get("code", "")
        # state = request.GET.get("state", "")
        realm_id = request.GET.get("realmId", "")

        auth_client.get_bearer_token(code, realm_id=realm_id)
        print("access token", auth_client.access_token)
        headers = {
            'Authorization': f"Bearer {auth_client.access_token}",
            'Accept': 'application/json'
        }
        if not os.path.exists(csv_folders):
            os.makedirs(csv_folders)
        cur_company = company_list.get_next()
        if cur_company != None:
            cur_company.save_all_sheets(headers, cur_company.name)
            if not company_list.is_last():
                auth_url = auth_client.get_authorization_url(scopes)
                webbrowser.open(auth_url)
                return HttpResponse()
        return save_as_zip()

atexit.register(utils.exit_handler)