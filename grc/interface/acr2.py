from multiprocessing import Pool
from acoust_in import acoust_in as AcoustIn
from acoust_out import acoust_out as AcoustOut
from os import path
import threading
import os
from multiprocessing import Pool
import signal 
import sys
import fcntl
#

class BlockThread(threading.Thread):
  def __init__(self, block):
    threading.Thread.__init__(self)
    self.tb = block 
  def run(self):
    self.tb.start()
    self.tb.wait()
    self.tb.stop()

if __name__ == "__main__":
  xfq = 10 * 1000
  xport = 10000
  cfq = 11 * 1000
  cport = 11000
  packet = 32

  pool = Pool(processes=4)
  
  blocks = [
    # Control Setup
    BlockThread(AcoustOut(cport, packet, cfq)),
    BlockThread(AcoustIn(cport + 1, packet, cfq)),
    # Data setup
    BlockThread(AcoustOut(xport, packet, xfq)),
    BlockThread(AcoustIn(xport + 1, packet, xfq))
  ]
  
  for block in blocks:
    block.start()

  def signal_handler(signal, frame):
    pool.terminate()
    sys.exit(0)

  signal.signal(signal.SIGINT, signal_handler)
  print 'Press Ctrl+C'
  signal.pause()

