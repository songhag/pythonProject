import socket
import json

from ds_protocol import *

class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.port = 3001
        self.username = username
        self.password = password
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.success = self._connect()

    def _connect(self):
        try:
            self.client.connect((self.dsuserver, self.port))
            send_file = self.client.makefile('w')
            recv_file = self.client.makefile('r')

            # Send join command
            join_cmd = join_message(self.username, self.password)

            send_file.write(join_cmd + '\r\n')
            send_file.flush()

            # Process join response
            join_resp = recv_file.readline()
            join_data = extract_json(join_resp)
            if join_data.type != 'ok' or not join_data.token:
                return False
            self.token = join_data.token

            return True
        except Exception as e:
            print(e)
            return False

    def send(self, message: str, recipient: str) -> bool:
        # must return true if message successfully sent, false if send failed.
        if self.success:
            if message is not None:
                if message.strip() != '':
                    msg = format_direct_message(self.token, message, recipient, time.time())

                    send_file = self.client.makefile('w')
                    recv_file = self.client.makefile('r')
                    send_file.write(msg + '\r\n')
                    send_file.flush()

                    resp = recv_file.readline()
                    data = extract_json(resp)
                    if data.type != 'ok':
                        self.success = False
                    return self.success
                else:
                    print("Can't send nothing")
                    return False
        else:
            print("Fail to connect")
            return False


    def retrieve_new(self) -> list:
        # must return a list of DirectMessage objects containing all new messages
        if self.success:
            msg = retrieve_messages(self.token, 'new')

            send_file = self.client.makefile('w')
            recv_file = self.client.makefile('r')
            send_file.write(msg + '\r\n')
            send_file.flush()

            resp = recv_file.readline()
            data = extract_json(resp)
            if data.type != 'ok':
                self.success = False

            # Convert server response to DirectMessage objects
            messages = data.messages
            dm_list = []
            for msg_dict in messages:
                dm = DirectMessage()
                if 'from' in msg_dict:  # Received message (new messages are only incoming)
                    dm.recipient = msg_dict.get('from')
                    dm.message = msg_dict.get('message')
                    dm.timestamp = msg_dict.get('timestamp')
                dm_list.append(dm)
            return dm_list
        else:
            print("Fail to connect")
            return []

    def retrieve_all(self) -> list:
        # must return a list of DirectMessage objects containing all messages
        if self.success:
            msg = retrieve_messages(self.token, 'all')

            send_file = self.client.makefile('w')
            recv_file = self.client.makefile('r')
            send_file.write(msg + '\r\n')
            send_file.flush()

            resp = recv_file.readline()
            data = extract_json(resp)
            if data.type != 'ok':
                self.success = False

            # Convert server response to DirectMessage objects
            messages = data.messages
            dm_list = []
            for msg_dict in messages:
                dm = DirectMessage()
                if 'from' in msg_dict:  # Received message
                    dm.recipient = self.username
                    dm.message = msg_dict.get('message')
                    dm.timestamp = msg_dict.get('timestamp')
                else:  # Sent message
                    dm.recipient = msg_dict.get('recipient')
                    dm.message = msg_dict.get('message')
                    dm.timestamp = msg_dict.get('timestamp')
                dm_list.append(dm)
            return dm_list
        else:
            print("Fail to connect")
            return []

    def __del__(self): #close the client
        self.client.close()