class Commands:
    def __init__(self, cmdText, expResponse, waitTime, addText, reset):
        self.cmdText = cmdText
        self.expResponse = expResponse
        self.waitTime = waitTime/1000
        self.addText = addText
        self.reset = reset 
