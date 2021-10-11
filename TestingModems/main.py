from serial.serialutil import Timeout
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
        temp = Commands(cmds["cmdText"], cmds["expectedResponse"], cmds["responseWaitingTime"], cmds["aditionalTextInput"], cmds["reset"])
        testCommands.append(temp)
    return testDevice, testCommands

def getSerialConnection(device):

    connection = serial.Serial(device.address, timeout = 12.0)
    print("Connected to serial")
    return connection
def listToStr(listStr):
    output = ""
    for stri in listStr:
        if(stri!=listStr[0]):
            output += str(stri.strip(), encoding='utf-8')+" "
    return ' '.join(output.split())
def testing(link, commands):
    results ="Test commnad; Expected result; Pass;\n"
    for cmd in commands:
        response = ""
        link.write(bytes(cmd.cmdText+"\r", encoding='ascii'))
        if cmd.addText == "":
            time.sleep(cmd.waitTime)
            print("no adtional text")
        else:
            print("aditional text")
            link.write(bytes(cmd.addText+"\x1a\n\r", encoding='ascii'))
            link.write(bytes("\r", encoding='ascii'))
            time.sleep(cmd.waitTime)
        #for 
        response = link.readlines()
        print(listToStr(response))
        strResponse = listToStr(response)
        print(response)
        
        if strResponse == cmd.expResponse:
            results += strResponse+";"+cmd.expResponse+";"+"Pass;\n"
        else:
            results += strResponse+";"+cmd.expResponse+";"+"Didn't pass;\n"
        if cmd.reset:
            link.write(bytes("AT&F0\r", encoding='ascii'))
            link.readlines()
    with open('results.csv', 'w') as file:
        file.write(results)

def main():
    print("testas")
    device, commands = readData()
    print(commands[0].addText)
    if device.connectionType == "serial":
        link = getSerialConnection(device)
        testing(link, commands)
    else:
        pass #prisijungimo metodas ssh
    print("Program ended testing")


if __name__ =="__main__":
    main()