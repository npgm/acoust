from multiprocessing import Pool
from acoust_in import acoust_in as AcoustIn
from acoust_file import acoust_out as AcoustOut
from os import path
import os
import signal 
import sys
import fcntl

acoustdev = "/home/nathan/acoustdev/"

def startBlock(tb):
  tb.start()
  tb.wait()
  tb.stop()

def createFifos(fifos):
  for fifo in fifos:
    if not os.path.exists(fifos[fifo]):
      os.mkfifo(fifos[fifo])
    fifos[fifo] = open(fifos[fifo], 'r' if fifo[0] == "T" else 'w')

if __name__ == "__main__":

  pool = Pool(processes=4)
  
  fifos = {"Tx": path.join(acoustdev, "int/atx"), "Rx": path.join(acoustdev, "int/arx"), 
           "Tc": path.join(acoustdev, ".ctl/atc"), "Rc": path.join(acoustdev, ".ctl/arc")}
  #createFifos(fifos)
  print fifos

  xfq = 10 * 1000
  cfq = 11 * 1000
  packet = 32
  
  blocks = [
    # Control Setup
    #AcoustOut(fifos["Tc"].fileno(), cfq),
    #AcoustIn(fifos["Rc"].fileno(), cfq),
    # Data setup
    AcoustOut(path.join(acoustdev, "int/atx"), 15000),
    #AcoustIn(fifos["Rx"].fileno(), xfq)
  ]

  blocks[0].start()
  blocks[0].wait()
  blocks[0].stop()
  pool.map_async(startBlock, blocks)

  def signal_handler(signal, frame):
    pool.terminate()
    sys.exit(0)

  signal.signal(signal.SIGINT, signal_handler)
  print 'Press Ctrl+C'
  signal.pause()

