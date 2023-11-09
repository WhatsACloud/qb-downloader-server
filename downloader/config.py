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
debug = config['DEBUG']
DEV_CONTACT = config['DEV_CONTACT_DETAILS']

temp_folder_name = "/tmp/django_temp"
csv_folders = temp_folder_name + "/csv_folders"

scopes = [Scopes.ACCOUNTING]

CONTACT_DEV_MSG = f"If the problem persists, it is likely to be a developer error (in which case, please contact the developer at {DEV_CONTACT})."

LOG_LOCATION = os.path.join(os.getcwd(), "log.txt")