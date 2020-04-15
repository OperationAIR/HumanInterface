from models.mcuSensorModel import Sensors
from utils.config import ConfigValues
from datetime import datetime
import threading
from queue import Queue
from pathlib import Path
import os
import csv
import random

REPLAY_SPEEDUP = 2.0

sf_index = 0
def replay_log(filename, start_index):
   """
   Plays back a CSV log.
   Args: - filename (string): CSV filename
   """
   config = ConfigValues()
   ROOT_DIR = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent)
   LOGDIR = config.values['developer']['logDir']
   # Serialize CSV data
   ser_data = []
   with open(ROOT_DIR + '/' + LOGDIR + '/' + filename) as logfile:
      readCSV = csv.reader(logfile, delimiter=',')
      for line in readCSV:
         # Serialize into Sensors object
         ser_data.append(Sensors.from_list(line))

   # Replay data from a thread
   callback_queue = Queue()
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