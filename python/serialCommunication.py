import serial
from os import system, name
import time

serial_port = serial.Serial(
    port='COM10',
    baudrate=9600
    )

while True:
    #userInput = input("Enter text to send: ")
    #serial_port.write((userInput + "\n").encode())
    data = serial_port.read()
    if int.from_bytes(data,byteorder='big') != 0:
        print(hex(int.from_bytes(data,byteorder='big')))


#while True:
    #userInput = input("Enter text to send: ")
    #serial_port.write(("Test/n").encode())
    # Check if incoming bytes are waiting to be read from the serial input
    # buffer.
    #if serial_port.in_waiting > 0:
        # read the bytes and convert from binary array to ASCII
    #    data_str = serial_port.readline(serial_port.in_waiting).decode('ascii')
        # print the incoming string without putting a new-line
        # ('\n') automatically after every print()
    #    print(data_str, end="")

    # Put the rest of your code you want here

    # Optional, but recommended: sleep 10 ms (0.01 sec) once per loop to let
    # other threads on your PC run during this time.
    #time.sleep(0.01)
