from constants import LOGDIR
from sensors import Sensors
from datetime import datetime
import threading

UPDATE_INTERVAL_MS = 10

sf_index = 0
def replay_log(filename, callback):
   # Serialize CSV data
   ser_data = []
   with open(LOGDIR + '/' + filename) as logfile:
      for line in logfile:
         # Isolate values
         values = line.split(',')
         # Serialize into Sensors object
         sensors = Sensors.from_list(values)
         sensors.timestamp = datetime.strptime(values[0], '%Y-%m-%d %H:%M:%S.%f')
         ser_data.append(sensors)

   # Replay data from a thread
   def dispatch():
      global sf_index
      callback(ser_data[sf_index])
      sf_index += 1
      threading.Timer(float(UPDATE_INTERVAL_MS) * 0.001, dispatch).start()
   dispatch()