import paramiko
import time

class Connect:
    def __init__(self):
        pass

    def connect(device):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys(r'C:\Users\PC/.ssh/known_hosts')
        ssh.connect(device.address, port=22, username=device.uName, password=device.password)
        return ssh

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
        data ="Test commnad; Expected result; Pass; Response\n"
        time.sleep(1)
        for cmd in commands:
            response = ""
            if cmd.addText == "":
                stdin, stdout, stderr = link.exec_command("gsmctl -A "+cmd.cmdText+"\r")
                da = stdout.readlines()
                response = sshLink.listToStr(da, cmd)
                time.sleep(cmd.waitTime)
            else:
                time.sleep(2)
                stdin, stdout, stderr = link.exec_command(cmd.addText+"\x1a\n\r")
                time.sleep(cmd.waitTime)
                da = stdout.readlines()
            if response == cmd.expResponse:
                data += cmd.cmdText+";"+cmd.expResponse+";"+"Pass;"+response+"\n"
            else:
                data += cmd.cmdText+";"+cmd.expResponse+";"+"Didn't pass;"+response+"\n"
        return data
    def disconnect(self):
        self.close()
        print("Testing ended")

if __name__ == __name__:
    sshLink = Connect()