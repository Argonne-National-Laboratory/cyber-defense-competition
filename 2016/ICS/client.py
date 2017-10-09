"""Fake modbus client for Argonne's Cyber Defense Competition 2016"""


from pymodbus.client.sync import ModbusTcpClient


__author__ = "Mike Thompson <thompsonm@anl.gov>"


DEBUG = True


# coils are laid out as follows:
# 0-7: powerfactor
# 8-15: frequency
# 16-23: current
# 24-32: voltage


def clear_mem(addr, offset):
  """Clear the memory at the given address + the given offset

  Args:
    addr: int, mem addr
    offset: int, offset
  """
  client = ModbusTcpClient(addr)
  for i in range(offset, offset+8):
    client.write_coil(i, value=False)


def set_val(addr, val, offset):
  """Set a value in memory

  Args:
    addr: int, mem addr
    offset: int, offset
  """
  try:
    client = ModbusTcpClient(addr)
    binary = bin(val)[2:]
  except:
    binary = '00000000'
  if DEBUG:
    print "len: %d" % len(binary)
  length = len(binary)
  word = ''
  if length < 8:
    for i in range(0, 8-length):
      client.write_coil(offset+i, value=False)
      word += '0'

  for i, bit in enumerate(binary):
    i = i+(8-length)
    if bit == '1':
      client.write_coil(offset+i, value=True, unit=0)
      word += '1'
      if DEBUG:
        print "addr: %d val: %s" % (i, True)
    else:
      client.write_coil(offset+i, value=False, unit=0)
      if DEBUG:
        print "addr: %d val: %s" % (i, False)
      word += '0'


  if DEBUG:
    print "wrote %d to memory as %s" % (int(word, 2), word)


def get_val(addr, offset):
  """get a value in memory

  Args:
    addr: int, mem addr
    offset: int, offset
  """
  client = ModbusTcpClient(addr)
  binary = ''
  for i in range(offset, offset+8):
    result = client.read_coils(address=i, count=1, unit=0)
    if DEBUG:
      print "%s" % result.bits[0]
    if result.bits[0]:
      binary += '1'
    else:
      binary += '0'
  if DEBUG:
    print binary
  if DEBUG:
    print int(binary, 2)
  return int(binary, 2)
