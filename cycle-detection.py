from log_player import replay_log

def update(sensor_frame):
   print(sensor_frame)

# If script is ran standalone, replay log
if __name__ == "__main__": replay_log('sensors_0.csv', update)