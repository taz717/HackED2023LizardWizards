import time
import serial
# TODO move to main.py
arduinoData = serial.Serial('com6', 115200)
time.sleep(1)
i = 0

# Infinite loop to watch for serial comms from Arduino
# TODO move loop to main.py
while True:
    # If the arduino has bytes waiting to be read, read them
    if arduinoData.inWaiting() != 0:
        dataPacket = arduinoData.readline()
        dataPacket = str(dataPacket, 'utf-8')
        dataPacket = dataPacket.strip('\r\n')
        # Print arduino output into terminal
        print(dataPacket)
        time.sleep(0.1)
    else:
        # Accept user input
        # TODO change this to output of AI
        cmd = input('Enter command: ')
        # Write command to serial
        arduinoData.write(str.encode(cmd+'\r\n'))
        time.sleep(0.5)
