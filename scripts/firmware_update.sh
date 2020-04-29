#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

while true ; do

    python3 $DIR/mcu.py --bootloader --delay
    echo "Start firmware update over uart.."
    $DIR/../bin/mxli -b 115200 -d /dev/ttyS0 -c12M -E $DIR/../bin/firmware.bin
    res=$?
    python3 $DIR/mcu.py --reset
    if [ "$res" -eq 0 ]; then
        echo 'done'
        break
    fi
    ((c++)) && ((c==3)) && c=0 && break
    echo "Failed try $c. Try again"
done
