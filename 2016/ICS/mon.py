#!/usr/bin/python

import socket
import RPi.GPIO as GPIO
from random import randint

HOST, PORT = '', 1337

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

def get_power_factor(status):
  return status

def get_freq(status):
  if (status):
    return randint(58, 62)
  else:
    return randint(0,58)

  return status

def get_voltage(status):
  if status:
    return randint(470, 490)
  else:
    return randint(0, 460)

def get_current(status):
  return status

while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)

    http_response = """\
HTTP/1.1 200 OK

PF: %d
FQ: %d
V: %d
A: %d
""" % (
  get_power_factor(GPIO.input(16)),
  get_freq(GPIO.input(16)),
  get_voltage(GPIO.input(16)),
  get_current(GPIO.input(16)),
)

    client_connection.sendall(http_response)
    client_connection.close()

