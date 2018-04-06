#!/usr/bin/python

import subprocess as sub
import re
from threading import Thread
import argparse

class ThreadedRegisterMac(Thread):
    def __init__(self, mac, iface):
        Thread.__init__(self)
        self.mac = mac
        self.iface = iface

    def run(self):
        sub.check_call(['sudo', 'macchanger', '-m', self.mac, self.iface])
        sub.check_call(['sudo', 'dhclient', self.iface])
        # insert POST to captive portal here

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

if __name__ == '__main__':
    aparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    aparser.add_argument('-l', '--listen-iface', action='store', default=None, dest='listen_iface')
    aparser.add_argument('-t', '--talk-iface', action='store', default=None, dest='talk_iface')
    args = aparser.parse_args()
    macs = set()
    p = sub.Popen(('sudo', 'tcpdump', '-i', args.listen_iface, '-l', '-s 0', '-vvv', '-n', '((udp port 67) and (udp[8:1] = 0x1))'), stdout=sub.PIPE)
    for row in iter(p.stdout.readline, b''):
        if findWholeWord('requested-ip')(row):
            mac = row.split(' ')[-1]
            if mac not in macs:
                macs.add(mac)
                ThreadedRegisterMac(mac, args.talk_iface)
        elif findWholeWord('client-id')(row):
            mac = row.split(' ')[-1]
            if mac not in macs:
                macs.add(mac)
                ThreadedRegisterMac(mac, args.talk_iface)
