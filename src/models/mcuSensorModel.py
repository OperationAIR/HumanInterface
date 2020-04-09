import struct

import datetime

from utils.math import pressure_to_cm_h2o
import struct

from utils.math import pressure_to_cm_h2o


class Sensors:
    """
    Sensors represents the sensor data that is sent as the following c struct:

    struct SensorsAllData {
        int32_t flow_inhale;        // Inhale flow [mL / minute] (approximation)
        int32_t flow_exhale;        // Exhale flow [mL / minute]

        int32_t pressure_inhale;    // Inhale pressure [Pa]
        int32_t pressure_exhale;    // Exhale pressure [Pa]
        int32_t pressure_patient;   // Pressure at patient [Pa] (TODO: Not Implemented Yet)
        int32_t pressure_mfc;       // Pressure at MFC pressure vessel [Pa]

        int32_t oxygen;             // Oxygen percentage [0-100]
        int32_t tidal_volume_inhale;       // Tidal volume [mL] (Based on inhale flow)
        int32_t tidal_volume_exhale;       // Tidal volume [mL] (Based on exhale flow)
        int32_t minute_volume;      // Average flow (exhale) [mL / minute] (average over last 10 sec interval)
        int32_t cycle_state;        // PeeP / Peak / None
        uint32_t power_status;      // Status of UPS: volatage [mV OR-ed with UPSStatus bits]

        int32_t inspiratory_hold_result;   // Value for end of inspiratory hold sensor 1
        int32_t expiratory_hold_result;   // Value for end of expiratory hold sensor 1

    }
    """
    def __init__(self,
            flow_inhale,
            flow_exhale,
            pressure_inhale,
            pressure_exhale,
            pressure_patient,
            pressure_mfc,
            oxygen,
            tidal_volume_inhale,
            tidal_volume_exhale,
            minute_volume,
            cycle_state,
            power_status,
            inspiratory_hold_result,
            expiratory_hold_result):

        self.timestamp = datetime.datetime.now()
        self.flow_inhale = flow_inhale / 1000
        self.flow_exhale = flow_exhale / 1000
        self.pressure_inhale = pressure_to_cm_h2o(pressure_inhale)
        self.pressure_exhale = pressure_to_cm_h2o(pressure_exhale)
        self.pressure_patient = pressure_to_cm_h2o(pressure_patient)
        self.pressure_mfc = pressure_to_cm_h2o(pressure_mfc)
        self.oxygen = oxygen
        self.tidal_volume_inhale = tidal_volume_inhale
        self.tidal_volume_exhale = tidal_volume_exhale
        self.minute_volume = minute_volume / 1000
        self.cycle_state = cycle_state # 0: stopped, 1: peak pressure, 2: peep pressure
        self.power_status = power_status
        self.inspiratory_hold_result = inspiratory_hold_result
        self.expiratory_hold_result = expiratory_hold_result

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
        return 14

    @classmethod
    def size(cls):
        prop_size = 4
        return cls.num_properties()*prop_size

    def __repr__(self):
        repr = 'Sensor data: t={}, cycle = {}, flow {}, pressure {} [cm H2O], tidal volume {} [mL], oxygen: {} %, inspiratory hold 1: {}'.format(
            self.timestamp,
            self.cycle_state,
            self.flow_exhale,
            self.pressure_exhale,
            self.tidal_volume_exhale,
            self.oxygen,
            self.inspiratory_hold_result)
        return repr

    def __str__(self):
        return self.__repr__()

    def as_list(self):
        return [[self.timestamp, self.cycle_state, self.pressure, self.flow, self.tidal_volume_exhale,  self.oxygen]]

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
            tidal_volume_inhale=0,
            tidal_volume_exhale=0,
            minute_volume=0,
            cycle_state=0,
            power_status=1,
            inspiratory_hold_result=0,
            expiratory_hold_result=0,
        )

