from log_player import replay_log
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colors as cl
from matplotlib import collections as mc
import numpy as np
import Queue

sensor_buffer = []
peep_buffer = np.array([], dtype=np.bool)
cycles = None
count = 0
state = False
curr_peep = None
figz = None
axz = None
countz = 0
def update(sensor_frame):
   global count, state, curr_peep, peep_buffer, figz, axz, countz
   def conv(input, filter):
      return np.convolve(np.array(input), np.array(filter), 'valid')
   def cons(input, filter):
      return np.convolve(np.array(input), np.array(filter), 'same')
   def conf(input, filter):
      return np.convolve(np.array(input), np.array(filter), 'full')

   sensor_buffer.append(sensor_frame)

   x = np.arange(len(sensor_buffer))
   y = np.array([sf.pressure for sf in sensor_buffer])

   delta_filter = conf([0.5, 0.5], [1, -1])
   delta_delta_filter = conf(conf([0.5, 0.5], [1, -1]), [1, -1])
   # print('d: {}, dd: {}'.format(delta_filter, delta_delta_filter))

   valid_delta = len(x) >= len(delta_filter)
   valid_delta_delta = len(x) >= len(delta_delta_filter)

   if valid_delta:
      dx = np.arange(len(delta_filter) - 1, len(sensor_buffer))
      dy = conv(y, delta_filter)

   if valid_delta_delta:
      ddx = np.arange(len(delta_delta_filter) - 1, len(sensor_buffer))
      ddy = conv(y, delta_delta_filter)

   if valid_delta_delta and len(dy) > 5 and len(ddy) > 5:
      # Detects if we're in peep
      if np.sum(np.abs(dy[-5:-1])) < 2.5 and np.mean(ddy[-5:-1] > 0):
         curr_peep = y[-1]
         print('PEEP zone {}'.format(count))
         count += 1
      else: curr_peep = None

   peep_buffer = np.append(peep_buffer, curr_peep is None)

   points = np.array([x, y]).T.reshape(-1, 1, 2)
   segments = np.concatenate([points[:-1], points[1:]], axis=1)
   colors = np.zeros(shape=(len(segments),4))
   colors[peep_buffer[1:]] = cl.to_rgba('Crimson')
   colors[~peep_buffer[1:]] = cl.to_rgba('slategray')
   lc = mc.LineCollection(segments, colors=colors, linewidths=2)

   if not mpl.is_interactive():
      plt.ion()
      figz, axz = plt.subplots(3, figsize=(10, 5))
      plt.subplots_adjust(hspace=0.43)
      figz.suptitle('Pressure over time')
      plt.show()
   for ax in axz: ax.clear()

   axz[0].plot(x, y)
   if valid_delta: axz[1].plot(dx, dy)
   if valid_delta_delta: axz[2].plot(ddx, ddy)

   plt.draw()
   plt.pause(0.00000000001)

# If script is ran standalone, replay log
if __name__ == "__main__":
   callback_queue = replay_log('sensors_0.csv', 0)
   while True:
      callback = callback_queue.get()
      update(callback)