#!/usr/bin/python2
"""Run the electrical subsystem for SimmonsSystems"""

import client
import random
import time

addr = '127.0.0.1'

while True:
  pfgood_range = (92, 100)
  pfour_val = random.randrange(pfgood_range[0], pfgood_range[1])


  fgood_range = (59, 61)
  four_val = random.randrange(fgood_range[0], fgood_range[1])

  cgood_range = (90, 110)
  cour_val = random.randrange(cgood_range[0], cgood_range[1])

  vgood_range = (228, 252)
  vour_val = random.randrange(vgood_range[0], vgood_range[1])

  client.set_val(addr, pfour_val, 0)
  client.set_val(addr, four_val, 8)
  client.set_val(addr, cour_val, 16)
  client.set_val(addr, vour_val, 24)
  time.sleep(2)
