    # JazzHands | JazzHandsController
# Written by Amber Swarbrick 06/01/2024
# Code Review Passed by Toby Clark 06/01/2024

from gamemaker_handler import GMS2Client
from pi_handler import PiClient
from queue import Queue

class JazzhandsController():
    running: bool                                   # A flag to determine if the program has ended. Facilitates safe termination of threads.
    gamemaker_client: GMS2Client 
    pi_client: PiClient
    gamemaker_queue: Queue                             # An instance of the client queue. Facilitates sending gesture data to the client object.
    gesture_queue: Queue                          # An instance of the gesture_recognition queue. Allows transmission of gesture data to the client.

    def __init__(self) -> None:
        """
        Main function which initiates the client and gesture recognition.
        """

        self.create_client()
        self.create_pi_client()

        # Boolean flag to continuously run the controller until a stopping condition is met.
        self.running = True
        
    def create_client(self) -> None:
        """
        Creates a thread which initialises the client.
        """

        self.gamemaker_client = GMS2Client()
        self.gamemaker_queue: Queue = self.gamemaker_client.client_queue
        self.gamemaker_client.start_thread()


    def create_pi_client(self) -> None:
        """
        Creates a thread which initialises the pi client.
        """
        self.pi_client = PiClient()
        self.pi_queue: Queue = self.pi_client.client_queue
        self.pi_client.start_thread()

    def mainloop(self) -> None:
        """
        Program Main Loop. Retrieves gesture detections and sends them to GameMaker server.
        """
        while self.running:
            self.update_client()
        print("stopped running")

    def update_client(self) -> None:
        """
        Attempt to update the client. Handle keyboard interrupt exceptions.
        """
        try:
            self.try_transmit_to_client()

        # The program will safely end upon a keyboard interrupt (Ctrl+C).
        except KeyboardInterrupt:
            self.terminate_program()
        except Exception as e:
            raise e
    
    def terminate_program(self) -> None:
        """
        Safely end all threads and terminate the main process.
        """
        print("CTRL+C has been pressed. Ending threads.")
        self.pi_client.stop_thread()
        self.gamemaker_client.stop_thread()
        self.running = False
        exit(0)

    def try_transmit_to_client(self) -> bool:
        """
        Attempt to send the most recent gesture from gesture_queue to the GMS2 server.
        """
        if not self.gesture_queue.empty():
            gestures: str = self.gesture_queue.get()
            self.gamemaker_queue.put(gestures)
            return True
        else:
            return False


if __name__ == "__main__":
    JazzhandsController()