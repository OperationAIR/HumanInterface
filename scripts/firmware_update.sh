#!/bin/bash

# cd to script dir
cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

python mcu.py --bootloader

echo "flash firmware over uart.."

../bin/mxli -b 115200 -d /dev/ttyS0 -c12M -E ../bin/firmware.bin

echo "done"

python mcu.py --reset

# go back to previous directory
cd -