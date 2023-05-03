from decouple import config
from django.http import HttpResponse
from django.shortcuts import render
from intuitlib.client import AuthClient
import requests
import json
import sys
import base64
import urllib.parse
import webbrowser
from intuitlib.enums import Scopes
import os
import shutil
import atexit
sys.path.append("downloader")
from converter import Converter
data_file = "data.txt"
temp_folder_name = "/tmp/django_temp"

def exit_handler():
    if os.path.exists(temp_folder_name):
        shutil.rmtree(temp_folder_name)

client_id = config('CLIENT_ID')
client_secret = config('CLIENT_SECRET')
redirect_uri = config('REDIRECT_URI')
environment = config('ENVIRONMENT')

company_count = int(config('COMPANY_COUNT'))

# Instantiate client
auth_client = AuthClient(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    environment=environment, # “sandbox” or “production”
)

pAndL_url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365268313780/reports/ProfitAndLossDetail?minorversion=65"
bs_url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365268313780/reports/BalanceSheet?minorversion=65"
bs_url_2 = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365279120060/reports/BalanceSheet?minorversion=65"
pAndL_url_2 = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365279120060/reports/ProfitAndLossDetail?minorversion=65"

class Url:
    def __init__(self, base_url):
        self.base_url = base_url
        self.params = {}
    def add(self, name, value):
        self.params[name] = value
    def get(self):
        base_url = f"{self.base_url}?"
        for name in self.params:
            base_url += f"{name}={self.params[name]}"
            base_url += "&"
        base_url = base_url[:-1]
        return base_url

base_token_url = "https://sandbox-quickbooks.api.intuit.com/oauth2/v1/tokens/bearer"
token_class_url = Url(base_token_url)

scopes = [
    Scopes.ACCOUNTING,
]

def convert_and_save(converter, data, foldername, filename):
    csv_byte_str = converter.convert(data)
    print(foldername, "does this exist?", os.path.exists(foldername))
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    print(foldername, "does this exist?", os.path.exists(foldername))
    with open(foldername + f'/{filename}', 'wb') as f:
        f.write(csv_byte_str)
        f.close()

def get_current_count():
    bs_count = 1
    pAndl_count = 1
    for r, d, f in os.walk(temp_folder_name):
        print(f)
        for file in f:
            print("FILE", file)
            if file.startswith("bs"):
                bs_count += 1
            if file.startswith("pAndl"):
                pAndl_count += 1
    return bs_count, pAndl_count

bs_folder = "/bs"
pAndl_folder = "/pAndl"
csv_folders = temp_folder_name + "/csv_folders"
print("asdihfwirf   iprfu2rfbweifpweufewfoAHDSDJLfhadsifSDUJDHASLdkaJSFOISDEfhwadsouifaehwrnfiwehfweiufsdahnferaiufbredalkjndeafk")

def index(request):
    if request.method == "GET":
        code = request.GET.get("code", "")
        state = request.GET.get("state", "")
        realm_id = request.GET.get("realmId", "")
        # token_class_url.add("grant_type", "authorization_code")
        # token_class_url.add("code", code)
        # token_class_url.add("redirect_uri", redirect_uri)
        token_url = token_class_url.get()
        auth_header = f'{client_id}:{client_secret}'
        encoded_header = base64.b64encode(auth_header.encode('ascii'))
        headers = {
            'Authorization': f"Basic {encoded_header.decode('ascii')}",
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        auth_client.get_bearer_token(code, realm_id=realm_id)
        print("access token", auth_client.access_token)
        headers = {
            'Authorization': f"Bearer {auth_client.access_token}",
            'Accept': 'application/json'
        }
        print(temp_folder_name)
        if not os.path.exists(temp_folder_name):
            os.makedirs(temp_folder_name)
        converter = Converter()
        bs_count, pAndl_count = get_current_count()
        print(bs_count, company_count, "bruh")
        if bs_count < company_count or pAndl_count < company_count:
            response = requests.get(bs_url, headers=headers)
            pAndl_response = requests.get(pAndL_url, headers=headers)
            data = json.loads(response.content)
            pAndl_data = json.loads(pAndl_response.content)
            print("does exist", os.path.exists(csv_folders))
            if not os.path.exists(csv_folders):
                os.makedirs(csv_folders)
            print(csv_folders, "does exist", os.path.exists(csv_folders))
            convert_and_save(converter, data, f"{csv_folders}{bs_folder}", f'bs{bs_count}.csv')
            convert_and_save(converter, pAndl_data, f"{csv_folders}{pAndl_folder}", f'pAndl{pAndl_count}.csv')
            auth_url = auth_client.get_authorization_url(scopes)
            webbrowser.open(auth_url)
            print(bs_count, pAndl_count, company_count)
            return HttpResponse()
        response_2 = requests.get(bs_url_2, headers=headers)
        pAndl_response_2 = requests.get(pAndL_url_2, headers=headers)
        data_2 = json.loads(response_2.content)
        # print(data_2)
        pAndl_data_2 = json.loads(pAndl_response_2.content)
        convert_and_save(converter, data_2, f"{csv_folders}{bs_folder}", f'bs{bs_count}.csv')
        convert_and_save(converter, pAndl_data_2, f"{csv_folders}{pAndl_folder}", f'pAndl{pAndl_count}.csv')
        shutil.make_archive(f"{temp_folder_name}/totalzip", 'zip', csv_folders)
        with open(f"{temp_folder_name}/totalzip.zip", "rb") as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=totalzip.zip'
            f.close()
            print("BRUH IT STOPPED :0")
        # response = HttpResponse(, content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename=bs.csv'
        return response

atexit.register(exit_handler)
