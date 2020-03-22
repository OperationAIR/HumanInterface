'''Function to transmit receive serially to respiratory module by Jeffrey Visser '''
import serial
from time import sleep
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ser = serial.Serial ("/dev/ttyACM1", 115200, timeout=1)    #Open port with baud rate
ser.flushInput()

# Parameters
x_len = 200         # Number of points to display
y_range = [0, 30]  # Range of possible Y values to display

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)

# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)

# Add labels
plt.title('Pressure over Time')
plt.xlabel('Samples')
plt.ylabel('Pressure (mbar)')

# This function is called periodically from FuncAnimation
def animate(i, ys):

    # Read temperature (Celsius) from TMP102
    try:
        pr = ser.readline().decode('utf-8').rstrip()
    except:
        pr = 0
    print(pr)
    
    try:
        pressure = round(float(pr), 2)
    except ValueError:
        pressure = 0

    # Add y to list
    ys.append(pressure)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line.set_ydata(ys)

    return line,

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(ys,), interval=50, blit=True)
plt.show()
