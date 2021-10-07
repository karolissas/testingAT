class Commands:
    def __init__(self, cmdText, expResponse, waitTime, addText):
        self.cmdText = cmdText
        self.expResponse = expResponse
        self.waitTime = waitTime
        self.addText = addText


class Device:
    def __init__(self, name, connectioType, address, uName, password):
        self.name = name
        self.connectionType = connectioType
        self.address = address
        self.uName = uName
        self.password = password
        
    