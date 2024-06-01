import serial
from time import sleep
import sys

COM = 'COM4'
BAUD = 9600


class Button():

    def __init__(self):

        try:
            self.ser = serial.Serial(COM, BAUD, timeout=1)
        except serial.SerialException as e:
            print(f"Error: {e}")
            sys.exit(1)

        print('Waiting for device')
        sleep(1)
        print(f"Connected to: {self.ser.name}")

        self.mainloop()


    def mainloop(self):
        # Check args
        try:
            while True:
                val = self.ser.readline().decode().strip()
                if val:

                    if "D10" in val:
                        print("D10 pressed")
                    if "D7" in val:
                        print("D7 pressed")
                    if "D6" in val:
                        print("D6 pressed")
                    if "D5" in val:
                        print("D5 pressed")
                    if "D4" in val:
                        print("D4 pressed")

        except serial.SerialException as e:
            print(f"Serial error: {e}")
        except KeyboardInterrupt:
            print("Program interrupted")
        finally:
            self.ser.close()
