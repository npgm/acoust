from acoust import Packet
p = Packet('00', '01', 'ABCDEFGH')
print p.payload
pEnc = p.encode()
print pEnc
print len(pEnc)
pChk = Packet.decode(pEnc)
print pChk.encode()

