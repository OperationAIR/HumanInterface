from collections import namedtuple

# Dev settings
FULLSCREEN = True
SIMULATE = False

# Serial Settings
BAUDRATE = 500000
# for RPi
TTY = '/dev/ttyS0'
# for Mac
#TTY = '/dev/cu.usbmodemC1DDCDF83'
# for Ubuntu
#TTY = '/dev/ttyUSB0'

# Logging
LOGGING_ENABLED = True
LOGDIR = 'sensorlogs'

# Allowed Settings Ranges


ValidSettingsRange = namedtuple('validrange', ['max', 'min', 'step'])

PEEP_RANGE =        ValidSettingsRange(min=5, max=35, step=5)
PRESSURE_RANGE =    ValidSettingsRange(min=10, max=70, step=5)
FREQ_RANGE =        ValidSettingsRange(min=5, max=30, step=1)
OXYGEN_RANGE =      ValidSettingsRange(min=20, max=100, step=5)

# alarm range
# TODO

# colors

BACKGROUND_COLOR = '#161E2E'
BUTTON_COLOR = '#263655'
ALARM_COLOR = '#FF0749'
WARNING_COLOR = '#FFFF00' # todo add correct color
TEXT_COLOR = 'white'