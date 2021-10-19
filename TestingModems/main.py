from resources.connection import link
import argparse
import sys

def runArgs():
    my_parser = argparse.ArgumentParser(usage="-h for help")
    my_parser.add_argument('-f', action='store', type=bool, const=True, nargs='?', help='Enables result result aving in FTP server')
    my_parser.add_argument('-a', action='store', type=str, required='-f' in sys.argv, help='FTP address')
    my_parser.add_argument('-u', action='store', type=str, default="", help='FTP username')
    my_parser.add_argument('-p', action='store', type=str, default="", help='FTP password')
    my_parser.add_argument('-P', action='store', type=int, default=21, help='FTP port (default - 21)')
    my_parser.add_argument('-ip', action='store', type=str, default="", help='Test device address (overrides address in config file)')
    args = my_parser.parse_args()
   
    if(args.f is None):
        ftp = False
    else:
        ftp = True
    return ftp, args.a, args.u, args.p, args.P, args.ip

def main():
   ftp, address, username, password, port, testIP = runArgs()
   link.handle(ftp, address, username, password, port, testIP)
   
if __name__ =="__main__":
    main()