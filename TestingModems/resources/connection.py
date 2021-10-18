import json
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

    def writeResults(self, data):
        with open('naujas.csv', 'w') as ope:
            ope.write(data)

    def startTesting(self, module, link, commands):
        data = module.runTest(link,commands)
        self.writeResults(data)

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

    def handle(self):
        deviceData, commands = self.readData()
        type = deviceData.connectionType
        module = self.loadModule(type)
        connectionLink = self.callConnection(module,deviceData)
        link = self.connect(connectionLink, deviceData)
        self.startTesting(connectionLink, link, commands)
        self.disconnect(connectionLink, link)
        
if __name__ == __name__:
    link = Connection()
