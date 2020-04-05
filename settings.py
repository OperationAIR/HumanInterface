import struct
from tools import pressure_to_pa, pressure_to_cm_h2o

def settings_from_binary(packed_data):
    unpacked = struct.unpack('H H H H H H H H H H H H H', packed_data)
    crc = [unpacked[-1]]
    start = unpacked[0]
    peep = pressure_to_cm_h2o(unpacked[1])
    freq = unpacked[2]
    ratio = unpacked[3]
    pressure = pressure_to_cm_h2o(unpacked[4])
    oxygen = unpacked[5]
    max_pressure = pressure_to_cm_h2o(unpacked[6])
    min_pressure = pressure_to_cm_h2o(unpacked[7])

    return Settings(start, peep, freq, ratio, pressure, oxygen, max_pressure, min_pressure,
        *unpacked[8:-1], max_peep=0, min_peep=0)

class Settings():

    @staticmethod
    def size():
        return (12*2)

    def __init__(self, start, peep, freq, ratio, pressure, oxygen, max_pressure, min_pressure, max_tv, min_tv, max_fio2, min_fio2, max_peep, min_peep):
        self.start = int(start)
        self.peep = int(peep)
        self.freq = int(freq)
        self.ratio = int(ratio)
        self.pressure = int(pressure)
        self.oxygen = int(oxygen)
        self.max_pressure = int(max_pressure)
        self.min_pressure = int(min_pressure)
        self.max_tv = int(max_tv)
        self.min_tv = int(min_tv)
        self.max_fio2 = int(max_fio2)
        self.min_fio2 = int(min_fio2)
        self.max_peep = int(max_peep)
        self.min_peep = int(min_peep)


    def get_bit_string(self):
        #B = unsigned char
        #H = unsigned short
        values = (
                self.start,
                pressure_to_pa(self.peep),
                self.freq,
                self.ratio,
                pressure_to_pa(self.pressure),
                self.oxygen,
                pressure_to_pa(self.max_pressure),
                pressure_to_pa(self.min_pressure),
                self.max_tv,
                self.min_tv,
                self.max_fio2,
                self.min_fio2)
        s = struct.Struct('H H H H H H H H H H H H')
        packed_data = s.pack(*values)
        return packed_data

    def equals(self, cmp):
        return (
            self.start == cmp.start and
            self.peep == cmp.peep and
            self.ratio == cmp.ratio and
            self.freq == cmp.freq and
            self.pressure == cmp.pressure and
            self.oxygen == cmp.oxygen and
            self.max_pressure == cmp.max_pressure and
            self.min_pressure == cmp.min_pressure and
            self.max_tv==cmp.max_tv and
            self.min_tv==cmp.min_tv and
            self.max_fio2==cmp.max_fio2 and
            self.min_fio2==cmp.min_fio2)


    def __repr__(self):
        return """start {}, peep {}, freq {}, ratio {}, pressure {}, oxygen {}, max_pressure {},
        min_pressure {}, max_tv {}, min_tv {}, max_fiO2 {}, min_fiO2 {}""".format(
            self.start, self.peep, self.freq, self.ratio, self.pressure, self.oxygen,
            self.max_pressure, self.min_pressure, self.max_tv, self.min_tv, self.max_fio2, self.min_fio2)

    def __str__(self):
        return self.__repr__()
