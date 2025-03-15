import json
import ds_protocol

def test_extract_json_valid():
    json_msg = '{"response": {"type": "ok", "messages": ["hello"], "token": "abc123"}}'
    result = ds_protocol.extract_json(json_msg)
    assert result.type == 'ok'
    assert result.messages == ["hello"]
    assert result.token == 'abc123'

def test_extract_json_invalid():
    json_msg = 'not a json'
    result = ds_protocol.extract_json(json_msg)
    assert result.type == 'error'
    assert 'Invalid JSON' in result.messages

def test_extract_json_missing_response():
    json_msg = '{"something": "else"}'
    result = ds_protocol.extract_json(json_msg)
    assert result.type == 'error'
    assert result.messages == ''
    assert result.token == ''

def test_extract_json_message_key():
    json_msg = '{"response": {"type": "ok", "message": "success", "token": "abc"}}'
    result = ds_protocol.extract_json(json_msg)
    assert result.messages == "success"

def test_extract_json_both_message_keys():
    json_msg = '{"response": {"type": "ok", "messages": ["msg1"], "message": "success", "token": "abc"}}'
    result = ds_protocol.extract_json(json_msg)
    assert result.messages == ["msg1"]

def test_join_message():
    username = "user123"
    password = "pass456"
    join_cmd = ds_protocol.join_message(username, password)
    data = json.loads(join_cmd)
    assert data['join']['username'] == username
    assert data['join']['password'] == password
    assert data['join']['token'] == ""

def test_join_message_empty_inputs():
    join_cmd = ds_protocol.join_message("", "")
    data = json.loads(join_cmd)
    assert data['join']['username'] == ""
    assert data['join']['password'] == ""

def test_format_direct_message():
    token = "token123"
    entry = "Hello!"
    recipient = "bob"
    timestamp = 123456.789
    cmd = ds_protocol.format_direct_message(token, entry, recipient, timestamp)
    data = json.loads(cmd)
    assert data['token'] == token
    assert data['directmessage']['entry'] == entry
    assert data['directmessage']['recipient'] == recipient
    assert data['directmessage']['timestamp'] == timestamp

def test_format_direct_message_string_timestamp():
    cmd = ds_protocol.format_direct_message("token", "entry", "recipient", "now")
    data = json.loads(cmd)
    assert data['directmessage']['timestamp'] == "now"

def test_retrieve_messages():
    token = "token123"
    for mode in ['new', 'all']:
        cmd = ds_protocol.retrieve_messages(token, mode)
        data = json.loads(cmd)
        assert data['token'] == token
        assert data['directmessage'] == mode