from decouple import config
from django.http import HttpResponse
from django.shortcuts import render
from intuitlib.client import AuthClient
import requests
import json
import sys
sys.path.append("downloader")
from converter import Converter

output_filename = "test.csv"

# Create your views here.

client_id = config('CLIENT_ID')
client_secret = config('CLIENT_SECRET')
redirect_uri = config('REDIRECT_URI')
environment = config('ENVIRONMENT')
# Instantiate client
auth_client = AuthClient(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    environment=environment, # “sandbox” or “production”
)

pAndL_base_url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365268313780/reports/ProfitAndLossDetail"
bs_base_url = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365268313780/reports/BalanceSheet"

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

pAndL_class_url = Url(pAndL_base_url)
pAndL_class_url.add("minorversion", "65")
pAndL_url = pAndL_class_url.get()

bs_class_url = Url(bs_base_url)
bs_class_url.add("minorversion", "65")
bs_url = bs_class_url.get()

def index(request):
    if request.method == "GET":
        code = request.GET.get("code", "")
        state = request.GET.get("state", "")
        realm_id = request.GET.get("realmId", "")
        auth_client.get_bearer_token(code, realm_id=realm_id)
        auth_header = f'Bearer {auth_client.access_token}'
        headers = {
            'Authorization': auth_header,
            'Accept': 'application/json'
        }
        response = requests.get(bs_url, headers=headers)
        data = json.loads(response.content)
        converter = Converter()
        csv_byte_str = converter.convert(data)
        response = HttpResponse(csv_byte_str, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=bs.csv'
        return response
