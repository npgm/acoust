from uuid import getnode as get_mac
import base64
import hashlib

class Packet:
  packetSize = 32
  payloadSize = 22

  @staticmethod
  def generatehash(source, dest, size, payload): 
    md5bytes=hashlib.md5(self.source + self.dest + chr(self.size) + self.payload).digest()
    return base64.urlsafe_b64encode(md5bytes)[:5]

  @staticmethod
  def decode(packet):
    if len(packet) != Packet.packetSize:
      return None
    source = packet[:2]
    dest = packet[2:4]
    hashid = packet[4:9]
    size = ord(packet[9:10])
    if size > 22:
      return None
    payload = packet[10:10+size]

    if hashid != Packet.generatehash(source, dest, size, payload):
      return None
    return Packet(source, dest, payload)

  def __init__(self, source, destination, payload):
    self.source = source
    self.dest = destination
    self.payload = payload
    self.sethash()
  
  @property 
  def hashid(self):
    return self._hash
  def sethash(self):
    self._hash = Packet.generatehash(self.source, self.dest, self.size, self.payload)

  @property
  def size(self):
    return self._size 

  @property 
  def source(self):
    return self._address 
  @source.setter
  def source(self, s):
    self._source = a
    self.sethash()

  @property 
  def destination(self):
    return self.dest 
  @destination.setter
  def destination(self, d):
    self.dest = d
    self.sethash()

  @property 
  def payload(self):
    return self._payload
  @payload.setter
  def payload(self, p):
    self._size = min(len(p), 22)
    self._payload = p.ljust(22, '0')
    self.sethash()

  def __unicode__(self):
    print self.source + ' ' + self.dest + ' ' + self.payload + ' ' + self.hashid
p = Packet('00', '01', 'ABCDEFGH')
print p

