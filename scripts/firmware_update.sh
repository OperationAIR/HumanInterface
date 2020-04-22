#!/bin/bash

# cd to script dir
cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

while true ; do

    python mcu.py --bootloader --delay
    echo 'Start firmware update over uart..'
    ../bin/mxli -b 115200 -d /dev/ttyS0 -c12M -E ../bin/firmware.bin
    res=$?
    python mcu.py --reset
    if [ "$res" -eq 0 ]; then
        echo 'done'
        break
    fi
    ((c++)) && ((c==10)) && c=0 && break
    echo 'Failed try $c. Try again'
done

# go back to previous directory
cd -

