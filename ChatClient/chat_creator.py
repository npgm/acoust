from ChatClient_pb2 import ChatMessage as cm
import time
import os

path = "/home/camspill/cuma"
#os.mkfifo(path)


message = cm()
message.fromUser = "Tony Veto"
message.content = "This is a test message generated and written to the Fifo"
message.time = "aoeu"
messageString = message.SerializeToString()

while True:
	with open(path, "w") as fifo:
		fifo.write(messageString)
		time.sleep(2)


