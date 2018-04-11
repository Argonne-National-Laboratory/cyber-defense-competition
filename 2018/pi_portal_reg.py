#!/usr/bin/python

import subprocess as sub
import re
from threading import Thread
import argparse
import time
import requests

class ThreadedRegisterMac(Thread):
    def __init__(self, mac, iface):
        Thread.__init__(self)
        self.mac = mac
        self.iface = iface

    def run(self):
        sub.check_call(['sudo', 'ifconfig', self.iface, 'down'])
        sub.check_call(['sudo', 'macchanger', '-m', self.mac, self.iface])
        time.sleep(2)
        sub.check_call(['sudo', 'ifconfig', self.iface, 'up'])
        sub.check_call(['sudo', 'dhclient', self.iface])
        # insert POST to captive portal here
        action_url = "http://146.137.2.106/cgi-bin/register-new.cgi"
        data = {"first": "Nataniel",
                "last": "Evans",
                "email": "nevans@anl.gov",
                "building": "240",
                "phone" : "6302523733",
                "length":"week",
                "":"submit"}
        r = requests.post(action_url, data=data)
        sub.Popen(['echo', r.text])


def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

if __name__ == '__main__':
    aparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    aparser.add_argument('-l', '--listen-iface', action='store', default=None, dest='listen_iface')
    aparser.add_argument('-t', '--talk-iface', action='store', default=None, dest='talk_iface')
    args = aparser.parse_args()
    macs = set()
    p = sub.Popen(('sudo', 'tcpdump', '-i', args.listen_iface, '-l', '-s 0', '-vvv', '-n', '((udp port 67) and (udp[8:1] = 0x1))'), stdout=sub.PIPE)
    while True:
        for row in iter(p.stdout.readline, b''):
            if findWholeWord('requested-ip')(row):
                mac = row.split(' ')[-1].strip()
                if ":" in mac and len(mac) == 17 and mac not in macs:
                    macs.add(mac)
                    t = ThreadedRegisterMac(mac, args.talk_iface)
                    print "registering %s to the guest network" % mac
                    t.start()
            elif findWholeWord('client-id')(row):
                mac = row.split(' ')[-1].strip()
                if ":" in mac and len(mac) == 17 and mac not in macs:
                    macs.add(mac)
                    t = ThreadedRegisterMac(mac, args.talk_iface)
                    print "registering %s to the guest network" % mac
                    t.start()
