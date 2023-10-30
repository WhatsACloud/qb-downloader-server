import os
import config
import shutil

def exit_handler():
    if os.path.exists(config.temp_folder_name):
        shutil.rmtree(config.temp_folder_name)


def convert_and_save(converter, data, foldername, filename):
    csv_byte_str = converter.convert(data)
    print(foldername, "does this exist?", os.path.exists(foldername))
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    print(foldername, "does this exist?", os.path.exists(foldername))
    with open(foldername + f'/{filename}', 'wb') as f:
        f.write(csv_byte_str)
        f.close()

def get_current_count(temp_folder_name):
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