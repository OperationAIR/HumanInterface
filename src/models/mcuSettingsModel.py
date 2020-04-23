import struct

from utils.config import ConfigValues
from utils.math import pressure_to_cm_h2o, pressure_to_pa


class MCUSettings:

    def __init__(self, start, peep, freq, ratio, pressure, oxygen):
        self.start = int(start)
        self.peep = int(peep)
        self.freq = int(freq)
        self.ratio = int(ratio)
        self.pressure = int(pressure)
        self.oxygen = int(oxygen)

    @classmethod
    def num_properties(cls):
        return 6

    @classmethod
    def size(cls):
        """binary size including crc"""
        return (cls.num_properties()*2 + 2)

    @classmethod
    def from_binary(cls, packed_data):
        """ reconstruct mcu settings from binary blob """

        # num + 1 because of crc16
        num_values = cls.num_properties() + 1
        unpacked = struct.unpack('H'*num_values, packed_data)
        crc = [unpacked[-1]]

        start = unpacked[0]
        peep = pressure_to_cm_h2o(unpacked[1])
        freq = unpacked[2]
        ratio = unpacked[3]
        pressure = pressure_to_cm_h2o(unpacked[4]) - peep
        oxygen = unpacked[5]
        return cls(start, peep, freq, ratio, pressure, oxygen)


    def pack(self):
        """Create binary struct to send to mcu"""
        values = (
                self.start,
                pressure_to_pa(self.peep),
                self.freq,
                self.ratio,
                pressure_to_pa(self.pressure + self.peep),
                self.oxygen)

        print(values)

        s = struct.Struct('H'*len(values))
        packed_data = s.pack(*values)
        return packed_data


# class alarmSettings:

#     def __init__(self, max_pressure, min_pressure, max_tv, min_tv, max_fio2, min_fio2, max_peep, min_peep)
#         self.max_pressure = int(max_pressure)
#         self.min_pressure = int(min_pressure)
#         self.max_tv = int(max_tv)
#         self.min_tv = int(min_tv)
#         self.max_fio2 = int(max_fio2)
#         self.min_fio2 = int(min_fio2)
#         self.max_peep = int(max_peep)
#         self.min_peep = int(min_peep)

class Settings():



    def __init__(self, start, peep, freq, ratio, pressure, oxygen, max_pressure, min_pressure, max_tv, 
            min_tv, max_fio2, min_fio2, max_peep, min_peep, min_batt_voltage, max_batt_voltage, min_batt):
        # settings for mcu
        self.start = int(start)
        self.peep = int(peep)
        self.freq = int(freq)
        self.ratio = int(ratio)
        self.pressure = int(pressure)
        self.oxygen = int(oxygen)

        # alarm settings
        self.max_pressure = int(max_pressure)
        self.min_pressure = int(min_pressure)
        self.max_tv = int(max_tv)
        self.min_tv = int(min_tv)
        self.max_fio2 = int(max_fio2)
        self.min_fio2 = int(min_fio2)
        self.max_peep = int(max_peep)
        self.min_peep = int(min_peep)

        # Battery settings
        self.min_batt_voltage = int(min_batt_voltage)
        self.max_batt_voltage = int(max_batt_voltage)
        self.min_batt = int(min_batt)

    @classmethod
    def fromConfig(cls):
        config = ConfigValues()

        start = config.values["defaultSettings"]["start"]
        peep = config.values["defaultSettings"]["peep"]
        freq = config.values["defaultSettings"]["freq"]
        ratio = config.values["defaultSettings"]["ratio"]
        pressure = config.values["defaultSettings"]["pressure"]
        oxygen = config.values["defaultSettings"]["oxygen"]

        max_pressure = config.values["alarmSettings"]["max_pressure"]
        min_pressure = config.values["alarmSettings"]["min_pressure"]
        max_tv = config.values["alarmSettings"]["max_tv"]
        min_tv = config.values["alarmSettings"]["min_tv"]
        max_fio2 = config.values["alarmSettings"]["max_fio2"]
        min_fio2 = config.values["alarmSettings"]["min_fio2"]
        max_peep = config.values["alarmSettings"]["max_peep"]
        min_peep = config.values["alarmSettings"]["min_peep"]

        min_batt_voltage = config.values["defaultSettings"]["min_batt_voltage"]
        max_batt_voltage = config.values["defaultSettings"]["max_batt_voltage"]

        min_batt = config.values["alarmSettings"]["min_batt"]

        return cls(start, peep, freq, ratio, pressure, oxygen, max_pressure, min_pressure, max_tv, 
            min_tv, max_fio2, min_fio2, max_peep, min_peep, min_batt_voltage, max_batt_voltage, min_batt)

    def pack_mcu_settings(self):

        return MCUSettings(
                self.start,
                self.peep,
                self.freq,
                self.ratio,
                self.pressure,
                self.oxygen).pack()

    def equals(self, cmp: MCUSettings):
        """Check received mcu settings against current settings"""
        return (
            self.start == cmp.start and
            self.peep == cmp.peep and
            self.ratio == cmp.ratio and
            self.freq == cmp.freq and
            self.pressure == cmp.pressure and
            self.oxygen == cmp.oxygen)


    def __repr__(self):
        return """start {}, peep {}, freq {}, ratio {}, pressure {}, oxygen {}, max_pressure {},
        min_pressure {}, max_tv {}, min_tv {}, max_fiO2 {}, min_fiO2 {}, 
        min_batt_voltage {}, max_batt_voltage {}, min_batt {}""".format(
            self.start, self.peep, self.freq, self.ratio, self.pressure, self.oxygen,
            self.max_pressure, self.min_pressure, self.max_tv, self.min_tv, self.max_fio2, self.min_fio2,
            self.min_batt_voltage, self.max_batt_voltage, self.min_batt)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def from_mcuSettings(cls, mcuSettings: MCUSettings):
        """ Create settings from MCUSettings and default alarms"""

        settings = cls.fromConfig()
        settings.start = mcuSettings.start
        settings.peep = mcuSettings.peep
        settings.freq = mcuSettings.freq
        settings.ratio = mcuSettings.ratio
        settings.pressure = mcuSettings.pressure
        settings.oxygen = mcuSettings.oxygen

        return settings
