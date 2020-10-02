import paramiko
from .info import *
import re


class ansible_cluster:
    def __init__(self, privateKey_path:str, command:str):
        self.command = command
        self.private_key = paramiko.RSAKey.from_private_key_file(privateKey_path)
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname, port=port, username=user, pkey = self.private_key)

    def __enter__(self):
        pass

    def start_command(self):
        result_str = ""
        stdin , stdout, stderr = self.ssh_client.exec_command(self.command)
        for str in stdout.readlines():
            if str.find("ok=") >= 0:
                if str.find("unreachable=0    failed=0") < 0:
                    str = '>:( ' + str
                result_str += str
        return result_str
            
    def __exit__(self):
        self.ssh_client.close()

