from acoust import Packet

class AcoustPacketDatagram:
  def __init__(self, packets):
      self.packets = packets
      self.packetsAcked = []
  @property
  def size(self):
    return len(selfx.packets)

  def get(packetNum):
    return self.packets[packetNum]