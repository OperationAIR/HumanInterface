import struct
import serial

def get_settings_from_binary(packed_data):
    unpacked = struct.unpack('I H H H H H H H H H H', packed_data)
    return Settings(unpacked[1], unpacked[2], unpacked[3], unpacked[4], unpacked[5], unpacked[6], unpacked[7], unpacked[8], unpacked[9], unpacked[10])

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
        values = (self.peep, self.freq, self.tidal_vol, self.pressure, self.max_pressure,self.min_pressure,self.max_tv,self.min_tv, self.max_fio2, self.min_fio2)
        s = struct.Struct('H H H H H H H H H H')
        packed_data = s.pack(*values)
        return packed_data

    def equals(self, cmp):
        return self.peep == cmp.peep and self.freq == cmp.freq and self.tidal_vol == cmp.tidal_vol and self.pressure == cmp.pressure and self.max_pressure == cmp.max_pressure and self.min_pressure == cmp.min_pressure and self.max_tv==cmp.max_tv and self.min_tv==cmp.min_tv and self.max_fio2==cmp.max_fio2 and self.min_fio2==cmp.min_fio2
