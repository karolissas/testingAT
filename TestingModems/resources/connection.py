import json
import ftplib
import os
from resources.data import Commands
from resources.device import Device

class Connection:
    def __init__(self):
        pass

    def loadModule(self, moduleName):
        module = None
        try:
            module = __import__('resources.{type}connection'.format(type=moduleName), fromlist=['resources'])
            return module
        except Exception as e:
            print(e)
            return False
    
    def callConnection(self, module, deviceData):
        try:
            method = getattr(module, "Connect")
            if not callable(method):
                return False
            return method
        except Exception as e:
            print("call method")
            print(e)
            return False

    def writeResults(self, data, ftp, address, username, password, port):
        with open('naujas.csv', 'w') as ope:
            ope.write(data)
        ope.close()
        if ftp:
            filename = "naujas.csv"
            ftpConnect = ftplib.FTP(address, username, password)
            with open('naujas.csv', 'rb') as upload:
                ftpConnect.storbinary(f"STOR {filename}",upload)
                ftpConnect.quit()
            os.remove('naujas.csv')


    def startTesting(self, module, link, commands, ftp, address, username, password, port):
        data = module.runTest(link,commands)
        self.writeResults(data, ftp, address, username, password, port)

    def connect(self, link, device):
        data = link.connect(device)
        return data

    def disconnect(self, module, link):
        module.disconnect(link)
    
    def readData(self):
        with open("TestingModems/testdata.json", "r") as data_file:
            data = json.load(data_file)
        testDevice = Device(data["device"]["name"], data["device"]["connectionType"], data["device"]["address"], data["device"]["uName"], data["device"]["password"])
        testCommands = []
        for cmds in data["commands"]:
            temp = Commands(cmds["cmdText"], cmds["expectedResponse"], cmds["responseWaitingTime"], cmds["aditionalTextInput"], cmds["reset"])
            testCommands.append(temp)
        return testDevice, testCommands

    def handle(self, ftp, address, username, password, port, testIP):
        deviceData, commands = self.readData()
        type = deviceData.connectionType
        module = self.loadModule(type)
        if testIP != "":
            deviceData.address = testIP
        connectionLink = self.callConnection(module,deviceData)
        link = self.connect(connectionLink, deviceData)
        self.startTesting(connectionLink, link, commands, ftp, address, username, password, port)
        self.disconnect(connectionLink, link)
        
if __name__ == __name__:
    link = Connection()
