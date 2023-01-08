import time
import serial
# TODO move to main.py


# Infinite loop to watch for serial comms from Arduino
# TODO move loop to main.py
class ArduinoIO:
    def __init__(self) -> None:
        self.arduinoData = serial.Serial('com6', 115200)

    def readData(self):
        while arduinoData.inWaiting() == 0:
            pass #block until there is something to read

        dataPacket = arduinoData.readline()
        dataPacket = str(dataPacket, 'utf-8')
        dataPacket = dataPacket.strip('\r\n')
        # Print arduino output into terminal
        return (dataPacket)
    
    def writeData(str):
        arduinoData.write(str.encode(cmd+'\r\n'))

if __name__ == "__main__":
    arduinoData = serial.Serial('com6', 115200)
    time.sleep(1)
    i = 0
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
