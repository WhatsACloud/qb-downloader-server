import os
import shutil
import downloader.tmp_query as tmp_query
import json
from django.http import HttpResponse
from intuitlib.exceptions import AuthClientError

def is_api_err(data: dict):
    if type(data) != dict:
        raise ValueError(f"data should be datatype 'dict', not datatype {type(data)}")
    return "Fault" in data and "type" in data["Fault"]
    # return data.get("Fault") and data["Fault"].get("Error") and data["Fault"]["Error"].get("type")

def ami_invalid_grant_err(err: AuthClientError):
    if err.status_code == 400:
        try:
            loaded_json = json.loads(err.content)
            if loaded_json["error"] == "invalid_grant":
                return True
        except json.JSONDecodeError as _:
            return False
    return False

def save_as_zip(zipfile_name, source_folder_location):
    response = None
    shutil.make_archive(zipfile_name, 'zip', source_folder_location)
    with open(f"{zipfile_name}.zip", "rb") as f:
        response = HttpResponse(f.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=totalzip.zip'
        f.close()
        print("Finished!")
    return response

def exit_handler():
    tmp_query.delete_tmp()

def convert_and_save(converter, data, foldername, filename):
    # csv_byte_str = converter.convert(data)
    # json_obj = json.loads(data)
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    with open(foldername + f'/{filename}', 'wb') as f:
        # f.write(csv_byte_str)
        formatted_str = json.dumps(data, indent=2)
        f.write(str.encode(formatted_str))
        f.close()

def get_current_count(temp_folder_name):
    bs_count = 1
    pAndl_count = 1
    for r, d, f in os.walk(temp_folder_name):
        for file in f:
            if file.startswith("bs"):
                bs_count += 1
            if file.startswith("pAndl"):
                pAndl_count += 1
    return bs_count, pAndl_count