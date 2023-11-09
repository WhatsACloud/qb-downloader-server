import downloader.config as config
import downloader.utils as utils
from converter import Converter
import api_response_handler as api
import downloader.tmp_query as tmp_query

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
    def __init__(self, company_id, access_token):
        self.company_id = company_id
        self.urls = {}
        self.urls["pAndL"] = self.new_url(pAndL_sub_url)
        self.urls["bs"] = self.new_url(bs_sub_url)
        self.headers = {
            'Authorization': f"Bearer {access_token}",
            'Accept': 'application/json'
        }
    
    def get_res(self, url):
        return api.get_res(url, self.headers)
    
    def is_already_saved(self):
        name = self.name or self.get_name()
        return tmp_query.does_file_exist(name)

    def get_name(self):
        company_info_url = f"{get_base_url()}/v3/company/{self.company_id}/query?query=select+%2A+from+CompanyInfo"
        # company_info_url = f"{get_base_url()}/v3/company/{self.company_id}/query?query=select+ajfsj+from+CompanyInfo"
        
        data = self.get_res(company_info_url)
        self.name = data["QueryResponse"]["CompanyInfo"][0]["CompanyName"]

    def new_url(self, sub_url):
        return f"{get_base_url()}/v3/company/sjdfdsjf/reports/{sub_url}?minorversion=69"
        # return f"{get_base_url()}/v3/company/{self.company_id}/reports/{sub_url}?minorversion=69"

    def save_sheet(self, converter, url, location, company_name, base_filename):
        data = self.get_res(url)
        utils.convert_and_save(converter, data, f"{location}/{company_name}", f'{base_filename}.csv')

    def save_all_sheets(self, location):
        self.save_sheet(converter, self.urls["bs"], location, self.name, "bs")
        self.save_sheet(converter, self.urls["pAndL"], location, self.name, "pAndL")