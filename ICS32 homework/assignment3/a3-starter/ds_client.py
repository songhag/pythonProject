# Starter code for assignment 3 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Songhao Gao
# songhag@uci.edu
# 42515328

import socket
import json
import time
from ds_protocol import extract_json


def send(server: str, port: int, username: str,
         password: str, message: str, bio: str = None):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((server, port))
            send_file = client.makefile('w')
            recv_file = client.makefile('r')

            # Send join command
            join_cmd = json.dumps({
                "join": {
                    "username": username,
                    "password": password,
                    "token": ""
                }
            })
            send_file.write(join_cmd + '\r\n')
            send_file.flush()

            # Process join response
            join_resp = recv_file.readline()
            join_data = extract_json(join_resp)
            if join_data.type != 'ok' or not join_data.token:
                return False
            token = join_data.token

            success = True

            # Send post command if message is provided
            if message is not None:
                if message.strip() != '':
                    post_cmd = json.dumps({
                        "token": token,
                        "post": {
                            "entry": message,
                            "timestamp": time.time()
                        }
                    })
                    send_file.write(post_cmd + '\r\n')
                    send_file.flush()

                    post_resp = recv_file.readline()
                    post_data = extract_json(post_resp)
                    if post_data.type != 'ok':
                        success = False
                else:
                    print("Can't upload nothing")
                    return False
            # Send bio command if bio is provided and no errors so far
            if bio is None and success:
                return success
            if bio.strip() != '' and success:
                bio_cmd = json.dumps({
                    "token": token,
                    "bio": {
                        "entry": bio,
                        "timestamp": time.time()
                    }
                })
                send_file.write(bio_cmd + '\r\n')
                send_file.flush()

                bio_resp = recv_file.readline()
                bio_data = extract_json(bio_resp)
                if bio_data.type != 'ok':
                    success = False
            else:
                print("Can't upload nothing")
                return False

            return success
    except Exception as e:
        return False
