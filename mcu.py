
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


    def _reader(self):
        """loop and copy serial->console"""
        try:
            while self._reader_alive:
                # try to read up to 1kb at a time
                data = self.serial.read(1024)
                if data and len(data):
                    while len(data):
                        print('got', data, SerialCommands.SensorData.format())
                        if data.startswith(b'###'):
                            i = data.index(b'\n')
                            print(data[3:i].decode("utf-8"))
                            # pop text and newline (so i+1)
                            data = data[i+1:]
                        elif data.startswith(SerialCommands.SensorData.format()):
                            # TODO: check data length, save data somewhere if not enough bytes have arrived.
                            #       Then also set timeout to discard data in case data never arrives
                            #       Also we should add the CRC16 to the sensor data

                            s = sensors_from_binary(data[4:])
                            # do something with sensor data
                            print(s)
                            data = []
                        elif data.startswith(SerialCommands.NewSettings.format()):
                            print('settings data:', len(data[4:]))
                            print(settings_from_binary(data[4:]))
                            data = []
                        else:
                            print('got unknown data:', data)
                            data = []
                time.sleep(0.1)

                    # else:
                    #     self.queue.put(data)
                    # print('got {} bytes back'.format(len(data)), type(data))
                    # try:
                    #     if chr(data[-1]) == '\n':
                    #         text = ''.join([chr(c) for c in data])
                    #         print(text)
                    #     else:
                    #         print("Got bytes: ", data)
                    # except e:
                    #     print('parse error:', e)
                    #     pass

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
    conn = SerialConnection(port, baudrate)

    s = Settings(
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
    message = s.get_bit_string()
    print('sending settings: ', len(message), message)
    # print('in ascii: ', binascii.hexlify(message))
    conn.send_buffer(message)

    time.sleep(1)

    req_sensor_data = 0x22226666
    cmd = req_sensor_data.to_bytes(4, 'little')
    conn.send_buffer(cmd)
    exit = False

    def exitFunc(_signal=None, _=None):
        global exit
        conn.disconnect()
        exit = True
        print('bye')

    signal.signal(signal.SIGINT, exitFunc)


    while not exit:
        time.sleep(0.1)
    # TTY = '/dev/cu.SLAB_USBtoUART'


    # with serial.Serial(TTY, 115200, timeout=1) as ser:
    #     ser.write(message)
    #     thread = threading.Thread(target=read_from_port, args=(ser,))
    #     thread.start()

    # print('done, bye')

    # time.sleep(10)
    # thread.join()



