import yaml
from intuitlib.enums import Scopes
import os

config_path = os.path.join(os.path.abspath(os.curdir), "config.yaml")
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

client_id = config['CLIENT_ID']
client_secret = config['CLIENT_SECRET']
redirect_uri = config['REDIRECT_URI']
environment = config['ENVIRONMENT']

company_list = config['company_id_list']

temp_folder_name = "/tmp/django_temp"
csv_folders = temp_folder_name + "/csv_folders"

scopes = [Scopes.ACCOUNTING]