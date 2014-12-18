from ChatClient.ChatClient_pb2 import ChatMessage as CM
from AcoustAppData.AcoustAppData_pb2 import AcoustAppData as AAD 
import argparse
import socket
import select
import sys

def acoustPack(payload):
  aad = AAD()
  aad.address = '00' #address everyone
  aad.data = payload
  return aad.SerializeToString()

def acoustUnpack(message):
  aad = AAD()
  aad.ParseFromString(message)
  return aad.data

def mesg_print(message):
  print "{}:{} > {}".format(message.time, message.fromUser, message.content)

def run(name, server, address):
  while True:
    inputs, outputs, excepts = select.select([server, sys.stdin], [], [])
    for input in inputs:
      if input is server:
        data, addr = server.recvfrom(2048)
        if addr[0] == address[0]:
          raw_message = acoustUnpack(data)
          message = CM()
          message.ParseFromString(raw_message)
          mesg_print(message)

      elif input is sys.stdin:
        line = sys.stdin.readline()
        message = CM()
        message.fromUser = name 
        message.content = line
        message.time = "1234"
        print("* Sending..."),
        server.sendto(acoustPack(message.SerializeToString()), address)
        print("sent!")
        mesg_print(message)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description='chatwo - an Acoustical chat app')
  parser.add_argument('-p', '--port', type=int, help='server port',
      required='true')
  parser.add_argument('-s', '--server', help='server address',required='true')
  parser.add_argument('-n', '--name', help='your public handle', 
      required='true')
  args = parser.parse_args()

  socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  
  run(args.name, socket, (args.server, args.port))

