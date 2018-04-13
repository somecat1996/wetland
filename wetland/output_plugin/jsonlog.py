import json
import time
import pytz
import datetime
import socket
from wetland import config


class plugin(object):
    def __init__(self, server):
        self.server = server
        self.methods = list(set(['file', 'tcp', 'udp']) &
                            set(config.cfg.options('jsonlog')))

        if 'tcp' in self.methods:
            ip, port = config.cfg.get('jsonlog', 'tcp').split(':')
            port = int(port)
            self.tcpsock = (ip, port)
        if 'udp' in self.methods:
            ip, port = config.cfg.get('jsonlog', 'udp').split(':')
            port = int(port)
            self.udpsock = (ip, port)
        if 'file' in self.methods:
            self.logfile = config.cfg.get('jsonlog', 'file')

    def file(self, data):
        with open(self.logfile, 'a') as logfile:
            logfile.write(data+'\n')

    def udp(self, data):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(self.udpsock)
        s.send(data)
        s.close()

    def tcp(self, data):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.tcpsock)
        s.send(data)
        s.close()

    def send(self, subject, action, content):
        t = datetime.datetime.fromtimestamp(time.time(),
                                            tz=pytz.timezone('UTC')).isoformat()

        if subject == 'wetland':
            data = {'timestamp': t, 'src': self.server.hacker_ip,
                    'dst': self.server.myip, 'type': action,
                    'content': content}
            data = json.dumps(data)
            for m in self.methods:
                getattr(self, m)(data)

        elif subject == 'content':
            pass

        elif subject in ['sftpfile', 'sftpserver']:
            pass
