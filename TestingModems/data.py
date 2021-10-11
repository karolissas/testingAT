class Commands:
    def __init__(self, cmdText, expResponse, waitTime, addText, reset):
        self.cmdText = cmdText
        self.expResponse = expResponse
        self.waitTime = waitTime/1000
        self.addText = addText
        self.reset = reset


class Device:
    def __init__(self, name, connectioType, address, uName, password):
        self.name = name
        self.connectionType = connectioType
        self.address = address
        self.uName = uName
        self.password = password
        
    