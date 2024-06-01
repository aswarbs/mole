import serial
from time import sleep
import sys
import threading
from queue import Queue

COM = '/dev/tty.usbmodem102'
BAUD = 9600


class Button():

    def __init__(self):

        # Create an event to signal the subthreads to safely stop execution.
        self.stop_event = threading.Event()

        self.client_queue = Queue()

        self.done = True

        try:
            self.ser = serial.Serial(COM, BAUD, timeout=1)
        except serial.SerialException as e:
            print(f"Error: {e}")
            sys.exit(1)

        print('Waiting for device')
        sleep(1)
        print(f"Connected to: {self.ser.name}")

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
            target=self.mainloop, args=(self.stop_event,)
        )
        return gm_thread
    
    def stop_thread(self) -> None:
        """
        Stop the client thread using the stop_event.
        """

        self.stop_event.set()
        self.thread.join()



    def mainloop(self, stop_event):
        # Check args
        try:
            while True:

                val = self.ser.readline().decode().strip()

                
                """if not self.done:
                    continue"""

                if val:

                    if "D10" in val:
                        print("D10 pressed")
                        self.client_queue.put("D10")
                        self.done = False
                    if "D7" in val:
                        print("D7 pressed")
                        self.client_queue.put("4")
                        self.done = False
                    if "D6" in val:
                        print("D6 pressed")
                        self.client_queue.put("3")
                        self.done = False
                    if "D5" in val:
                        print("D5 pressed")
                        self.client_queue.put("2")
                        self.done = False
                    if "D4" in val:
                        print("D4 pressed")
                        self.client_queue.put("1")
                        self.done = False

        except serial.SerialException as e:
            print(f"Serial error: {e}")
        except KeyboardInterrupt:
            print("Program interrupted")
        finally:
            self.ser.close()


    def set_done(self):
        self.done = True