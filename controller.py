    # JazzHands | JazzHandsController
# Written by Amber Swarbrick 06/01/2024
# Code Review Passed by Toby Clark 06/01/2024

from gamemaker_handler import GMS2Client
from pi_handler import PiClient
from queue import Queue

import cv2
from enum import Enum
import numpy as np


class Color(Enum):
    RED1LOWER = (0, 70, 50)
    RED1HIGHER = (10, 255, 255)

    RED2LOWER = (170, 70, 50)
    RED2HIGHER = (180, 255, 255)

    GREENLOWER = (30, 40, 15)
    GREENHIGHER = (90, 255, 255)

    BLUELOWER = (110,50,20)
    BLUEHIGHER = (130,255,255)

    BLACKLOWER = (0,0,0)
    BLACKHIGHER = (40,255,50)   

class JazzhandsController():
    running: bool                                   # A flag to determine if the program has ended. Facilitates safe termination of threads.
    gamemaker_client: GMS2Client 
    pi_client: PiClient
    gamemaker_queue: Queue                             # An instance of the client queue. Facilitates sending gesture data to the client object.
    pi_queue: Queue                          # An instance of the gesture_recognition queue. Allows transmission of gesture data to the client.
    

    

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

        test = False

        if test:
            image = cv2.imread("testimg.jpg")
            image = cv2.resize(image, (0, 0), fx = 0.5, fy = 0.5)
            self.process_image(image)
            return
        

        if not self.pi_queue.empty():
            image = self.pi_queue.get()
            image = image[100:600, 200:1000]
            cv2.imshow("",image)
            cv2.waitKey(1)

            self.process_image(image)

            return True
        else:
            return False

    def process_image(self, image):

        hsv_img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        red_low = cv2.inRange(hsv_img, Color.RED1LOWER.value, Color.RED1HIGHER.value)
        red_high = cv2.inRange(hsv_img, Color.RED2LOWER.value, Color.RED2HIGHER.value)
        red = red_low | red_high
        green = cv2.inRange(hsv_img, Color.GREENLOWER.value, Color.GREENHIGHER.value)
        blue = cv2.inRange(hsv_img, Color.BLUELOWER.value, Color.BLUEHIGHER.value)
        black = cv2.inRange(hsv_img, Color.BLACKLOWER.value, Color.BLACKHIGHER.value)

        ordered_contours = self.process_images(red, green, black, blue)
        self.gamemaker_client.send_response(ordered_contours)
        self.gamemaker_queue.put(ordered_contours)


    def find_contours(self, image, color):

        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        # Create a mask to erase small contours and contours with small aspect ratio
        mask = np.ones_like(image) * 255  # White mask

        # Erase small contours and contours with small aspect ratio
        for c in contours:
            area = cv2.contourArea(c)

            # Fill very small contours with zero (erase small contours)
            if area < 5:
                cv2.drawContours(mask, [c], -1, 0, thickness=cv2.FILLED)  # Draw black (0) to erase
                

        # Apply the mask to the original image to remove unwanted contours
        result = cv2.bitwise_and(image, image, mask=mask)


        # Find contours again in the processed image
        new_contours, _ = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #cv2.imshow(color, image)
        #cv2.waitKey(1)


        return [(c, color) for c in new_contours]



    def get_leftmost_point(self, contour):
        return tuple(contour[contour[:, :, 0].argmin()][0])

    def order_contours_by_position(self, contours):
        contours_with_positions = [(contour, color, self.get_leftmost_point(contour)) for contour, color in contours]
        contours_with_positions.sort(key=lambda x: x[2][0])  # Sort by the x-coordinate of the leftmost point

        ret = [color for contour, color, _ in contours_with_positions]
        return ret

    def process_images(self, red_mask, green_mask, black_mask, blue_mask):
        # Get contours from each mask with their corresponding color
        red_contours = self.find_contours(red_mask, 'red')
        green_contours = self.find_contours(green_mask, 'green')
        black_contours = self.find_contours(black_mask, 'black')
        blue_contours = self.find_contours(blue_mask, 'blue')

        # Combine all contours into one list
        all_contours = red_contours + green_contours + black_contours + blue_contours

        # Order contours from left to right
        ordered_contours = self.order_contours_by_position(all_contours)

        return ordered_contours



if __name__ == "__main__":
    c = JazzhandsController()
    c.mainloop()