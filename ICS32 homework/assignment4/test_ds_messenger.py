# test_ds_messenger.py
import uuid
from ds_messenger import DirectMessenger

def test_connect_success():
    """Test successful connection with valid credentials."""
    username = str(uuid.uuid4())
    password = "testpass"
    dm = DirectMessenger(dsuserver='localhost', username=username, password=password)
    assert dm.success is True
    assert dm.token is not None

def test_connect_invalid_password():
    """Test connection failure with invalid password."""
    username = str(uuid.uuid4())
    password = "valid_pass"
    # Create user first
    DirectMessenger(dsuserver='localhost', username=username, password=password)
    # Attempt login with wrong password
    dm_invalid = DirectMessenger(dsuserver='localhost', username=username, password="wrong_pass")
    assert dm_invalid.success is False
    assert dm_invalid.token is None

def test_send_and_retrieve_new_message():
    """Test sending a message and retrieving it as a new message."""
    sender_name = str(uuid.uuid4())
    recipient_name = str(uuid.uuid4())
    password = "pass"

    # Ensure recipient exists
    DirectMessenger(dsuserver='localhost', username=recipient_name, password=password)

    # Send message
    sender = DirectMessenger(dsuserver='localhost', username=sender_name, password=password)
    assert sender.send("Hello, pytest!", recipient_name) is True

    # Retrieve new messages as recipient
    recipient = DirectMessenger(dsuserver='localhost', username=recipient_name, password=password)
    new_messages = recipient.retrieve_new()
    assert len(new_messages) == 1
    assert new_messages[0].message == "Hello, pytest!"
    assert new_messages[0].recipient == sender_name  # 'recipient' field stores the sender's username for incoming messages

def test_retrieve_all_messages():
    """Test retrieving all messages (sent and received)."""
    sender_name = str(uuid.uuid4())
    recipient_name = str(uuid.uuid4())
    password = "pass"

    # Create users
    sender = DirectMessenger(dsuserver='localhost', username=sender_name, password=password)
    DirectMessenger(dsuserver='localhost', username=recipient_name, password=password)

    # Send two messages
    assert sender.send("First message", recipient_name) is True
    assert sender.send("Second message", recipient_name) is True

    # Retrieve all messages as recipient
    recipient = DirectMessenger(dsuserver='localhost', username=recipient_name, password=password)
    all_messages = recipient.retrieve_all()
    assert len(all_messages) >= 2
    messages_content = [msg.message for msg in all_messages]
    assert "First message" in messages_content
    assert "Second message" in messages_content

def test_send_empty_message():
    """Test sending an empty message (should fail)."""
    username = str(uuid.uuid4())
    dm = DirectMessenger(dsuserver='localhost', username=username, password="pass")
    assert dm.send("", "recipient") is False

def test_retrieve_no_new_messages():
    """Test retrieving new messages when none exist."""
    username = str(uuid.uuid4())
    dm = DirectMessenger(dsuserver='localhost', username=username, password="pass")
    assert dm.retrieve_new() == []