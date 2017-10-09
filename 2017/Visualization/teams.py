import state
from twisted.python import log

class Team(object):
    def __init__(self, num, network, name):
        self.num = num
        self.network = network
        self.name = name # this will be the school for us
        self.state = state.State(self.num)

    def contains(self, ip):
        netocts = self.network.split(".")
        ipocts = ip.split(".")
        if (netocts[0] == ipocts[0] and netocts[2] == ipocts[2] and netocts[1] == ipocts[1]):
            log.msg("Team %s packet received" % self.num)
            return True
        else:
            return False

    #self.seen_ips = []

class Teams(object):
    def __init__(self):
        self.teams = []

    def addTeam(self, team):
        self.teams.append(team)

    def getTeam(self, num):
        return self.teams[num-1]

    def slotPacket(self, packet):
        for team in self.teams:
            #log.msg("type: %s contains: %s" % (type(packet["ip"].dst), packet["ip"].dst))
            if (team.contains(packet["ip"].dst)):
                team.state.addPacket(packet)
                #return True

    def dump(self):
        l = []
        for team in self.teams:
            attacker, user, defender, fileattack, adattack, \
            hmiattack, mailattack, webattack, esxi = team.state.getCounts()
            l.append({
              "num" : team.num,
              "name": team.name,
              "network": team.network,
              "attacker": attacker,
              "user":user,
              "defender": defender,
              fileattack[0] : fileattack[1],
              adattack[0] : adattack[1],
              hmiattack[0] : hmiattack[1],
              mailattack[0]: mailattack[1],
              webattack[0] : webattack[1],
              esxi[0]: esxi[1]
            })
        return l
