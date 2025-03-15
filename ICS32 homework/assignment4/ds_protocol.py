# ds_protocol.py

# Starter code for assignment 3 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Songhao Gao
# songhag@uci.edu
# 42515328
import time
import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.

DataTuple = namedtuple('DataTuple', ['type', 'messages', 'token'])


def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json
    string and convert it to a DataTuple object

    '''
    try:
        json_obj = json.loads(json_msg)
        response = json_obj.get('response', {})
        data_type = response.get('type', 'error')
        messages = response.get('messages', response.get('message', ''))
        token = response.get('token', '')
        return DataTuple(data_type, messages, token)
    except json.JSONDecodeError:
        return DataTuple('error', 'Invalid JSON', '')
    except Exception as e:
        return DataTuple('error', str(e), '')


def join_message(username,password):
    join_cmd = json.dumps({
        "join": {
            "username": username,
            "password": password,
            "token": ""
        }
    })
    return join_cmd


def format_direct_message(token, entry, recipient, timestamp):
    direct_cmd = json.dumps({
        "token": token,
        "directmessage": {
            "entry": entry,
            "recipient": recipient,
            "timestamp": timestamp
        }
    })
    return direct_cmd

def retrieve_messages(token, mode):
    retrieve_cmd = json.dumps({
        "token": token,
        "directmessage": mode
    })
    return retrieve_cmd


