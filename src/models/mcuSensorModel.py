import datetime
import struct
from enum import Enum

from utils.config import ConfigValues
from utils.math import pressure_to_cm_h2o


class UPSStatus(Enum):
    UNKNOWN              = (0),
    OK                   = (1 << 31)
    BATTERY_POWERED      = (1 << 30)
    FAIL                 = (1 << 29)


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

        int32_t inspiratory_hold_result;   // Value for end of inspiratory hold sensor 1
        int32_t expiratory_hold_result;   // Value for end of expiratory hold sensor 1

        uint32_t power_status;      // Status of UPS: voltage [mV OR-ed with UPSStatus bits]
        uint32_t system_status;         // enum SystemStatus value(s) OR-ed together

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
            inspiratory_hold_result,
            expiratory_hold_result,
            power_status,
            system_status):

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
        self.inspiratory_hold_result = pressure_to_cm_h2o(inspiratory_hold_result)
        self.expiratory_hold_result = pressure_to_cm_h2o(expiratory_hold_result)
        self.system_status = system_status

        self.config = ConfigValues()


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
        return 15

    @classmethod
    def size(cls):
        prop_size = 4
        return cls.num_properties()*prop_size

    @property
    def ups_status(self):
        status = self.power_status & 0xF0000000
        if status == UPSStatus.OK.value:
            return UPSStatus.OK
        elif status == UPSStatus.BATTERY_POWERED.value:
            return UPSStatus.BATTERY_POWERED
        elif status == UPSStatus.FAIL.value:
            return UPSStatus.FAIL
        else:
            return UPSStatus.UNKNOWN

    @property
    def battery_percentage(self):
        battery_mv = self.power_status & 0x0000FFFF
        zero = self.config.values['defaultSettings']['min_batt_voltage']
        full = self.config.values['defaultSettings']['max_batt_voltage']
        battery_percentage = max(min((battery_mv - zero) / (full - zero) * 100, 100), 0)
        return battery_percentage


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
        return [[self.timestamp, self.cycle_state, self.pressure_inhale, self.pressure_exhale, self.flow, self.tidal_volume_inhale, self.tidal_volume_exhale, self.oxygen]]

    @classmethod
    def from_list(cls, list_data):
        # For testing different battery levels and whether power is connected
        # ps = 0x80006338 # Full battery and UPS OK
        # ps = 0x40006338 # Full battery and UPS Battery powered
        # ps = 0x40005c30 # Zero battery and UPS Battery powered
        # ps = 0x80005c30 # Zero battery and UPS OK
        # ps = 0x80005fb4 # 50 % battery and UPS OK
        ps = 0x40005fb4 # 50 % battery and UPS Battery powered

        sensors = Sensors(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, ps, 0)
        sensors.timestamp = datetime.datetime.strptime(list_data[0], '%Y-%m-%d %H:%M:%S.%f')
        sensors.cycle_state = int(list_data[1])
        sensors.pressure_inhale = float(list_data[2])
        sensors.pressure_exhale = float(list_data[3])
        sensors.flow_exhale = float(list_data[4])
        sensors.tidal_volume_inhale = int(list_data[5])
        sensors.tidal_volume_exhale = int(list_data[6])
        sensors.oxygen = int(list_data[7])
        return sensors

    @classmethod
    def from_binary(cls, packed_data):
        num_unsigned_properties = 2
        num_signed_properties = cls.num_properties() - num_unsigned_properties

        unpacked = struct.unpack('=' + 'i'*num_signed_properties + 'I'*num_unsigned_properties, packed_data)
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
            inspiratory_hold_result=0,
            expiratory_hold_result=0,
            power_status=0x800063381,
            system_status=0
        )
