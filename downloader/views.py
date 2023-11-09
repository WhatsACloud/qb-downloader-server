# from django.http import HttpResponse
from downloader.config import temp_folder_name, csv_folders, scopes
import downloader.error_logger as logger
logger.setup()
from intuitlib.exceptions import AuthClientError
# from django.shortcuts import render
import downloader.tmp_query as tmp_query
import sys
import webbrowser
import atexit
import downloader.utils as utils
sys.path.append("downloader")
import downloader.auth_client as auth_client
from downloader.url_list import Company
import downloader.page_responses as page_res

def reopen_auth_url():
    auth_url = auth_client.client.get_authorization_url(scopes) # safe
    webbrowser.open(auth_url) # safe

def index(request):
    try:
        if request.method == "GET":
            code = request.GET.get("code", "")
            company_id = request.GET.get("realmId", "") # company_id
            if company_id != auth_client.client.realm_id or not auth_client.client.access_token or not auth_client.client.access_token:
                # auth_client.client.get_bearer_token("malformed", realm_id=company_id)
                auth_client.client.get_bearer_token(code, realm_id=company_id)
            tmp_query.make_tmp()
            cur_company = Company(company_id, auth_client.client.access_token)
            cur_company.get_name()
            auth_url = auth_client.client.get_authorization_url(scopes) # safe
            if not cur_company.is_already_saved():
                cur_company.save_all_sheets(csv_folders)
                return page_res.render_success(request, tmp_query.get_folder_names(), auth_url, f"Data for {cur_company.name} has been successfully saved.")
            return page_res.render_success(request, tmp_query.get_folder_names(), auth_url, f"Data for {cur_company.name} has already been saved.")
    except AuthClientError as err:
        if utils.ami_invalid_grant_err(err):
            auth_url = auth_client.client.get_authorization_url(scopes)
            return page_res.render_invalid_grant_error(request, auth_url)
        return page_res.render_error(request, err)
        

def zipDownload(request):
    return utils.save_as_zip(f"{temp_folder_name}/totalzip", csv_folders)

atexit.register(utils.exit_handler)