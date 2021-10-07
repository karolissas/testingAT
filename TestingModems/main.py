from data import Commands
from data import Device
import time
import json
import serial

def readData():
    with open("TestingModems/testdata.json", "r") as data_file:
        data = json.load(data_file)
    testDevice = Device(data["device"]["name"], data["device"]["connectionType"], data["device"]["address"], data["device"]["uName"], data["device"]["password"])
    testCommands = []
    for cmds in data["commands"]:
        temp = Commands(cmds["cmdText"], cmds["expectedResponse"], cmds["responseWaitingTime"], cmds["aditionalTextInput"])
        testCommands.append(temp)
    return testDevice, testCommands

def getSerialConnection(device):

    connection = serial.Serial(device.address)
    print("Connected to serial")
    return connection

def testing(link, commands):
    for cmd in commands:
        response = ""
        link.write(bytes(cmd.cmdText+"\n\r", encoding='ascii'))
       # print(bytes(cmd.cmdText+"\n\r", encoding='utf-8'))
        if cmd.addText == None:
            time.sleep(cmd.waitTime)
        else:
            link.write(bytes(cmd.addText+"\x1a\n", encoding='ascii'))
            time.sleep(cmd.waitTime)
        #for 
       # response += str(link.readline())
       # skaityti po viena baita ir tikrinti ar ne new line
       #kad greiciau veiktu 
        print(response)


def main():
    print("testas")
    device, commands = readData()
    if device.connectionType == "serial":
        link = getSerialConnection(device)
        testing(link, commands)
    else:
        pass #prisijungimo metodas ssh
    print("Program ended testing")


if __name__ =="__main__":
    main()