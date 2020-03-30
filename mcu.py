
import serial
import threading
import time
import signal
from queue import Queue
from enum import Enum

import crcmod
from settings import Settings, settings_from_binary
from sensors import Sensors, sensors_from_binary


class SerialCommands(Enum):
    LedOn = 0x55556666
    LedOff = 0x66667777
    NewSettings = 0x41424344
    SensorData = 0x22226666

    def format(self):
        return self.value.to_bytes(4, 'little')

class Microcontroller:

    def __init__(self, port, baudrate, queue: Queue):

        self.serial = None
        self._reader_alive = False
        self.receiver_thread = None
        self.port = port
        self.baudrate = baudrate
        self.crc = crcmod.predefined.mkPredefinedCrcFun('crc-16-usb')
        self.queue = queue
        self.connect()
        self.serialdata = b''

    def _start_reader(self):
        """Start reader thread"""
        print('Start reader thread')
        self._reader_alive = True
        # start serial->console thread
        self.receiver_thread = threading.Thread(target=self._reader, name='rx')
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

    def _stop_reader(self):
        """Stop reader thread only, wait for clean exit of thread"""
        self._reader_alive = False
        if self.serial and hasattr(self.serial, 'cancel_read'):
            self.serial.cancel_read()

        if self.receiver_thread:
            self.receiver_thread.join()

    def _send_buffer(self, buffer: bytes):
        if self.serial:
            self.serial.write(buffer)

    def connect(self):
        self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
        print('open port: ', self.serial, self.serial.port)
        self._start_reader()

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
                    self.queue.put(sensors)
                    data = data[end:]
            elif data.startswith(SerialCommands.NewSettings.format()):
                settings_size = 26
                offset = 4
                end = offset+settings_size
                if len(data[offset:]) >= settings_size:
                    settings = settings_from_binary(data[offset:end])
                    self.queue.put(settings)
                    data = data[end:]
            else:
                # # save data for next round
                # self.serialdata.append(data)
                # print('got unknown data:', data)
                # data = []
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

        except serial.SerialException:
            # ToDo how to handle
            # self.console.cancel()
            raise       # XXX handle instead of re-raise?




if __name__ == "__main__":
    import serial
    import threading
    from settings import Settings

    BAUDRATE = 115200
    TTY = '/dev/cu.usbmodemC1DDCDF83'
    queue = Queue()
    mcu = Microcontroller(TTY, BAUDRATE, queue)

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
        if not queue.empty():
            packet = queue.get()
            print("Got packet:")
            print(packet)

        count += 1

        if count > 10:
            count -= 10
            toggle += 1
            if toggle % 2 == 0:
                mcu.led_on()
            else:
                mcu.led_off()

        time.sleep(0.1)
