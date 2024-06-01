

import socket
import threading
from queue import Queue
import json
import base64
import cv2
from PIL import Image
import io
import numpy as np


HOST = "10.0.1.197"
PORT = 1234

class PiClient():
    stop_event: threading.Event     # Event to signal the termination of the thread.
    client_queue: Queue             # Queue to transfer data from the subthread to the main thread.
    thread: threading.Thread        # Client thread to maintain client-server connection.

    def __init__(self):
        """
        Initializes stop event & client queue
        """
        # Create an event to signal the subthreads to safely stop execution.
        self.stop_event = threading.Event()

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
        pi_thread: threading.Thread
        pi_thread = threading.Thread(
            target=self.handle_connection_tcp, args=(self.stop_event,)
        )
        return pi_thread
    
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
            conn: socket.socket
            conn, _ = sock.accept()
            print("connected pi")

        # Handle socket timeout
        except socket.timeout:
            print("Failed to connect to GMS2 due to timeout.\nTry increasing timeout length in settings.ini")
            return False
        except Exception as e:
            raise e

        with conn:  
            self.mainloop(stop_event, conn)

    def mainloop(self, stop_event: threading.Event, conn:socket.socket) -> None:
        """
        Send messages to the GMS2 server if any are queued.
        """

        # if the pi has sent an image (pi queue not empty), process it
        while not stop_event.is_set():

            
            received_data = self.receive_data(conn)
            received_data = json.loads(received_data)

            if received_data["has_image"]:

                image = self.convert_bytes_to_image(received_data)

                self.client_queue.put(image)

                self.send_response(conn)

            else:

                self.send_response(conn)




        return None
            
    def receive_data(self,conn):
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


    

    def convert_bytes_to_image(self,parsed_data):
        # Retrieve the base64-encoded image data
        base64_image_data = parsed_data['screenshotPNG']

        # Decode the base64 string to bytes
        image_data_bytes = base64.b64decode(base64_image_data)

        # Create a BytesIO object from tfhe decoded bytes
        image_stream = io.BytesIO(image_data_bytes)

        # Open the image using PIL (Pillow)
        image = Image.open(image_stream)

        # Convert the PIL Image to a NumPy array
        image_array = np.array(image)

        # Convert RGB to BGR (this step is necessary only if your image is in color)
        image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)


        image_np = np.asarray(image)

        return image_np
    
    def send_response(self, conn):
            
            
            
            success_response = {"take_photo": True}
            json_data = json.dumps(success_response) + "\n"
            data = json_data.encode('utf-8')
            conn.send(data)