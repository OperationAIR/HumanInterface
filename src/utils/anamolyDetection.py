from enum import Enum
from queue import Queue

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import collections as mc
from matplotlib import colors as cl

from models.mcuSettingsModel import Settings
from utils.logPlayer import replay_log


class Anomaly(Enum):
   NONE = 0
   PEEP_TOO_HIGH = 1
   PEEP_TOO_LOW = 2
   PRESS_TOO_HIGH = 3
   PRESS_TOO_LOW = 4

def check_for_anomalies(sensor_frame, settings, visualize=False):
   # Determine current pressure and breathing phase
   curr_press = sensor_frame.pressure
   current_phase = determine_phase(sensor_frame, visualize)

   # Check for PEEP values
   if curr_press < settings.min_peep: return Anomaly.PEEP_TOO_LOW
   if current_phase == 4 and curr_press > settings.max_peep: return Anomaly.PEEP_TOO_HIGH

   # Check for pressure values
   if current_phase == 2 and curr_press < settings.min_pressure: return Anomaly.PRESS_TOO_LOW
   if curr_press > settings.max_pressure: return Anomaly.PRESS_TOO_HIGH

   return Anomaly.NONE

def to_line_collection(x, y, colors):
   global BREATH_IN_C, BREATH_IN_MAX_C, BREATH_OUT_C, BREATH_OUT_MIN_C
   points = np.array([x, y]).T.reshape(-1, 1, 2)
   segments = np.concatenate([points[:-1], points[1:]], axis=1)
   colors = colors[1:] # Truncate colors for segments
   rgba_mat = np.zeros(shape=(len(segments), 4))
   rgba_mat[colors == 1] = cl.to_rgba(BREATH_IN_C)
   rgba_mat[colors == 2] = cl.to_rgba(BREATH_IN_MAX_C)
   rgba_mat[colors == 3] = cl.to_rgba(BREATH_OUT_C)
   rgba_mat[colors == 4] = cl.to_rgba(BREATH_OUT_MIN_C)
   return mc.LineCollection(segments, colors=rgba_mat, linewidths=2)

# Convolution helper functions
def conv(input, filter): return np.convolve(np.array(input), np.array(filter), 'valid')
def conf(input, filter): return np.convolve(np.array(input), np.array(filter), 'full')

BREATH_IN_C = '#3de068'
BREATH_IN_MAX_C = '#08a112'
BREATH_OUT_C = '#3bcbff'
BREATH_OUT_MIN_C = '#057c87'

sensor_buffer = []
state_buffer = np.array([], dtype=int)
cycle_start_index = 0
reached_extrema = False
prev_cycle_state = None
plt_axes = None
def determine_phase(sensor_frame, visualize=False):
   """
   Dynamically determines the current breathing phase.
   This is any of the 4 following phases:
   - 1: Starting to breath in 
   - 2: Holding breath, highest pressure at this point
   - 3: Starting to breath out
   - 4: Finished breathing out, lowest pressure at this point
   The phase is returned as an integer [1-4].
   """
   global prev_cycle_state, reached_extrema, state_buffer, plt_axes, sensor_buffer, cycle_start_index

   # Store and retrieve data
   sensor_buffer.append(sensor_frame)
   x = np.arange(len(sensor_buffer))
   y = np.array([sf.pressure for sf in sensor_buffer])

   # Calculate signal derivative
   delta_filter = conf([0.5, 0.5], [1, -1])
   valid_delta = len(x) >= len(delta_filter)
   if valid_delta:
      dx = np.arange(len(delta_filter) - 1, len(sensor_buffer))
      dy = conv(y, delta_filter)

   # Determine current breath state
   if prev_cycle_state is not None and sensor_frame.cycle_state != prev_cycle_state: reached_extrema = False; cycle_start_index = len(sensor_buffer) - 1
   breath_state = 1 if sensor_frame.cycle_state == 1 else 3
   if not reached_extrema and valid_delta and len(dx) > 5 and len(sensor_buffer) - cycle_start_index > 5:
      if np.mean(dy[-5:-1]) < 0.5 and np.var(dy[-5:-1]) < 1: reached_extrema = True
   elif reached_extrema: breath_state = 2 if sensor_frame.cycle_state == 1 else 4
   state_buffer = np.append(state_buffer, breath_state)
   prev_cycle_state = sensor_frame.cycle_state

   # Make plot dynamic
   if not visualize or len(x) < 2: return breath_state
   if not mpl.is_interactive():
      plt.ion()
      _, plt_axes = plt.subplots(2, figsize=(10, 5))
      plt.subplots_adjust(hspace=0.35, left=0.09, right=0.95, bottom=0.07, top=0.91)
      plt.show()
   for ax in plt_axes: ax.clear()
   PLOT_SIZE = 100

   # Plot main graph
   plt_axes[0].set_title("Pressure over time")
   plt_axes[0].set_xlim(x[-PLOT_SIZE:-1].min() - 1, x[-PLOT_SIZE:-1].max() + 1)
   plt_axes[0].set_ylim(y[-PLOT_SIZE:-1].min() - 5, y[-PLOT_SIZE:-1].max() + 5)
   plt_axes[0].add_collection(to_line_collection(x[-PLOT_SIZE:-1], y[-PLOT_SIZE:-1], state_buffer[-PLOT_SIZE:-1]))

   # Plot derivative
   plt_axes[1].set_title("Pressure change over time")
   if valid_delta: plt_axes[1].plot(dx[-PLOT_SIZE:-1], dy[-PLOT_SIZE:-1])

   # Render plot
   plt.draw(); plt.pause(0.00000000001)
   print("Drawing plot")
   return breath_state

# If script is ran standalone, replay log
if __name__ == "__main__":
   callback_queue = replay_log('sensors_0.csv', 250)
   while True:
      callback = callback_queue.get()
      anomalies = check_for_anomalies(callback, visualize=True)
      if anomalies == Anomaly.NONE: str = 'No anomalies.'
      elif anomalies == Anomaly.PEEP_TOO_LOW: str = 'PEEP WAS TOO LOW!'
      elif anomalies == Anomaly.PEEP_TOO_HIGH: str = 'PEEP WAS TOO HIGH!'
      elif anomalies == Anomaly.PRESS_TOO_LOW: str = 'PRESSURE WAS TOO LOW!'
      elif anomalies == Anomaly.PRESS_TOO_HIGH: str = 'PRESSURE WAS TOO HIGH!'
      print(str)
