from django.http import HttpResponse
from intuitlib.exceptions import AuthClientError
# from django.shortcuts import render
import downloader.tmp_query as tmp_query
import sys
import webbrowser
import os
import atexit
import downloader.utils as utils
sys.path.append("downloader")
from downloader.config import temp_folder_name, csv_folders, scopes
from downloader.auth_client import auth_client
from downloader.url_list import Company
from downloader.page_responses import render_error, render_success

def reopen_auth_url():
    auth_url = auth_client.get_authorization_url(scopes) # safe
    webbrowser.open(auth_url) # safe

def index(request):
    if request.method == "GET":
        code = request.GET.get("code", "")
        # state = request.GET.get("state", "")
        company_id = request.GET.get("realmId", "") # company_id
        old_token = auth_client.access_token
        if company_id != auth_client.realm_id or not auth_client.access_token:
            try:
                # auth_client.get_bearer_token("malformed", realm_id=realm_id)
                auth_client.get_bearer_token(code, realm_id=company_id)
            except AuthClientError as err:
                print("Authorization error", err.content, err.intuit_tid)
                return render_error(request, err, "Server authorization failed. Please try again.")
        tmp_query.make_tmp()
        cur_company = Company(company_id, auth_client.access_token)
        cur_company.get_name()
        auth_url = auth_client.get_authorization_url(scopes) # safe
        if not cur_company.is_already_saved():
            cur_company.save_all_sheets(csv_folders)
            return render_success(request, tmp_query.get_folder_names(), auth_url, f"Data for {cur_company.name} has been successfully saved.")
        return render_success(request, tmp_query.get_folder_names(), auth_url, f"Data for {cur_company.name} has been already been saved.")
        

def zipDownload(request):
    return utils.save_as_zip(f"{temp_folder_name}/totalzip", csv_folders)

atexit.register(utils.exit_handler)