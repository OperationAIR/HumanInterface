#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "Copy systemd script to /etc/systemd/system/"

sudo cp $DIR/airone.service /etc/systemd/system/airone.service

echo "Reload and enable service"
sudo systemctl daemon-reload
sudo systemctl enable airone.service

echo "All done"
