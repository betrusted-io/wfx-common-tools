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

print("*** DID YOU TURN OFF AP SSID SCANNING ON THE EC?? ***")
print("wait for boot...")
time.sleep(2)


dut = WfxTestDut('Serial', port='/dev/ttyS0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=2)
dut.link.trace = True
dut.link.debug = False
dut.trace = True

# dut.test_conditions()

#dut.tone_freq(0)
#dut.tone_power(16)
#dut.tone_start()
#time.sleep(10)
#dut.tone_stop()

dut.run('wfx_test_agent ec_version')
dut.run('wfx_test_agent soc_version')

if False:
   dut.test_ind_period(1000000)
   dut.tx_rx_select(1,1)      # Select antenna 1 in TX/RX
   dut.tx_framing(1500,0)     # Frame size of 1500 bytes with the lowest inter frame space (IFS)
   dut.regulatory_mode('FCC') # set regulatory mode to ETSI or FCC or JAPAN
   dut.channel(11)
   dut.tx_mode('B_1Mbps')
   dut.tx_backoff('B_1Mbps',0.0)  # Tx power reduction of 0.5dB for B_1Mbps (step: 0.25 dB)
   dut.tx_start('continuous')
   dut.run('wfx_test_agent commit_pds')
   time.sleep(10)
   dut.tx_stop()
   dut.run('wfx_test_agent commit_pds')

if True:
   dut.test_ind_period(1000000)
   dut.tx_framing(4091, 0)
   dut.tx_rx_select(1, 1)
   dut.channel(6)
   dut.tx_mode('G_12Mbps')
   dut.tx_power(None) # None == max. Go Python!
   dut.tx_start(0)
#   dut.run('repeat')   # make this the last commpand to stick in this mode forever.
   dut.run('wfx_test_agent commit_pds')
   time.sleep(20)
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


