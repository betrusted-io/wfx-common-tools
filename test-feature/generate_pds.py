#!/usr/bin/python3

from wfx_test_dut import *
import time
import RPi.GPIO as GPIO
from collections import OrderedDict

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


#dut = WfxTestDut('Serial', port='/dev/ttyS0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=2, fw_version='3.12.1', agent_version='generate')
dut = WfxTestDut('Local', log='pds.rs')
dut.link.trace = False
dut.link.debug = False
dut.trace = False


rates = ['B_1', 'B_2', 'B_5_5', 'B_11', 'G_6', 'G_9', 'G_12', 'G_18', 'G_24', 'G_36', 'G_48', 'G_54', 'GF_MCS0', 'GF_MCS1', 'GF_MCS2', 'GF_MCS3', 'GF_MCS4', 'GF_MCS5', 'GF_MCS6', 'GF_MCS7']

rate_to_enum = OrderedDict()
rate_to_enum['B_1'] ='B1Mbps'
rate_to_enum['B_2'] ='B2Mbps'
rate_to_enum['B_5_5'] = 'B5_5Mbps'
rate_to_enum['B_11'] = 'B11Mbps'
rate_to_enum['G_6'] = 'G6Mbps'
rate_to_enum['G_9'] = 'G9Mbps'
rate_to_enum['G_12'] = 'G12Mbps'
rate_to_enum['G_18'] = 'G18Mbps'
rate_to_enum['G_24'] = 'G24Mbps'
rate_to_enum['G_36'] = 'G36Mbps'
rate_to_enum['G_48'] = 'G48Mbps'
rate_to_enum['G_54'] = 'G54Mbps'
rate_to_enum['GF_MCS0'] = 'NMCS0'
rate_to_enum['GF_MCS1'] = 'NMCS1'
rate_to_enum['GF_MCS2'] = 'NMCS2'
rate_to_enum['GF_MCS3'] = 'NMCS3'
rate_to_enum['GF_MCS4'] = 'NMCS4'
rate_to_enum['GF_MCS5'] = 'NMCS5'
rate_to_enum['GF_MCS6'] = 'NMCS6'
rate_to_enum['GF_MCS7'] = 'NMCS7'

dut.log.write("""#[derive(Debug, Eq, PartialEq, Copy, Clone)]
pub enum Rate {
""")

for rate in rate_to_enum:
   dut.log.write("    {},\n".format(rate_to_enum[rate]))

dut.log.write("""}

pub struct PdsRecord {
    pub rate: Rate,
    pub pds_data: &'static [[&'static str; 2]; 14],
}

pub const PDS_DATA: [PdsRecord; 20] = [""")

for rate in rate_to_enum:
   dut.log.write("""
    PdsRecord {
        rate: Rate::""")
   dut.log.write("{},".format(rate_to_enum[rate]))
   dut.log.write("""
        pds_data: &[""")
   for channel in range(1,15):
      dut.log.write("""
            [""")
      print('generating {} ch {}'.format(rate, channel))
      dut.test_ind_period(36000000)
      dut.tx_rx_select(1, 1)
      dut.channel(channel)
      dut.tx_mode(rate)
      dut.tx_framing(4091, 0)
      dut.tx_power(None)
      dut.tx_start('continuous')
      #dut.tx_stop()
      dut.log.write("],")
   dut.log.write("""
        ],
    },
""")

dut.log.write("""
];

pub const PDS_STOP_DATA: &str = "{i:{a:6,b:1,f:2255100,c:{a:0,b:0,c:0,d:44},d:{a:FFB,b:0,c:0,d:0,e:f,f:4},e:{}}}";
""")
