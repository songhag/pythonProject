import socket
from collections import namedtuple
from pathlib import Path
import bookmark_connection as bmc
from bookmarker import Bookmarker

BOOKMARK_PATH = "."
BOOKMARK_FILE = "pybookmark.txt"

PORT = 2024
HOST = "127.0.0.1"



def store(_conn: bmc.Connection, bm: Bookmarker, url: str): 
    '''
    store will send the command specified by the parameters and return a response to the command. 

    url: the URL of the webpage to bookmark
    status: either 0 or 1 to indicate the status of the command specified in the url parameter
    '''
    try:
        bm.add(url)
        status = bmc.BookmarkProtocol(bmc.BookmarkProtocol.OK)
    except ValueError:
        status = bmc.BookmarkProtocol(bmc.BookmarkProtocol.ERROR)

    # send a response back to client to confirm receipt of message
    bmc._write_command(_conn, bmc.BookmarkProtocol.format(status))

def view_all(_conn: bmc.Connection, bm: Bookmarker):
    try:
        bookmarks = bm.read_notes()
        print(type(bookmarks))
        status = bmc.BookmarkProtocol(bmc.BookmarkProtocol.OK, bookmarks)
    except:
        status = bmc.BookmarkProtocol(bmc.BookmarkProtocol.ERROR)
    bmc._write_command(_conn, bmc.BookmarkProtocol.format(status))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    # the file used to store bookmarks
    p = Path(BOOKMARK_PATH) / BOOKMARK_FILE

    # if file does not exist, create it.
    if not p.exists():
        p.touch()

    # instantiate the bookmark class and pass to run 
    bm = Bookmarker(p)
    srv.bind((HOST, PORT))
    srv.listen()

    print("server listening on port", PORT)
    while True:
        connection, address = srv.accept()

        with connection:
            print("client connected")
            _bmc_conn = bmc.init(connection)

            while True:
                rec_msg = bmc.listen(_bmc_conn)
                
                # assume an empty message means client has disconnected so break
                # and wait for new connection
                if rec_msg == '': break

                print("message: ", rec_msg)

                try:
                    # convert message to protocol format
                    bm_msg = bmc.BookmarkProtocol.open(rec_msg)
                    # perform operation depending on protocol type
                    if bm_msg.protocol == bmc.BookmarkProtocol.ADD:
                        store(_bmc_conn, bm, bm_msg.data)
                    elif bm_msg.protocol == bmc.BookmarkProtocol.VIEW_ALL:
                        view_all(_bmc_conn, bm)
                except Exception as ex:
                    bmc.error(_bmc_conn)
                    print(ex)
                    break
            
            print("client disconnected")

