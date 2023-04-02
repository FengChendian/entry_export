import base64
import json

def get_pdf_base64(file_path:str):
    with open(file_path, "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read())
    return encoded_string.decode("ascii")
    # print(encoded_string)
def get_secret_info() -> dict:
    with open('./tencent_config.json', "r") as config_file:
        config_dict = json.load(config_file)
    return config_dict
# print(config_dict)