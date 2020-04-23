#!/usr/bin/env python3
from time import sleep
import argparse

from gpiozero import DigitalOutputDevice

rst = DigitalOutputDevice(16, active_high=False, initial_value=False)
isp = DigitalOutputDevice(17, active_high=False, initial_value=False)

parser = argparse.ArgumentParser(
    description='Simple tool to reset lpc11u37 or put it in bootloader mode for in-system programming (ISP)')

parser.add_argument('--reset', action='store_true',
    help="trigger mcu reset")

parser.add_argument('--bootloader', action='store_true',
    help="restart mcu in uart bootloader")

parser.add_argument('--delay', action='store_true',
    help="Extra 1 second delay at end")

args = parser.parse_args()

delay = 0.01
if args.reset:
    print('resetting..')
    rst.on()
    sleep(delay)
    print('mcu should be reset to regular firmware now')
    rst.off()
elif args.bootloader:
    print('reset to uart bootloader..')
    isp.on()
    sleep(delay)
    rst.on()
    sleep(delay)
    rst.off()
    sleep(delay)
    isp.off()
    print('mcu should be in uart bootloader now')
else:
    parser.print_help()


if args.delay:
    sleep(1)
