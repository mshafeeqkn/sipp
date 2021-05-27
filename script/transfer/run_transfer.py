import sys
import os
import argparse
import logging

from script.utils.pyutils import SSHClient

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("paramiko").setLevel(logging.WARNING)

def my_parser(data):
    dev_conf = {}

    for line in data:
        line_parts = line.split()
        user = None

        for part in line_parts:
            if part.startswith('n='):
                user = part.split('=')[-1]

        dev_conf[user] = {}
        dev_conf[user]['ip'] = line_parts[2]
        dev_conf[user]['port'] = line_parts[3]

    logging.debug('parsed output: {}'.format(dev_conf))


if __name__ == '__main__':
    initiator = '6001'
    transferee = '6002'
    target = '6003'
    
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
        logging.error('No Edgemarc specified. Set DEV_IP and DEV_PASS first')
        sys.exit(-1)

    em = SSHClient(user='root', ip=dev_ip, passwd=dev_pass)
    em.execute('cat /etc/config/sipdptargets', my_parser)
    del em
