#!/bin/bash

echo "Copy systemd script to /etc/systemd/system/"

sudo cp ./airone.service /etc/systemd/system/airone.service

echo "Reload and enable service"
sudo systemctl daemon-reload
sudo systemctl enable airone.service

echo "All done"
