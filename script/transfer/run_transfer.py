import paramiko
import time
import os
import sys
import argparse


initiator = '6001'
transferee = '6002'
target = '6003'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--addr", required=False, help="IP address of Edgemarc")
parser.add_argument("-p", "--pass", required=False, help="Password of Edgemarc")
args = vars(parser.parse_args())

dev_ip = args['addr']
dev_pass = args['pass']

if not dev_ip and not dev_pass:
    dev_ip = os.environ.get('DEV_IP', None)
    dev_pass = os.environ.get('DEV_PASS', None)

if not dev_ip or not dev_pass:
    print('No Edgemarc specified. Set DEV_IP and DEV_PASS first')
    sys.exit(-1)

try:
    client.connect(dev_ip, username='root', password=dev_pass)
except paramiko.ssh_exception.AuthenticationException:
    print('Edgemarc Authentication failed')
    sys.exit(-1)

stdin, stdout, stderr = client.exec_command('cat /etc/config/sipdptargets')
time.sleep(1)

dev_conf = {}

for line in stdout:
    line_parts = line.split()
    user = None

    for part in line_parts:
        if part.startswith('n='):
            user = part.split('=')[-1]

    dev_conf[user] = {}
    dev_conf[user]['ip'] = line_parts[2]
    dev_conf[user]['port'] = line_parts[3]

client.close()
print(dev_conf)
