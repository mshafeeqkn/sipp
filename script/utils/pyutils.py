import logging
import paramiko


class SSHClient:
    def __init__(self, user, ip, passwd):
        self.client = paramiko.SSHClient()
        self.name = '{}@{}'.format(user, ip)
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(ip, username=user, password=passwd)
            logging.info('Connecting to {}'.format(self.name))
        except paramiko.ssh_exception.AuthenticationException:
            logging.error('Edgemarc Authentication failed')
            del self.client
            sys.exit(-1)

    def execute(self, cmd, parser):
        logging.debug('Executing: {}'.format(cmd))
        stdin, stdout, stderr = self.client.exec_command(cmd)
        data = [m for m in stdout]
        parser(data)

    def __del__(self):
        self.client.close()
        logging.info('Closing connection to {}'.format(self.name))
        del self.client


