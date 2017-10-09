import config
from twisted.python import log

class State(object):
    """There will be a current state for each team.  That state will
    contain information about the last X packets exchanged on that
    network according to what we care about.
    """
    def __init__(self, team_num):
        self.num_packets = 3000 # arbitrary, should be tweaked
        self.team_num = team_num
        # this is super inefficient.  But hey, it works!
        self.attackers = []
        self.fileattack = []
        self.adattack = []
        self.hmiattack = []
        self.mailattack = []
        self.webattack = []
        self.esxi = []
        self.defenders = []
        self.users = []

    def addPacket(self, packet):
        """We assume that if we got a packet here, its dest
        ip is in the team_num's ip space"""
        dest_ip = packet['ip'].dst
        last_dest = dest_ip.split(".")[3]
        last_oct = packet['ip'].src.split(".")[3]
        log.msg('lo %s' % last_oct)
        if config.is_green(last_oct):
            self.addUser()
            log.msg("USER ADDED src ip: %s dst ip: %s" % (packet['ip'].src, packet['ip'].dst))
        elif config.is_red(last_oct):
            self.addAttack()
            log.msg("ATTACKER ADDED src ip: %s dst ip: %s" % (packet['ip'].src, packet['ip'].dst))
            for description, last in config.blue.items():
                if description == "File Server" and last == last_dest:
                    self.addFileAttack()
                elif description == "Active Directory" and last == last_dest:
                    self.addADAttack()
                elif description == "HMI" and last == last_dest:
                    self.addHMIAttack()
                elif description == "Mail Server" and last == last_dest:
                    self.addMailAttack()
                elif description == "Web Server" and last == last_dest:
                    self.addWebAttack()
                elif description == "ESXi" and last == last_dest:
                    self.addEsxiAttack()
        else:
            self.addDefend()
            log.msg("DEFENDER ADDED src ip: %s dst ip: %s" % (packet['ip'].src, packet['ip'].dst))



    def addAttack(self):
        if len(self.attackers) > self.num_packets:
            self.popAll()
        self.attackers.append(True)
        self.defenders.append(False)
        self.users.append(False)


    def addFileAttack(self):
        if len(self.fileattack) > self.num_packets:
            self.popLeaves()
        self.fileattack.append(True)
        self.adattack.append(False)
        self.hmiattack.append(False)
        self.mailattack.append(False)
        self.webattack.append(False)
        self.esxi.append(False)

    def addADAttack(self):
        if len(self.fileattack) > self.num_packets:
            self.popLeaves()
        self.fileattack.append(False)
        self.adattack.append(True)
        self.hmiattack.append(False)
        self.mailattack.append(False)
        self.webattack.append(False)
        self.esxi.append(False)

    def addHMIAttack(self):
        if len(self.fileattack) > self.num_packets:
            self.popLeaves()
        self.fileattack.append(False)
        self.adattack.append(False)
        self.hmiattack.append(True)
        self.mailattack.append(False)
        self.webattack.append(False)
        self.esxi.append(False)

    def addMailAttack(self):
        if len(self.fileattack) > self.num_packets:
            self.popLeaves()
        self.fileattack.append(False)
        self.adattack.append(False)
        self.hmiattack.append(False)
        self.mailattack.append(True)
        self.webattack.append(False)
        self.esxi.append(False)

    def addWebAttack(self):
        if len(self.fileattack) > self.num_packets:
            self.popLeaves()
        self.fileattack.append(False)
        self.adattack.append(False)
        self.hmiattack.append(False)
        self.mailattack.append(False)
        self.webattack.append(True)
        self.esxi.append(False)

    def addEsxiAttack(self):
        if len(self.fileattack) > self.num_packets:
            self.popLeaves()
        self.fileattack.append(False)
        self.adattack.append(False)
        self.hmiattack.append(False)
        self.mailattack.append(False)
        self.webattack.append(False)
        self.esxi.append(True)

    def addUser(self):
        if len(self.attackers) > self.num_packets:
            self.popAll()
        self.attackers.append(False)
        self.defenders.append(False)
        self.users.append(True)

    def addDefend(self):
        if len(self.attackers) > self.num_packets:
            self.popAll()
        self.attackers.append(False)
        self.defenders.append(True)
        self.users.append(False)

    def popAll(self):
        self.attackers.pop(0)
        self.defenders.pop(0)
        self.users.pop(0)

    def popLeaves(self):
        self.fileattack.pop(0)
        self.adattack.pop(0)
        self.hmiattack.pop(0)
        self.mailattack.pop(0)
        self.webattack.pop(0)
        self.esxi.pop(0)

    def getDefenders(self):
        count = 0
        for d in self.defenders:
            if d:
                count += 1
        return count

    def getAttackers(self):
        count = 0
        for a in self.attackers:
            if a:
                count += 1
        return count

    def getUsers(self):
        count = 0
        for u in self.users:
            if u:
                count += 1
        return count

    def getFileAttack(self):
        return ("%s.%d" % (config.getPrefix(self.team_num), 30), self.getAttrCount(self.fileattack))

    def getADAttack(self):
        return ("%s.%d" % (config.getPrefix(self.team_num), 40), self.getAttrCount(self.adattack))

    def getHMIAttack(self):
        return ("%s.%d" % (config.getPrefix(self.team_num), 50), self.getAttrCount(self.hmiattack))

    def getMailAttack(self):
        return ("%s.%d" % (config.getPrefix(self.team_num), 60), self.getAttrCount(self.mailattack))

    def getWebAttack(self):
        return ("%s.%d" % (config.getPrefix(self.team_num), 70), self.getAttrCount(self.webattack))

    def getEsxiAttack(self):
        return ("%s.%d" % (config.getPrefix(self.team_num), 2), self.getAttrCount(self.esxi))

    def getAttrCount(self, attr):
        count = 0
        for i in attr:
            if i:
                count += 1
        return count

    def getCounts(self):
        return self.getAttackers(), self.getUsers(), self.getDefenders(),  \
            self.getFileAttack(), self.getADAttack(), self.getHMIAttack(), \
            self.getMailAttack(), self.getWebAttack(), self.getEsxiAttack()
