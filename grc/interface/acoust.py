#!/usr/bin/python

import time
import socket
from AcoustAppData_pb2 import AcoustAppData
import threading
import os, sys
import acoust_out
import acoust_in
import select
from uuid import getnode as get_mac
import base64
import hashlib
import datetime

class Packet(object):
  packetSize = 32
  payloadSize = 22

  @staticmethod
  def generatehash(source, dest, size, payload): 
    md5bytes=hashlib.md5(source + dest + str(unichr(size)) + payload + str(time.time())).digest()
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
    self.frameLength = size
  def makePackets(self, adp):
    splice = adp.data
    packets = []
    for i in range(1 + (len(splice)/Packet.payloadSize)):
      packets.append(Packet(self._address, adp.address, splice[:Packet.payloadSize]))
      print "{}: {}".format(len(packets) - 1, packets[len(packets) - 1].encode())
      splice = splice[self.frameLength:]
    return packets

class Acoust:
  def __init__(self, freq, host, port):
    self.packeter = PacketMaker()
    self._xport = 10000
    self._cport = 11000
    self._frameLength = 32

    self._writeApp = (host, port)
    self._writeAcr = (host, self._xport)
    self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    self._appread = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self._appread.bind((host, port))

    self._acrread = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self._acrread.bind((host, self._xport+1))

  def run(self):
    read = [self._acrread, self._appread]
    while True:
      print "Selecting on ARC and APP"
      ir, ur, er = select.select(read, [], read, 3.0)
      for r in ir:
        if r is self._acrread:
          print "Data incoming from ACR"
          data, address = r.recvfrom(32)
          self._sock.sendto(message, self._writeApp)
        elif r is self._appread:
          print "Data incoming from APP"
          data, address = r.recvfrom(10000)
          # data represents a protobuf AppDataPacket
          adp = AcoustAppData()
          adp.ParseFromString(data)
          print "received a data packet addressed to {}".format(adp.address)
          datagram = self.packeter.makePackets(adp)
          self.write(datagram)

  def write(self, out):
    for packet in out:
      self.write4(packet.encode())

  def write4(self, out):
    self._sock.sendto(out, self._writeAcr)
    heard = self._checkwrite(out)
    if not heard:
      return false
  
  def _checkwrite(self, out):
    read = [self._acrread]
    while read:
      ir, ur, er = select.select(read, [], read, 3.0)
      for r in ir:
        heard = r.recvfrom(self._frameLength)
        if heard != out:
          print "want: {}, heard: {}".format(out, heard)
          return False
        else:
          print "I heard the value - want: {}, heard: {}".format(out, heard)
          return True

if __name__ == "__main__":
  acoust = Acoust(12000, "127.0.0.1", 20000)
  print "Running Acoust..."
  acoust.run()
  

