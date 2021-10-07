import serial
from data import Commands
from data import Device
import json

def readData():
    with open("TestingModems/testdata.json", "r") as data_file:
        data = json.load(data_file)
    testDevice = Device(data["device"]["name"], data["device"]["connectionType"], data["device"]["address"], data["device"]["uName"], data["device"]["password"])
    testCommands = []
    for cmds in data["commands"]:
        temp = Commands(cmds["cmdText"], cmds["expectedResponse"], cmds["responseWaitingTime"], cmds["aditionalTextInput"])
        testCommands.append(temp)
    return testDevice, testCommands


def main():
    print("testas")
    device, commands = readData()
    print(commands[1].cmdText)
    print(device.name)


if __name__ =="__main__":
    main()