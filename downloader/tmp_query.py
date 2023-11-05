import downloader.config as config
import os
import shutil

# if not os.path.exists(csv_folders):
#     os.makedirs(csv_folders)

def does_file_exist(filename):
    return os.path.exists(f"{config.csv_folders}/{filename}")

def make_tmp():
    if not os.path.exists(config.csv_folders):
        os.makedirs(config.csv_folders)

def delete_tmp():
    if os.path.exists(config.temp_folder_name):
        shutil.rmtree(config.temp_folder_name)

"""Gets list of names of folders in csv_folders
"""
def get_folder_names():
    return os.listdir(config.csv_folders)