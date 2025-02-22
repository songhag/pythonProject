# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Songhao Gao
# songhag@uci.edu
# 42515328

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.

DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object

    '''
    try:
        json_obj = json.loads(json_msg)
        response = json_obj.get('response', {})
        data_type = response.get('type', 'error')
        message = response.get('message', '')
        token = response.get('token', '')
        return DataTuple(data_type, message, token)
    except json.JSONDecodeError:
        return DataTuple('error', 'Invalid JSON', '')
    except Exception as e:
        return DataTuple('error', str(e), '')
