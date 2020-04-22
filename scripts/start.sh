#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

$DIR/production_mode.sh

$DIR/firmware_update.sh

$DIR/../src/main.py