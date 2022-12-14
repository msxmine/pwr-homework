import random

random.seed()

class DataBus:
    def __init__(self, length):
        self.bus = [{'left': 0, 'right': 0, 'val': 3} for k in range(length)]
    def update(self):
        for i in range(0,len(self.bus),1):
            if i < len(self.bus)-1:
                self.bus[i]["left"] = self.bus[i+1]["left"]
            else:
                self.bus[i]["left"] = 0
        for i in range(len(self.bus)-1, -1, -1):
            if i > 0:
                self.bus[i]["right"] = self.bus[i-1]["right"]
            else:
                self.bus[i]["right"] = 0
            self.bus[i]["val"] = 3 - min((self.bus[i]["right"] + self.bus[i]["left"]),3)
        
    def transmit(self, pos, bit):
        self.bus[pos]["val"] = max(0, self.bus[pos]["val"]-bit)
        self.bus[pos]["left"] += bit
        self.bus[pos]["right"] += bit
    def get(self, pos):
        return self.bus[pos]["val"]
    
class Transmitter:
    def __init__(self, databus, pos, packet, prob, maxretry, cooldown):
        self.db = databus
        self.pos = pos
        self.packet = packet
        self.prob = prob
        self.maxretry = maxretry
        self.cooldown = cooldown
        self.sent = 0
        self.attempt = 0
        self.wait = 0
        self.successes = 0
        self.failures = 0
        self.retrys = 0
    def update(self):
        if self.wait > 0:
            self.wait -= 1
            return
        
        if self.attempt == 0:
            if random.random() < self.prob:
                self.attempt = 1
                self.sent = 0
                
        if self.attempt != 0:
            if self.sent == 0:
                if self.db.get(self.pos) != 3:
                    return
            self.db.transmit(self.pos, self.packet[self.sent])
            if self.db.get(self.pos) != (3-self.packet[self.sent]):
                self.sent = 0
                if self.attempt >= self.maxretry:
                    self.attempt = 0
                    self.failures += 1
                    return
                else:
                    self.attempt += 1
                    self.retrys += 1
                    self.wait = random.randint(0, self.cooldown)
                    return
            else:
                self.sent += 1
            if self.sent == len(self.packet):
                self.attempt = 0
                self.sent = 0
                self.successes += 1
                

mainbus = DataBus(100)
nodes = []
nodes.append(Transmitter(mainbus, 2, [1,2]*110, 0.005, 5, 300))
nodes.append(Transmitter(mainbus, 89, [1,2]*110, 0.005, 5, 300))

for step in range(100000):
    mainbus.update()
    for node in nodes:
        node.update()
        
totalsucc = 0
totalretry = 0
totalfail = 0

for node in nodes:
    totalsucc += node.successes
    totalretry += node.retrys
    totalfail += node.failures
    
print("SUKCESY",totalsucc, "PORA??KI", totalfail, "POWTARZANE", totalretry)
            
#Wnioski:
# Liczba w??z????w bardzo mocno wp??ywa na dzia??anie sieci
# Wi??ksze prawdopodobie??stwo zmierza do g??rnego ograniczenia,
# bo w??z??y wi??cej czasu nadaj?? ni?? czekaj?? na wylosowanie
# Liczba powt??rze?? i cooldown pomagaj?? dla niezawodno????i ale nie przepustowo????i
# Wielko???? ramki musi by?? odpowidnio du??a aby nadawca nie sko??czy?? 
# nadawa?? zanim dojdzie do niego kolizja (2xczas propagacji)
# W zwi??zku z tym po??o??enie nadajnik??w nie ma wi??kszego znaczenia
# Jednynie je??li s?? blisko to wi??ksza szansa na czekanie zamiast kolizji


            
