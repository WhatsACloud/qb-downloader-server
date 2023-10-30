import config
import requests
import json
import utils
from converter import Converter

converter = Converter()

pAndL_sub_url = "ProfitAndLossDetail"
bs_sub_url = "BalanceSheet"

def get_base_url():
    if config.environment == "sandbox":
        return "https://sandbox-quickbooks.api.intuit.com"
    elif config.environment == "production":
        return "https://quickbooks.api.intuit.com"
    raise Exception("Environment not specified or not recognised! In config.ini, please enter entry 'environment' with a value of either 'sandbox' or 'production'.")

class Url:
    def __init__(self, base_url):
        self.base_url = base_url
        self.params = {}
    def add_param(self, name, value):
        self.params[name] = value
    # def join_url_path_string(self, url_path):
    #     if self.base_url[-1] == "/" and url_path[0] == "/":
    #         return self.base_url + url_path[1:]
    #     if self.base_url[-1] != "/" and url_path[0] != "/":
    #         return self.base_url + "/" + url_path
    #     return self.base_url + url_path
    # def join_url_path(self, url_path):
    #     new_url = Url(self.join_url_path_string(url_path))
    #     new_url.params = dict.copy(self.params)
    #     return new_url
    def get(self):
        base_url = f"{self.base_url}?"
        for name in self.params:
            base_url += f"{name}={self.params[name]}"
            base_url += "&"
        base_url = base_url[:-1]
        return base_url

class Company:
    """
    Where sub_url is the text in the following API url

    full_url = "https://sandbox-quickbooks.api.intuit.com/v3/company/[insert company_id]/reports/[sub_url]?minorversion=69"

    NOTE: only works for "reports" APIs, such as the following:
    1. Balance Sheet (BalanceSheet)
    2. Profit and loss (ProfitAndLossDetail)
    """
    def __init__(self, name, company_id):
        self.name = name
        self.company_id = company_id
        self.urls = {}
        self.urls["pAndL"] = self.new_url(pAndL_sub_url)
        self.urls["bs"] = self.new_url(bs_sub_url)
    
    def new_url(self, sub_url):
        return f"{get_base_url()}/v3/company/{self.company_id}/reports/{sub_url}?minorversion=69"

    def save_sheet(self, converter, url, headers, company_name, base_filename):
        response = requests.get(url, headers=headers)
        data = json.loads(response.content)
        utils.convert_and_save(converter, data, f"{config.csv_folders}/{company_name}", f'{base_filename}.csv')

    def save_all_sheets(self, headers, company_name):
        self.save_sheet(converter, self.urls["bs"], headers, company_name, "bs")
        self.save_sheet(converter, self.urls["pAndL"], headers, company_name, "pAndL")

class CompanyList:
    def __init__(self, company_list):
        self.key_list = list(company_list.keys())
        self.company_list = {x: Company(x, company_list[x]) for x in self.key_list}
        self.current = 0
    
    def get_next(self):
        if self.is_last():
            return None
        self.current += 1
        key = self.key_list[self.current-1]
        return self.company_list[key]

    def is_last(self):
        if self.current >= len(self.key_list):
            return True
        return False

company_list = CompanyList(config.company_list)