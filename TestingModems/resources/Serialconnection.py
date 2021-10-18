import serial
import time

class Connect:
    def __init__(self):
        pass

    def connect(device):
        connection = serial.Serial(device.address, timeout = 12.0)
        return connection

    def listToStr(self, listStr, cmd):
        output = ""
        for stri in listStr:
            if(stri!=cmd.cmdText):
                try:
                    output += str(stri.rstrip(), encoding='utf-8')+" "
                except TypeError:
                    try:
                        output += stri.rstrip()+" "
                    except TypeError:
                        print("Incorrect data!")
                else:
                    output = output.replace('> Sample text ','')
        return ' '.join(output.split())

    def runTest(link, commands):
        results ="Test commnad; Expected result; Pass; Response\n"
        for cmd in commands:
            response = ""

            link.write(bytes(cmd.cmdText+"\r", encoding='ascii'))
            if cmd.addText == "":
                time.sleep(cmd.waitTime)
            else:
                time.sleep(2)
                link.write(bytes(cmd.addText+"\x1a\n\r", encoding='ascii'))
                link.write(bytes("\r", encoding='ascii'))
                time.sleep(cmd.waitTime)
            response = link.readlines()
            strResponse = serialLink.listToStr(response, cmd)
            if strResponse == cmd.expResponse:
                results += cmd.cmdText+";"+cmd.expResponse+";"+"Pass;"+strResponse+"\n"
            else:
                results += cmd.cmdText+";"+cmd.expResponse+";"+"Didn't pass;"+strResponse+"\n"
            if cmd.reset:
                link.write(bytes("AT&F0\r", encoding='ascii'))
                link.readlines()
        return results

    def disconnect(link):
        link.close()
        print("Testing ended")

if __name__ == __name__:
    serialLink = Connect()