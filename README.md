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

# DISCLAIMER

Licensor means Technische Universiteit Delft and OperationAIR

Licensee means any business, organisation or person using the Licensed Material

Licensed Material means all information pertaining to the last resort ventilator also known as the AIRone

### Intended use

1.  The AIRone is a last resort device. It is not designed to replace the currently available, conventional ventilators. The AIRone is a pressure-controlled emergency mechanical ventilation system created for the treatment of COVID-19 patients, who need respiratory support, for who no conventional ventilation machine is available.
2.  The for profit exploitation of the Licensed Material is explicitly prohibited.

### Disclaimer of Warranties and Limitation of Liability.

The Licensor offers the Licensed Material “as-is” and “as-available”, and makes no representations or warranties of any kind concerning the Licensed Material, whether express, implied, statutory, or other. This includes, without limitation, warranties of title, merchantability, fitness for a particular purpose, non-infringement, absence of latent or other defects, accuracy, or the presence or absence of errors, whether or not known or discoverable.
To the extent possible, in no event will the Licensor be liable to Licensee on any legal grounds (including, but not limited to, gross negligence and wilful misconduct) or otherwise for any direct, special, indirect, incidental, consequential, punitive, exemplary, or other losses, costs, expenses, or damages arising out of this Public License or use of the Licensed Material, even if the Licensor has been advised of the possibility of such losses, costs, expenses, or damages.

The disclaimer of warranties and limitation of liability provided above shall be interpreted in a manner that, to the extent possible, most closely approximates an absolute disclaimer and waiver of all liability.
