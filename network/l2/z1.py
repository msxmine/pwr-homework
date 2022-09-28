plik = open("./Z", "rt")
cont = plik.read().strip()
plik.close()

def crc(bitstring):
    crc32_poly = "100000100110000010001110110110111"
    calc_str = ""
    for offset in range(0,len(bitstring),8):
        byte = bitstring[offset:offset+8]
        byte = byte.ljust(8, '0')
        calc_str = calc_str + byte[::-1]
    calc_str = format(int(calc_str[0:32],2)^0xffffffff, '032b') + calc_str[32:]
    calc_str = calc_str + ("0"*32)
    for offset in range(len(bitstring)):
        if calc_str[offset] == '1':
            calc_str = calc_str[0:offset] + format((int(calc_str[offset:(offset+33)],2) ^ int(crc32_poly,2)), '033b') + calc_str[(offset+33):]
    return format(int(calc_str[-32:],2)^0xffffffff, '032b')[::-1]


def hdlc_bitstuff(bitstring):
    onescnt = 0
    result = ""
    for bit in bitstring:
        result = result + bit
        if bit == "1":
            onescnt += 1
        else:
            onescnt = 0
        
        if onescnt == 5:
            onescnt = 0
            result = result + "0"
    return result
            
def frame(bitstring):
    result = ""
    result = result + "01111110"
    result = result + hdlc_bitstuff(bitstring + crc(bitstring))
    result = result + "01111110"
    return result

with open("./W", "wt") as plik:
    plik.write(frame(cont))




