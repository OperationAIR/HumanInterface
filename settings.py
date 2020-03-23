import struct
import binascii

class Settings():
    def __init__(self, peep, freq, tidal_vol, pressure, max_pressure, min_pressure, max_tv, min_tv, max_fio2, min_fio2):
        self.peep = int(peep)
        self.freq = int(freq)
        self.tidal_vol = int(tidal_vol)
        self.pressure = int(pressure)
        self.max_pressure = int(max_pressure)
        self.min_pressure = int(min_pressure)
        self.max_tv = int(max_tv)
        self.min_tv = int(min_tv)
        self.max_fio2 = int(max_fio2)
        self.min_fio2 = int(min_fio2)

    def get_bit_string(self):
        #B = unsigned char
        #H = unsigned short
        start_flag = 13
        end_flag = 12
        values = (start_flag, self.peep, self.freq, self.tidal_vol, self.pressure, self.max_pressure,self.min_pressure,self.max_tv,self.min_tv, self.max_fio2, self.min_fio2, end_flag)
        s = struct.Struct('B H H H H H H H H H H B')
        packed_data = s.pack(*values)
        return binascii.hexlify(packed_data)


s = Settings(10, 10, 10, 10, 10, 10, 10, 10, 10, 10)
message = s.get_bit_string()
print(message)
