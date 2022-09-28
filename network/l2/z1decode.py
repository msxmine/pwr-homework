plik = open("./W", "rt")
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


def hdlc_deframe(bitstring):
    cur_frame = ""
    onescnt = 0
    inframe = 0
    result = []
    offset = 0
    while offset < len(bitstring):
        if inframe == 0:
            if bitstring[offset-7:offset+1] == "01111110":
                inframe = 1
            offset += 1
            continue
        
        if onescnt == 5:
            if bitstring[offset] == "1":
                offset += 1
                inframe = 0
                if bitstring[offset] == "1":
                    offset += 1
                    continue
                else:
                    offset += 1
                    result.append(cur_frame[:-6])
                    continue
            else:
                offset += 1
                onescnt = 0
        cur_frame = cur_frame + bitstring[offset]
        if bitstring[offset] == "1":
            onescnt += 1
        else:
            onescnt = 0
        offset += 1
    return result
            
            
cont_verified = ""
for frame in hdlc_deframe(cont):
    if frame[-32:] == crc(frame[0:-32]):
        cont_verified = cont_verified + frame[0:-32]

with open("./R", "wt") as plik:
    plik.write(cont_verified)
    plik.write('\n')




