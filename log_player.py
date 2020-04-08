from constants import LOGDIR
from sensors import Sensors
from datetime import datetime
import threading
import Queue

REPLAY_SPEEDUP = 2.0

sf_index = 0
def replay_log(filename, start_index):
   """
   Plays back a CSV log.

   Args: - filename (string): CSV filename
   """

   # Serialize CSV data
   ser_data = []
   with open(LOGDIR + '/' + filename) as logfile:
      for line in logfile:
         # Isolate values
         values = line.split(',')
         # Serialize into Sensors object
         ser_data.append(Sensors.from_list(values))

   # Replay data from a thread
   callback_queue = Queue.Queue()
   global sf_index
   sf_index = start_index
   def dispatch():
      global sf_index
      if sf_index == len(ser_data) - 2: return
      callback_queue.put(ser_data[sf_index])
      sf_index += 1
      interval_sec = (ser_data[sf_index + 1].timestamp - ser_data[sf_index].timestamp).microseconds * 0.000001 / REPLAY_SPEEDUP
      threading.Timer(interval_sec, dispatch).start()
   dispatch()
   return callback_queue