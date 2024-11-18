import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

NI_1 = os.getenv('NI1')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=NI_1,username=USERNAME,password=PASSWORD)

stdin,stdout,stderr=ssh_client.exec_command('sudo -S energibridge sleep 3')
stdin.write(f'{PASSWORD}\n')

print(stdout.readlines())
print(stderr.readlines())

