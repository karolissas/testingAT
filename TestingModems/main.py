from data import Commands
from data import Device
import paramiko
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
    return connection

def getSSHConnection(device):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys(r'C:\Users\PC/.ssh/known_hosts')
    ssh.connect(device.address, port=22, username=device.uName, password=device.password)
    return ssh

def listToStr(listStr, cmd):
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
            #print("string to list "+output)
                output = output.replace('> Sample text ','')
    return ' '.join(output.split())

def testing(link, commands):
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
        strResponse = listToStr(response, cmd)
        if strResponse == cmd.expResponse:
            results += cmd.cmdText+";"+cmd.expResponse+";"+"Pass;"+strResponse+"\n"
        else:
            results += cmd.cmdText+";"+cmd.expResponse+";"+"Didn't pass;"+strResponse+"\n"
        if cmd.reset:
            link.write(bytes("AT&F0\r", encoding='ascii'))
            link.readlines()
    with open('results.csv', 'w') as file:
        file.write(results)

def testSSH(link, commands):
    data ="Test commnad; Expected result; Pass; Response\n"
    #link.send("clear\r")
    time.sleep(1)
    for cmd in commands:
        response = ""

        # link.send("gsmctl -A "+cmd.cmdText+"\r")
        # time.sleep(1)
        # link.settimeout(7.0)
        # response = link.recv(4096)
        
        
        if cmd.addText == "":
            stdin, stdout, stderr = link.exec_command("gsmctl -A "+cmd.cmdText+"\r")
            da = stdout.readlines()
            response = listToStr(da, cmd)
            time.sleep(cmd.waitTime)
        else:
            time.sleep(2)
            stdin, stdout, stderr = link.exec_command(cmd.addText+"\x1a\n\r")
            time.sleep(cmd.waitTime)
            da = stdout.readlines()
    #     # output = response.replace(b'root@Teltonika-RUTX11:~# ',b'').replace(b'gsmctl -A ',b'')
    #     # output = output.split(b'\n')
    #     # temp = b""
    #     # i = 0
    #     # for te in output:
    #     #     if i>12:
    #     #         temp += te.rstrip()+b"\n"
    #     #     i+=1
    #     strResponse = ""#listToStr()
    #     print(strResponse)
        if response == cmd.expResponse:
            data += cmd.cmdText+";"+cmd.expResponse+";"+"Pass;"+response+"\n"
        else:
            data += cmd.cmdText+";"+cmd.expResponse+";"+"Didn't pass;"+response+"\n"
        #if cmd.reset:
           # link.send("gsmctl -A "+"AT&F0\r", encoding='ascii')
            #link.readlines()
    #     #link.send('clear\r')
    with open('naujas.csv', 'w') as ope:
       ope.write(data)

def main():
    device, commands = readData()
    if device.connectionType == "serial":
        try:
            link = getSerialConnection(device)
        except serial.SerialException as e:
            print("Unable connect to serial: " + str(e))
        else:
            testing(link, commands)
    else:
        try:
            link = getSSHConnection(device)
        except (paramiko.ssh_exception.AuthenticationException, paramiko.ssh_exception.NoValidConnectionsError, paramiko.ssh_exception.CouldNotCanonicalize)as e:
            print("Error while connecting to SSH: " + str(e))
        else:
            shell = link.invoke_shell()
            
            testSSH(link, commands)
            # output = ""
            # stdin, stdout, stderr = link.exec_command("gsmctl -A ATE1\r")
            # da = stdout.readlines()
            # print(da)
            # stdin, stdout, stderr = link.exec_command("gsmctl -A AT+CMGF=1\r")
            # da = stdout.readlines()
            # stdin, stdout, stderr = link.exec_command("gsmctl -A AT+CMGS=\"+37062892859\"\r")
            # da = stdout.readlines()
            # print(da)

    print("Program ended testing")
    link.close()


if __name__ =="__main__":
    main()