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

    return dev_conf

def get_ip_pass(data):
    if not len(data):
        return None, None

    parts = data[0].split()
    return parts[0], parts[1]


if __name__ == '__main__':
    initiator = '6001'
    xferee = '6002'
    target = '6003'

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--addr", required=False, help="IP address of Edgemarc")
    parser.add_argument("-p", "--pass", required=False, help="Password of Edgemarc")
    parser.add_argument("-n", "--num", required=False, help="Edgemarc Number")
    args = vars(parser.parse_args())

    dev_ip = args['addr']
    dev_pass = args['pass']

    if not dev_ip and not dev_pass:
        dev_ip = os.environ.get('DEV_IP', None)
        dev_pass = os.environ.get('DEV_PASS', None)

    dev_pc = SSHClient(user='shafeeque', ip='1.1.1.104', passwd='123')
    dev_ip, dev_pass = dev_pc.execute('cat .devpass | grep {}'.format(args['num']), get_ip_pass)

    if not dev_ip or not dev_pass:
        logging.error('No Edgemarc specified. Set DEV_IP and DEV_PASS first')
        del dev_pc
        sys.exit(-1)

    em = SSHClient(user='root', ip=dev_ip, passwd=dev_pass)
    dev_conf = em.execute('cat /etc/config/sipdptargets', my_parser)
    sipp_cmd = 'sipp -i {ip} -p {port} -sf {sf} -inf users.csv {dev_ip}:5060 -m 1'
    init_sipp = sipp_cmd.format(ip=dev_conf[initiator]['ip'],
            port=dev_conf[initiator]['port'], sf='initiator.xml', dev_ip=dev_ip)
    xferee_sipp = sipp_cmd.format(ip=dev_conf[xferee]['ip'],
            port=dev_conf[xferee]['port'], sf='xferee.xml', dev_ip=dev_ip)
    target_sipp = sipp_cmd.format(ip=dev_conf[target]['ip'],
            port=dev_conf[target]['port'], sf='target.xml', dev_ip=dev_ip)
    logging.info("Initiator command: {}".format(init_sipp))
    logging.info("Transferee command: {}".format(xferee_sipp))
    logging.info("Target command: {}".format(target_sipp))

    del em
    del dev_pc
