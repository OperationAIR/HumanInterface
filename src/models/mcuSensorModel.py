import struct
from utils.math import pressure_to_cm_h2o
import struct

from utils.math import pressure_to_cm_h2o


class Sensors:
    """
    Sensors represents the sensor data that is sent as the following c struct:

    struct SensorsAllData {
        int32_t flow_inhale;        // Unknonwn (only average flow / total volume MFC)
        int32_t flow_exhale;        // ml / minute ?
        int32_t pressure_inhale;
        int32_t pressure_exhale;
        int32_t pressure_patient;
        int32_t pressure_mfc;
        int32_t oxygen;             // 21-100 (should never be below 21)
        int32_t tidal_volume;       // mL
        int32_t minute_volume;      // L / minute
        int32_t cycle_state;        // PeeP / Peak / None
        int32_t power_status;
    };
    """
    def __init__(self,
            flow_inhale, flow_exhale,
            pressure_inhale, pressure_exhale, pressure_patient, pressure_mfc,
            oxygen,
            tidal_volume, minute_volume,
            cycle_state, power_status):

        self.timestamp = "now"
        self.flow_inhale = flow_inhale / 1000
        self.flow_exhale = flow_exhale / 1000
        self.pressure_inhale = pressure_to_cm_h2o(pressure_inhale)
        self.pressure_exhale = pressure_to_cm_h2o(pressure_exhale)
        self.pressure_patient = pressure_to_cm_h2o(pressure_patient)
        self.pressure_mfc = pressure_to_cm_h2o(pressure_mfc)
        self.oxygen = oxygen
        self.tidal_volume = tidal_volume
        self.minute_volume = minute_volume / 1000
        self.cycle_state = cycle_state # 0 -> stopped 1 -> peak pressure 2 -> peep pressure
        self.power_status = power_status

    @property
    def peep(self):
        return self.cycle_state >= 2

    @property
    def flow(self):
        return self.flow_exhale

    @property
    def pressure(self):
        """ Returns average pressure between inhale and exhale"""
        return (self.pressure_inhale + self.pressure_exhale) / 2.0

    @classmethod
    def num_properties(cls):
        return 11

    @classmethod
    def size(cls):
        prop_size = 4
        return cls.num_properties()*prop_size

    def __repr__(self):
        repr = 'Sensor data: t={}, cycle = {}, flow {}, pressure {} [cm H2O], tidal volume {} [mL], oxygen: {} %'.format(
            self.timestamp,
            self.cycle_state,
            self.flow_exhale,
            self.pressure_exhale,
            self.tidal_volume,
            self.oxygen)
        return repr

    def __str__(self):
        return self.__repr__()

    def as_list(self):
        return [self.timestamp, self.pressure, self.flow, self.tidal_volume,  self.oxygen]

    @classmethod
    def from_binary(cls, packed_data):
        unpacked = struct.unpack('=' + 'i'*cls.num_properties(), packed_data)
        return cls(*unpacked)

    @classmethod
    def default(cls):
        return cls(
            flow_inhale=30,
            flow_exhale=30,
            pressure_inhale=45,
            pressure_exhale=45,
            pressure_patient=45,
            pressure_mfc=45,
            oxygen=40,
            tidal_volume=0,
            minute_volume=0,
            cycle_state=0,
            power_status=1
        )

