#!/usr/bin/python

import threading
import os, sys
import acoust_out
import acoust_in
import select
from uuid import getnode as get_mac
import base64
import hashlib
import AcoustAppData_pb2 as apd
from datetime import datetime

class Packet(object):
  packetSize = 32
  payloadSize = 22

  @staticmethod
  def generatehash(source, dest, size, payload): 
    md5bytes=hashlib.md5(source + dest + str(unichr(size)) + payload + datetime.now()).digest()
    return base64.urlsafe_b64encode(md5bytes)[:5]
  def encode(self):
    return self.source + self.destination + self.hashid + str(unichr(len(self.payload))) + self.payload.ljust(22, '0')

  @staticmethod
  def decode(packet):
    if len(packet) != Packet.packetSize:
      return None
    source = packet[:2]
    dest = packet[2:4]
    hashid = packet[4:9]
    size = ord(packet[9:10])
    if size > 22:
      print size
      return None
    payload = packet[10:10+size]

    if hashid != Packet.generatehash(source, dest, size, payload):
      print hashid
      return None
    return Packet(source, dest, payload)


  def __init__(self, source, destination, payload):
    self.source = source
    self.destination = destination
    self.payload = payload
  
  @property 
  def hashid(self):
    self.sethash()
    return self._hash
  def sethash(self):
    self._hash = Packet.generatehash(self.source, self.destination, len(self.payload), self.payload)

  def __unicode__(self):
    print self.source + ' ' + self.destination  + ' ' + self.payload + ' ' + self.hashid




class PacketMaker:
  def __init__(self, address=None, size=32):
    if address is not None:
      self._address = address
    else:
      self._address = base64.b64encode(bytes([get_mac()]))[:2]
  def makePackets(self, payload, dest='00'):
    splice = payload
    packets = []
    for i in range(1 + (len(payload)/Packet.payloadSize)):
      packets += Packet(self._address, dest, splice[:Packet.payloadSize])
      splice = splice[self._frameLength:]
    return packets



class BlockThread(threading.Thread):
  def __init__(self, block):
    threading.Thread.__init__(self)
    self.tb = block 
  def run(self):
    self.tb.start()
    self.tb.wait()
    self.tb.stop()

class Acoust:
  def __init__(self, freq):
    
    self._frameLength = 32

    # Pipe for writing
    x, w = os.pipe()
    self._w = os.fdopen(w, 'w', 0)
    #init acoust out
    aout = acoust_out.acoust_out(x, freq, self._frameLength)

    # Pipe for reading
    r, x = os.pipe()
    self._r = os.fdopen(r)
    #init acoust out
    ain = acoust_in.acoust_in(x, freq)

    self._threads = [BlockThread(ain), BlockThread(aout)]
    for thread in self._threads:
      thread.start()

  def getReadFd(self):
    return self._r

  def run(self):
    read = [self._readfifo, self._r]
    while True:
      ir, ur, er = select.select(read, [], read, 3.0)
      for r in ir:
        if r is self._readfifo:
          

          #write to audio
          pass
        elif r is self._r:
          read = self._r.read(self._frameLength)
          pass
          #recover, write to fifo 

    
  def cleanup(self):
    for thread in self._threads:
      thread.join()
    self._w.close()
    self._r.close()


  def write(self, out):
    self.swrite("X" * self._frameLength)
    for packet in out:
      self.write4(packet)
    self.swrite("Z" * self._frameLength)

  def swrite(self, out):
    self._lastwrite = out
    self._w.write(out)

  def write4(self, out):
    #preamble, indicates destination host
    heard = False 
    self._w.write(out)
    heard = self._checkwrite(self._lastwrite)
    if not heard:
      return false
    else:
      self._lastwrite = out
  
  def _checkwrite(self, out):
    read = [self._r]
    while read:
      ir, ur, er = select.select(read, [], read, 3.0)
      for r in ir:
        heard = self._r.read(self._frameLength)
        if heard != out:
          print "want: {}, heard: {}".format(out, heard)
          return False
        else:
          print "I heard the value - " + "want: {}, heard: {}".format(out, heard)
          return True

  def readraw(self):
    heard = self._r.read(self._frameLength)
    return heard
  
class PacketPusher:
  def __init__(self, interface, packeter, inputfile, outputfile):
    self._interface = interface
    self._packeter = packeter
    print "PacketPusher!"
    if not os.path.exists(inputfile):
      os.mkfifo(inputfile)
    if not os.path.exists(outputfile):
      os.mkfifo(outputfile)
    print "opening " + outputfile 
    self._out = open(outputfile, 'w')
    print "opening " + inputfile
    self._in = open(inputfile, 'r')
  def run(self):
    print "Running"
    read = [self._in, self._interface.getReadFd()]
    while read:
      ir, ur, er = select.select(read, [], read)
      for r in ir:
        if r is self._in:
          #read and send
          data = self._in.read()
        elif r is self._interface.getReadFd():
          #read and send
          data = self._interface.readraw()
          self.applicationOut(data)


  def interfaceOut(self, out):
    interface.write(packeter.makePackets(out))

  def applicationOut(self, inf):
    outputfile.write(Packet.decode(inf))

if __name__ == "__main__":
  pp = PacketPusher(Acoust(13000), PacketMaker(), "/home/nathan/inacoust", "/home/nathan/outacoust")
  pp.run()
