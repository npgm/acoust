from acoust_out import acoust_out as AcoustOut

aout = AcoustOut(10000, 32, 10000)
aout.start()
aout.wait()
aout.stop()

