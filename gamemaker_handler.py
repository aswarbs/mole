

import socket
import threading
from queue import Queue
import json
import base64
import cv2
from PIL import Image
import io
import numpy as np


HOST = "10.0.3.255"
PORT = 9999


class GMS2Client():
    stop_event: threading.Event     # Event to signal the termination of the thread.
    client_queue: Queue             # Queue to transfer data from the subthread to the main thread.
    thread: threading.Thread        # Client thread to maintain client-server connection.

    def __init__(self):
        """
        Initializes stop event & client queue
        """
        # Create an event to signal the subthreads to safely stop execution.
        self.stop_event = threading.Event()
        self.conn = None

        self.client_queue = Queue()

    def start_thread(self) -> None:
        """
        Initialise & Start the Client thread.
        """

        self.thread = self.create_thread()
        self.thread.start()

    def create_thread(self) -> threading.Thread:
        """
        Create the Client thread.
        Returns: the client thread instance.
        """

        # ',' used in thread args to convert the single argument to a tuple.
        gm_thread: threading.Thread
        gm_thread = threading.Thread(
            target=self.handle_connection_tcp, args=(self.stop_event,)
        )
        return gm_thread
    
    def stop_thread(self) -> None:
        """
        Stop the client thread using the stop_event.
        """

        self.stop_event.set()
        self.thread.join()

    def handle_connection_tcp(self, stop_event:threading.Event) -> bool:
        """
        Initialise the connection to the server.
        Handle message transmission between the client and server.

        Args:
            client_queue: A Queue shared between the client thread and controller. Stores messages to be sent from the client to the server.
            stop_event: A threading.Event instance that will be set once the thread should terminate.
        """

        # Initialise the socket and bind it to the specified host, at the specified port.
        sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.bind((HOST, PORT))
        print("listening")
        sock.listen()

        # Attempt connection to the server.
        try:
            self.conn: socket.socket
            self.conn, _ = sock.accept()
            print("connected gamemaker")

        # Handle socket timeout
        except socket.timeout:
            print("Failed to connect to GMS2 due to timeout.\nTry increasing timeout length in settings.ini")
            return False
        except Exception as e:
            raise e

        with self.conn:  
            self.mainloop(stop_event, self.conn)

    def mainloop(self, stop_event: threading.Event, conn:socket.socket) -> None:
        """
        Send messages to the GMS2 server if any are queued.
        """

        self.send_response("")

        # if the pi has sent an image (pi queue not empty), process it
        while not stop_event.is_set():

            if not self.client_queue.empty():
                pass






        return None


    def receive_data(self, conn):
        # Initialize an empty byte string to accumulate data
        received_data = b""  

        while True:
            # Receive 1024 bytes of data
            data = conn.recv(1024)

            # Append the newly received data to the current item of data being collected
            received_data += data  

            # If the message delimiter is in the message, the end of the message has been found
            if b'\n' in data:
                break

        return received_data

            
    def send_response(self, contours):
            
            if self.conn is None:
                return
            

            success_response = {"contours": contours}
            
            self.conn.send(json.dumps(success_response).encode('utf-8') + b'\n')

    def send_button_response(self, button):

        if self.conn is None:
            return
        
        response = {"button": button}
        self.conn.send(json.dumps(response).encode('utf-8') + b'\n')