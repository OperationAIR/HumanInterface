# Human Interface for Operation AIR

Built in Python 3 using the tkinter gui platform, matplotlib and pyserial.

# For Production
In the case of Production it is assumed that a Raspberry Pi loaded with Raspbian is used.

Clone this repository in the home directory (eg `/home/pi`).

```
git clone https://github.com/OperationAIR/HumanInterface.git
```

Go into the new directory and install python dependencies and run the install script. This script will install the systemd service that automatically starts the app on startup.

Check `Pipfile` for any missing dependencies.

```
cd HumanInterface
pip3 install matplotlib numpy pyserial crcmod pyyaml gpiozero pygame
scripts/install.sh
scripts/production_mode.sh

# test the app
src/main.py
```


## AIROne systemd service

The systemd service is named `airone`

Some useful commands:

```console
# start the service
sudo service airone start
# stop the service and kill the app
sudo service airone stop
# see status overview
sudo service airone status
```

## other scripts

* `mcu.py` for resetting the microcontroller to bootloader and back to application.
* `firmware_update.sh` for updating the microcontroller firmware. It will update to `bin/firmware.bin`.
* `start.sh` is the script called by `airone service`. It will apply the production config, flash the firmware and start the app.

# For Development

## How to install

Check `Pipfile` for requirements. These are easuly installable using [Pipenv](https://pipenv.pypa.io/en/latest/) or you can do it manually.

### Install using pipenv

Go to the project directory and start a pipenv shell `pipenv shell`. Then install dependencies: `pipenv install`

### Install manually

Use pip or apt or brew or any other (python) package manager ot obtain all required dependencies as listed in `Pipfile`

## How to Run

Apply development config, or create your own `config/config.yml` based on `config/config.yml.example`.

```
# run this
scripts/dev_mode.sh

# or
cp config/config.yml.example config/config.yml
# edit config.yml
```

### Run with python3 on ubuntu or Raspbian

*You need python3 in your path*

```console
src/main.py
```

### Run with pipenv

```console
pipenv shell
python src/main.py
```

# License

Copyright (c) 2020 TU Delft. All rights reserved.

Licensed under the [Apache 2.0](LICENSE) license.