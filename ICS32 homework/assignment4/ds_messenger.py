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
        self.success=self._connect()
        self.send_file = None
        self.recv_file = None

    def _connect(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, self.port))
                self.send_file = client.makefile('w')
                self.recv_file = client.makefile('r')

                # Send join command
                join_cmd = join_message(self.username, self.password)

                self.send_file.write(join_cmd + '\r\n')
                self.send_file.flush()

                # Process join response
                join_resp = self.recv_file.readline()
                join_data = extract_json(join_resp)
                if join_data.type != 'ok' or not join_data.token:
                    return False
                self.token = join_data.token

                return True
        except:
            return False

    def send(self, message: str, recipient: str) -> bool:
        # must return true if message successfully sent, false if send failed.
        if self.success:
            if message is not None:
                if message.strip() != '':
                    msg = format_direct_message(self.token, message, recipient, time.time())

                    self.send_file.write(msg + '\r\n')
                    self.send_file.flush()

                    resp = self.recv_file.readline()
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

            self.send_file.write(msg + '\r\n')
            self.send_file.flush()

            resp = self.recv_file.readline()
            data = extract_json(resp)
            if data.type != 'ok':
                self.success = False

            return data.message
        else:
            print("Fail to connect")
            return []

    def retrieve_all(self) -> list:
        # must return a list of DirectMessage objects containing all messages
        if self.success:
            msg = retrieve_messages(self.token, 'new')

            self.send_file.write(msg + '\r\n')
            self.send_file.flush()

            resp = self.recv_file.readline()
            data = extract_json(resp)
            if data.type != 'ok':
                self.success = False

            return data.message
        else:
            print("Fail to connect")
            return []