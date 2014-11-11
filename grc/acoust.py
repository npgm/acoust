#!/usr/bin/python

import threading
import os, sys
import acoust_out
import acoust_in
import select

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

    # Pipe for writing
    x, w = os.pipe()
    self._w = os.fdopen(w, 'w', 0)
    #init acoust out
    aout = acoust_out.acoust_out(x, freq)

    # Pipe for reading
    r, x = os.pipe()
    self._r = os.fdopen(r)
    #init acoust out
    ain = acoust_in.acoust_in(x, freq)

    self._threads = [BlockThread(ain), BlockThread(aout)]
    for thread in self._threads:
      thread.start()

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    print "Exiting"
    
  def cleanup(self):
    for thread in self._threads:
      thread.join()
    self._w.close()
    self._r.close()


  def write(self, out):
    self.swrite("XXXX")
    splice = out
    for i in range(1 + (len(out)/4)):
      self.write4(splice[:4].ljust(4, " "))
      splice = splice[4:]
    self.write4("ZZZZ")

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
        heard = self._r.read(4)
        if heard != out:
          print "want: {}, heard: {}".format(out, heard)
          return False
        else:
          print "I heard the value - " + "want: {}, heard: {}".format(out, heard)
          return True

  def read(self):
    read = [self._r]
    while read:
      ir, ur, er = select.select(read, [], read, 3.0)
      for r in ir:
        heard = self._r.read(4)
        if heard != out:
          print "want: {}, heard: {}".format(out, heard)
          return False
        else:
          print "I heard the value - " + "want: {}, heard: {}".format(out, heard)
          return True
  
with Acoust(20000) as ac:
  ac.write("Hello World, my name is Nathan!")

