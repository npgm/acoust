from acoust_in import acoust_in as AcoustIn
from acoust_out import acoust_out as AcoustOut


class BlockThread(threading.Thread):
  def __init__(self, block):
    threading.Thread.__init__(self)
    self.tb = block 
  def run(self):
    self.tb.start()
    self.tb.wait()
    self.tb.stop()

def createFifos(fifos):
  for fifo in fifos:
    if not os.path.exists(fifos[fifo]):
      os.mkfifo(fifos[fifo])
    fifos[fifo] = os.fdopen(fifos[fifo], "r" if fifo[0] == "T" else "w")

if __name__ == "__main__":
  fifos = {"Tx": "int/atx", "Rx": "int/arx", 
           "Tc": ".con/atc", "Rc": ".con/arc"}
  xfq = 20 * 1000
  cfq = 21 * 1000
  packet = 
  
  threads = []
  # Control Setup
  tc = AcoustOut(fifos["Tc"], cfq, packet)
  
  

  
  createFifos(fifos)
