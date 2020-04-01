
import serial
import threading
import time
import signal
from serial.tools import list_ports
from queue import Queue
from enum import Enum
import random
import binascii

import crcmod
from settings import Settings, settings_from_binary
from sensors import Sensors, sensors_from_binary


class SerialCommands(Enum):
    NewSettings = 0x41424344
    SensorData  = 0x22226666
    LedOn       = 0x55550000
    LedOff      = 0x66660000
    Switch1On   = 0x55551111
    Switch1Off  = 0x66661111
    Switch2On   = 0x55552222
    Switch2Off  = 0x66662222

    def format(self):
        return self.value.to_bytes(4, 'little')

class Microcontroller:

    def __init__(self, port, baudrate, settings_queue: Queue, sensor_queue: Queue, simulate=False):

        self.serial = None
        self._reader_alive = False
        self.receiver_thread = None
        self.port = port
        self.baudrate = baudrate
        self.crc = crcmod.predefined.mkPredefinedCrcFun('crc-16-usb')
        self.settings_queue = settings_queue
        self.sensor_queue = sensor_queue


        self.serialdata = b''

        self.connect()
        self.simulate_thread = None
        if simulate:
            self._simulation_alive = True
            self.simulate_thread = threading.Thread(target=self._simulate_sensor_data, name='simulate')
            self.simulate_thread.daemon = True
            self.simulate_thread.start()

    def _simulate_sensor_data(self):
        while self._simulation_alive:
            sensors = Sensors(random.random()*10, random.random()*40, random.random()*40, random.random()*100)
            self.sensor_queue.put(sensors)
            time.sleep(1)

        print ('exit simulation thread')



    def _start_reader(self):
        """Start reader thread"""
        print('Start reader thread')
        self._reader_alive = True
        self.receiver_thread = threading.Thread(target=self._reader, name='rx')
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

    def _stop_reader(self):
        """Stop reader thread only, wait for clean exit of thread"""
        self._reader_alive = False
        self._simulation_alive = False
        if self.serial and hasattr(self.serial, 'cancel_read'):
            self.serial.cancel_read()

        if self.receiver_thread:
            self.receiver_thread.join()
            print('serial thread joined')

        if self.simulate_thread:
            self.simulate_thread.join()
            print('simulate thread joined')

    def _send_buffer(self, buffer: bytes):
        if self.serial:
            self.serial.write(buffer)

    def connect(self):
        available_ports = [p.device for p in list_ports.comports()]
        print(available_ports)
        if self.port in available_ports:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=0.1)
            print('open port: ', self.serial, self.serial.port)
            self._start_reader()
        else:
            print('could not connect')

    def disconnect(self):
        self._stop_reader()
        if self.serial and self.serial.is_open:
            self.serial.close()


    def led_on(self):
        """Send Led On command to microcontroller"""
        self._send_buffer(SerialCommands.LedOn.format())

    def led_off(self):
        """Send Led Off command to microcontroller"""
        self._send_buffer(SerialCommands.LedOff.format())

    def send_settings(self, settings: Settings):
        """Send new settings to microcontroller"""
        cmd = SerialCommands.NewSettings.format()
        settings_buffer = settings.get_bit_string()
        checksum = self.crc(settings_buffer).to_bytes(2, byteorder='little')
        msg = cmd + settings_buffer + checksum
        self._send_buffer(msg)

    def request_sensor_data(self):
        """Send command to request latest sensor data from microcontroller"""
        self._send_buffer(SerialCommands.SensorData.format())


    def parse_serial_data(self, data):
        while len(data):
            if data.startswith(b'###'):
                i = data.index(b'\n')
                print(data[3:i].decode("utf-8"))
                # pop text and newline (so i+1)
                data = data[i+1:]
            elif data.startswith(SerialCommands.SensorData.format()):
                # TODO: check data length, save data somewhere if not enough bytes have arrived.
                #       Then also set timeout to discard data in case data never arrives
                #       Also we should add the CRC16 to the sensor data

                sensors_size = 4*4
                offset = 4
                end = offset+sensors_size
                if len(data[offset:]) >= sensors_size:
                    sensors = sensors_from_binary(data[offset:end])
                    self.sensor_queue.put(sensors)
                    data = data[end+2:] #account for crc16
                else:
                    print("delete data")
                    data = b''
            elif data.startswith(SerialCommands.NewSettings.format()):
                settings_size = 26
                offset = 4
                end = offset+settings_size
                if len(data[offset:]) >= settings_size:
                    settings = settings_from_binary(data[offset:end])
                    self.settings_queue.put(settings)
                    data = data[end:]
            else:
                print('could not parse: ',binascii.hexlify(data))
                data=b''# # save data for next round

                break;
        return data

    def _reader(self):
        """loop and copy serial->console"""
        try:
            while self._reader_alive:
                # try to read up to 1kb at a time
                newdata = self.serial.read(1024)
                if newdata and len(newdata):
                    self.serialdata += newdata
                    self.serialdata = self.parse_serial_data(self.serialdata)

                time.sleep(0.1)

            print ('exit serial thread')

        except serial.SerialException:
            # ToDo how to handle
            raise       # XXX handle instead of re-raise?




if __name__ == "__main__":
    import serial
    import threading
    from settings import Settings

    BAUDRATE = 115200
    TTY = '/dev/cu.usbmodemC1DDCDF83'
    settings_queue = Queue()
    sensor_queue = Queue()
    mcu = Microcontroller(TTY, BAUDRATE, settings_queue, sensor_queue, simulate=True)

    s = Settings(
        start=0,
        peep=20,
        freq=20,
        ratio=2,
        pressure=40,
        oxygen = 25,
        max_pressure=45,
        min_pressure=5,
        max_tv=400,
        min_tv=200,
        max_fio2=50,
        min_fio2=20)

    mcu.led_on()
    mcu.send_settings(s)

    time.sleep(1)
    mcu.request_sensor_data()

    exit = False

    def exitFunc(_signal=None, _=None):
        global exit
        mcu.disconnect()
        exit = True
        print('bye')

    signal.signal(signal.SIGINT, exitFunc)

    count = 0
    toggle = 0
    while not exit:
        if not sensor_queue.empty():
            packet = sensor_queue.get()
            print("Got sensors:")
            print(packet)
        if not settings_queue.empty():
            packet = settings_queue.get()
            print("Got settings:")
            print(packet)

        count += 1

        if count > 10:
            count -= 10
            toggle += 1
            if toggle % 2 == 0:
                mcu.led_on()
            else:
                mcu.led_off()
                mcu.request_sensor_data()

        time.sleep(0.1)

