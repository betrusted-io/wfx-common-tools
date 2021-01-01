#!/usr/bin/python3

from wfx_test_dut import *
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def reset_ec():
   print("reset EC")
   # reset EC
   GPIO.setup(25, GPIO.OUT)
   GPIO.output(25, GPIO.LOW)
   time.sleep(0.2)
   GPIO.output(25, GPIO.HIGH)

def reset_soc():
   print("reset SOC")
   # reset SoC
   GPIO.setup(24, GPIO.OUT)
   GPIO.output(24, GPIO.LOW)
   time.sleep(0.2)
   GPIO.output(24, GPIO.HIGH)

reset_ec()
reset_soc()

print("wait for boot...")
time.sleep(2)


dut = WfxTestDut('Serial', port='/dev/ttyS0', baudrate=115200, bytesize=8, parity='N', stopbits=1)
dut.link.trace = True
dut.link.debug = False
dut.trace = True

# dut.test_conditions()

#dut.tone_freq(0)
#dut.tone_power(16)
#dut.tone_start()
#time.sleep(10)
#dut.tone_stop()

if True:
   dut.test_ind_period(10000)
   dut.tx_framing(4091, 0)
   dut.channel(1)
   dut.tx_rx_select(1, 1)
   dut.tx_mode('N_MCS7')
   dut.tx_power(None) # None == max
   dut.tx_start(0)
   dut.run('wfx_test_agent commit_pds')
   time.sleep(30)
   dut.tx_stop()
   dut.run('wfx_test_agent commit_pds')

if False:
   dut.test_ind_period(10000)
   dut.tx_framing(4091, 0)
   dut.channel(1)
   dut.tx_rx_select(1, 1)
   dut.tx_mode('B_1')
   dut.tx_power(None) # None == max
   dut.tone_start(0)
   dut.run('wfx_test_agent commit_pds')
   time.sleep(30)
   dut.tx_stop()
   dut.run('wfx_test_agent commit_pds')
   
if False:
   reset_ec()
   reset_soc()


