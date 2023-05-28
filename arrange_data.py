import os
import json
import base64
from datetime import datetime
import random

def convert_str_bytes(string:str):
    string_json = json.dumps(string)
    string_bytes = string_json.encode('utf-8')
    return string_bytes

def convert_bytes_str(data)->dict:
    encoded_data = {}
    for key, value in data.items():
        if isinstance(value, bytes):
            encoded_data[key] = base64.b64encode(value).decode('utf-8')
        elif isinstance(value, dict):
            encoded_data[key] = {}
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, bytes):
                    encoded_data[key][sub_key] = base64.b64encode(sub_value).decode('utf-8')
                else:
                    encoded_data[key][sub_key] = sub_value
        else:
            encoded_data[key] = value
    return encoded_data

def convert_to_base64(data):
    if isinstance(data, str):
        # Convert string to Base64
        data_bytes = data.encode('utf-8')
        base64_data = base64.b64encode(data_bytes).decode('utf-8')
        return base64_data
    elif isinstance(data, bytes):
        # Convert bytes to Base64
        base64_data = base64.b64encode(data).decode('utf-8')
        return base64_data
    elif isinstance(data, bytearray):
        # Convert bytearray to Base64
        base64_data = base64.b64encode(bytes(data)).decode('utf-8')
        return base64_data
    elif isinstance(data, (list, tuple)):
        # Convert list or tuple elements to Base64
        base64_data = [convert_to_base64(item) for item in data]
        return base64_data
    elif isinstance(data, dict):
        # Convert dictionary values to Base64
        base64_data = {key: convert_to_base64(value) for key, value in data.items()}
        return base64_data
    else:
        # Unsupported data format
        raise ValueError(f"Unsupported data format: {type(data)}")

def create_dict(**old_dict)->dict:
    new_dict = dict(old_dict)
    return new_dict

def arrange_file(**old_dict)->dict:
    if 'file_path' in old_dict:
        file_name = os.path.basename(old_dict['file_path'])
        file_extension = os.path.splitext(file_name)[1]
        old_dict['file_name'] = fine_name
        old_dict['file_extension'] = file_extension
        old_dict.pop('file_path')
    if 'file_data' in old_dict:
        b_data = convert_to_base64(old_file['file_data'])
        old_dict['file_b_data'] = b_data
        old_dict.pop('file_data')
    new_dict = create_dict(old_dict):
    return new_dict

def file_apart():
    pass

def split_file_data(file_path, file_b_data)->list:
    chunks = divide_into_chunks(file_b_data, 90000)
    file = arrange_data(file_path, None)
    files = []
    for index, chunk in enumerate(chunks):
        file['part_num'] = index
        file['file_b_data'] = chunk
        files.append(file)
    return files

def divide_into_chunks(string, chunk_size)->list:
    chunks = [string[i:i+chunk_size] for i in range(0, len(string), chunk_size)]
    return chunks

def reconstitute():
    pass
