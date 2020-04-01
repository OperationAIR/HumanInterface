
import datetime
import struct
from tools import pressure_to_cm_h2o

class Sensors:
    """
    Sensors represents the sensor data that is sent as the following c struct:

    # struct SensorsAllData {
    #     int32_t flow;
    #     int32_t pressure_1_pa;
    #     int32_t pressure_2_pa;
    #     int32_t oxygen;
    # };
    """
    def __init__(self, flow, pressure1, pressure2, oxygen):
        self.timestamp = datetime.datetime.now()
        self.flow = flow
        self.pressure_1_pa = pressure_to_cm_h2o(pressure1)
        self.pressure_2_pa = pressure_to_cm_h2o(pressure2)
        self.oxygen = oxygen

    def __repr__(self):
        repr = 'Sensor data: t={}, flow {}, pressure1 {} [pa], pressure2 {} [pa], oxygen: {} %'.format(
            self.timestamp,
            self.flow,
            self.pressure_1_pa,
            self.pressure_2_pa,
            self.oxygen)
        return repr

    def __str__(self):
        return self.__repr__()

def sensors_from_binary(packed_data):
    unpacked = struct.unpack('=iiii', packed_data)
    return Sensors(*unpacked)

