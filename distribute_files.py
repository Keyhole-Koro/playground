import tkinter as tk
import threading
import socket
from pathlib import Path
import os
import json
import base64
from datetime import datetime
import random

import blockchain
import database as db
import p2p_communicate as p2p

bc = blockchain.Blockchain()
db = db.Database()

opponent_nodes = {}
    
def setup_nodes(number_nodes):
    keys = []
    values = []
    for i in range(number_nodes):
        key = f'user{i + 1}'
        value = random.randint(40000, 49999)
        if i > 0 and value in values:
        # Regenerate a new value
            while value == values[-1]:
                value = random.randint(40000, 49999)
        arranged_value = ['localhost', value]
        keys.append(key)
        values.append(arranged_value)
    key_value_pairs = {key: values[i % len(values)] for i, key in enumerate(keys)}
    return key_value_pairs

def convert_strdict_bytes(string:str):
    string_json = json.dumps(string)
    string_bytes = string_json.encode('utf-8')
    return string_bytes

#make more abstract(arg kwarg)
def sort_file_base64str(opponent_name, text, file:list, sender)->list:
    file_name = file['file_name']
    file_extension = file['file_extension']
    file_b_data = file['file_b_data']
    file_data_encoded = base64.b64encode(file_b_data).decode('utf-8')
    sorted_file = {
        'file_name': file_name,
        'file_extension': file_extension,
        'file_b_data': file_data_encoded
    }
    sorted_data = {
        'sender': sender,
        'text': text,
        'file': sorted_file
    }
    return sorted_data

def pull_request():
    pass

def arrange_data(file_path, file_b_data)->dict:
    file_name_ext = file_path.split('\\')[-1]
    file_name = file_name_ext.split('.')[0]
    file_extension = file_name_ext.split('.')[-1]

    file = {
        'file_name': file_name,
        'file_extension': file_extension,
        'file_b_data': file_b_data
    }
    return file

def file_part():
    pass

def split_file(file_path, file_b_data)->list:
    chunks = divide_into_chunks(file_b_data, 90000)
    file = arrange_data(file_path, None)
    files = []
    for c in range(len(chunks)):
        chunk = chunks[c]
        file['part_num'] = c
        file['file_b_data'] = chunk
        files.append(file)
    return files

def divide_into_chunks(string, chunk_size)->list:
    chunks = [string[i:i+chunk_size] for i in range(0, len(string), chunk_size)]
    return chunks

def put_out(node):
    return opponent_nodes[node]
    
def listening(address):
    ip, port = addresses[address]
    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receive_socket.bind((ip, port))
    receive_socket.listen()
    while True:
        try:
            client_socket, client_address = receive_socket.accept()
            data = json.loads(client_socket.recv(1000000).decode())
            sender = data['sender']
            text = None
            file = None
            if data['text']:
                text = data['text']
                print(f'{sender}:{text}')
            if data['file']:
                file = data['file']
                file_path = f'C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/files/{file["file_name"]}.{file["file_extension"]}'
                with open(file_path, 'wb') as new_file:
                    new_file.write(base64.b64decode(file['file_b_data']))
                file['file_path'] = file_path
            db.insert(sender = sender, text = text, file = file)
            print(db.get(text, file))
        except Exception:
                pass

def listen_request(client_name):
    ip_address, port = addresses[client_name]
    print(client_name, ip_address, port)
    print('listen_request')
    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('listen_request1')
    receive_socket.bind((ip_address, port))
    print('listen_request2')
    receive_socket.listen()
    print('listen_request3')
    while True:
        try:
            print('listen_request4')
            client_socket, client_address = receive_socket.accept()
            data = json.loads(client_socket.recv(1000).decode())
            sender = data['sender']
            text = None
            file = None
            if data['text']:
                text = data['text']
                print(f'{sender}:{text}')
            if data['file']:
                file = data['file']
                file_name = file['file_name']
                file_extension = file['file_extension']
        except Exception:
                pass

def dispatch_request(l_file=[], sender=None):
    request = {
        'sender': sender,
        'carrier': None,
        'file': l_file,
        'timestamp': blockchain.add_timestamp()
    }
    spread_count = 0
    for op_ip, op_port in put_out(sender):
        if spread_count > 10:
            break
        try:
            with p2p.p2pconnect_to(op_ip, op_port) as op_socket:
                request['carrier'] = {
                'ip': op_ip,
                'port': op_port
                }
                op_socket.sendall(request)
            spread_count += 1
        except socket.error as e:
            print(f"Error connecting to node {op_ip}:{op_port}: {e}")

#have yet to handle list
def transmit_data(text=None, l_file=[], sender=None):
    try:
        for part in range(len(l_file)):
            data = sort_file_base64str(text, file, sender)
            data_bytes = convert_strdict_bytes(data)
            with p2p.p2pconnect_to(op_ip, op_port) as op_socket:#ip port have yet to
                op_socket.sendall(data_bytes)
                bc.add_block(data_bytes)
        else:
            print(f"Opponent '{opponent_name}' does not exist in node.")
    except KeyError as e:
        print(f"KeyError: '{e}' does not exist.")
    except Exception as e:
        print('Error:', e)
    except ValueError as v:
        print('ValueError:', v)

if __name__ == '__main__':
    addresses = setup_nodes(20)
    for key, value in addresses.items():
        node_values = []
        for address in addresses:
            probability = random.randint(1, 3)
            if probability == 1 and key != address:
                node_values.append(key)
        opponent_nodes[key] = node_values
    listening_threads = []
    for address in addresses.keys():
        listening_thread = threading.Thread(target=listen_request, args=(address,))
        listening_thread.start()
        listening_threads.append(listening_thread)
    for thread in listening_threads:
        thread.join()
    print('passed')
    user = {
    'ip':'localhost',
    'port':50000
    }
    file_path = "/Users/katsukawakiho/Desktop/blockchain-playground/playground/received_video2.mp4"
    request = arrange_data(file_path, None)
    dispatch_request(request, user)
