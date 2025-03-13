from ds_messenger import *
import time

# Server details
server_address = '127.0.0.1'  # localhost
username = 'testuser123'
password = 'password123'

server_address2 = '127.0.0.1'  # localhost
username2 = 'user2'
password2 = '12'
# Create a DirectMessenger instance and connect to the server
messenger = DirectMessenger(
    dsuserver=server_address,
    username=username,
    password=password
)
messenger2 = DirectMessenger(
    dsuserver=server_address2,
    username=username2,
    password=password2
)
# Check if connection was successful
if messenger.success:
    print(f"Successfully connected as {username}")

    # Send a test message to another user (let's say 'user2')
    recipient = 'user2'
    message = "Hello! This is a test message."

    # Send the message
    send_success = messenger.send(message, recipient)

    if send_success:
        print(f"Message sent successfully to {recipient}")
    else:
        print("Failed to send message")
else:
    print("Failed to connect to the server")


if messenger.success:
    print(messenger.retrieve_all())