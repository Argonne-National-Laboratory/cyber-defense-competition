#!/usr/bin/python2
"""Emergency shutoff switch (with mfr backdoor)"""
import SocketServer, subprocess, sys

HOST = 'localhost'
PORT = 20001
#OMG Hardcoded passwords!
PASSWORD = 'Set me to something good!'

def pipe_command(standard_input=False):
  if standard_input.startswith(PASSWORD):
    print subprocess.check_output("kill $(ps awx |grep modbus |awk '{print$1}'|xargs)", shell=True)

class SingleTCPHandler(SocketServer.BaseRequestHandler):
  "One instance per connection.  Override handle(self) to customize action."
  def handle(self):
    # self.request is the client connection
    data = self.request.recv(1024)  # clip input at 1Kb
    reply = pipe_command(data)
    if reply is not None:
      self.request.send(reply)
    self.request.close()

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
  daemon_threads = True
  allow_reuse_address = True

  def __init__(self, server_address, RequestHandlerClass):
    SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
  server = SimpleServer((HOST, PORT), SingleTCPHandler)
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    sys.exit(0)
