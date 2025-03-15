import socket
from typing import Callable
import bookmark_connection as bmc
from bookmark_connection import BookmarkProtocol, BookmarkServerError

# default port and host
PORT = 2024
HOST = "127.0.0.1"

# input/output messages. Keeping them together for easy translation and editing!
INPUT_MAIN_MENU = "What would you like to do? \n 1. Add a bookmark\n 2. Open a bookmark\n 3. View all bookmarks\n 4. Find a bookmark\n 5. Remove a bookmark\n 6. Quit\n"
INPUT_ADD = "Great. What bookmark would you like to add?\n"
INPUT_OPEN = "What bookmark would you like to open (enter item number)?\n"
INPUT_REMOVE = "What bookmark would you like to remove (enter item number)?\n"
INPUT_FIND = "Great. Enter a few words associated with the bookmark you want to find:\n"
MSG_OPEN_MENU = "Here is a list of your current bookmarks:\n"
MSG_EMPTY = "You currently do not have any bookmarks saved.\n"
MSG_ONLINE = "You are connected to the PyBookmarks Server.\n"
MSG_ONLINE_ERROR = "An error occurred on the PyBookmarks Server.\n"
MSG_ONLINE_SUCCESS = "Bookmark successfully added to the PyBookmarks Server.\n"

def print_bookmarks(bookmarks:list):
    print(MSG_OPEN_MENU)
    id = 0
    for b in bookmarks:
        print(f"{id}: {b[1:-3]}")
        id+=1

def call(func:Callable, conn:bmc.Connection, param:any):
    """
    call is a helper function to encapsulate error handling for commonly called 
    bookmark connection functions

    :params func: the function to be called
    :params conn: a Connection object, required by all bookmark_connection functions
    :params param: a value to be passed as parameter 2 to desired function.
    :returns: None if error, otherwise relays the return message from the called function
    """

    result = None
    try:
        result = func(conn, param) 
    except Exception as ex:
        print(ex)
    
    return result

def connect_to_server(host:str, port:int) -> socket.socket:
    try:
        # TODO: create a socket object and use it to connect to the
        # server specified by the host and port params. If created successfully, 
        # return the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock
    except:
        return None

def run():
    # create a socket connection to server, be sure server is running first!
    sock = connect_to_server(HOST, PORT)
    if sock == None:
        print(MSG_ONLINE_ERROR)
        return

    # initialize a read/write namedtuple using the established socket connection.
    _conn = bmc.init(sock)

    try:
        resp = input(INPUT_MAIN_MENU)
        while resp != '6':
            if resp == '1':
                result = call(bmc.add, _conn, input(INPUT_ADD))
                if result.protocol == BookmarkProtocol.OK:
                    print(MSG_ONLINE_SUCCESS)
                else:
                    print(MSG_ONLINE_ERROR)
            elif resp == '2':
                # Opening Bookmarks not supported in this version of PyBookmarker Online
                print("Opening Bookmarks not supported in this version of PyBookmarker Online")
            elif resp == '3':
                result = call(bmc.view_all, _conn, None)
                if result.protocol == BookmarkProtocol.OK:
                    if len(result.data)!=0:
                        res = result.data.strip('[')
                        res = res.strip(']')
                        res = res.split(', ')
                        print_bookmarks(res)
                    else:
                        print(MSG_EMPTY)
                else:
                    print(MSG_ONLINE_ERROR)
            elif resp == '4': 
                pass
                # TODO Add support finding a bookmark
            elif resp == '5':
                pass
                # TODO Add support removing a bookmark
            
            resp = input(INPUT_MAIN_MENU)
    except BookmarkServerError:
        print("An error occurred while attempting to communicate with the remote server.")    
    else:
        # only disconnect if an error did not occur
        bmc.disconnect(_conn)
    finally:
        sock.close()

if __name__ == "__main__":
    print("Welcome to PyBookmarker Online! \n")

    try:
        run()
    except: 
        print("Uh oh. The programming team for pybookmark has clearly missed handling a critical error. Please direct all complaints to the TAs! :)")

