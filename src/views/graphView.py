from collections import deque
from time import time

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils.config import ConfigValues

matplotlib.use("TkAgg")


class GraphView:

    def __init__(self, title, ylabel, data, yrange, xlen, linecolor="#ffffff", parent=None):
        self.linecolor = linecolor
        self.xlen = xlen
        self.yrange = yrange
        self.data = data
        self.title = title
        self.ylabel = ylabel
        self.parent = parent

        self.config = ConfigValues()

        self.yaxisRefreshTime = time()

        self.ys = deque([0 for x in range(xlen)], maxlen=xlen)

    def update(self, data):
        self.data = data

    def getPlot(self):

        # Parameters
        x_len = self.xlen         # Number of points to display
        y_range = self.yrange  # Range of possible Y values to display

        # Create figure for plotting
        self.fig = plt.figure(figsize=(1,1))
        self.fig.patch.set_facecolor(self.config.values['colors']['darkBlue'])
        ax = self.fig.add_subplot(1, 1, 1, facecolor=self.config.values['colors']['darkBlue'])
        #ax.spines['bottom'].set_color('gray')

        xs = list(range(-x_len, 0))

        ax.set_ylim(bottom=min(y_range), top=max(y_range))
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("white")
        ax.get_yaxis().tick_left()
        ax.yaxis.label.set_size(13)
        ax.yaxis.label.set_color('white')
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.yticks(fontsize=13, color='white')

        plt.tick_params(axis="both", which="both", bottom=False, top=False,
                labelbottom=False, left=False, right=False, labelleft=True, colors="white")
        
        # Create a blank line. We will update the line in animate
        line, = ax.plot(xs, self.ys, color= self.linecolor)

        # Add labels
        plt.title(self.title, fontsize= 13, color="white")
        plt.ylabel(self.ylabel)
        plt.gcf().subplots_adjust(top=0.8, left=0.2, right=1, bottom=0.18)

        # This function is called periodically from FuncAnimation
        def animate(i, ys):
            # Add y to list
            ys.append(self.data)
            # Update line with new Y values
            line.set_ydata(ys)

            if time() - self.yaxisRefreshTime >= self.config.values['defaultSettings']['graphYaxisUpdateInterval']:
                margin = 5
                ax.set_ylim(bottom=min(ys)-margin, top=max(ys)+margin)
                self.canvas.draw()
                self.yaxisRefreshTime = time()

            return line,
        # Set up plot to call animate() function periodically

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
        self.flow_animation_ref = animation.FuncAnimation(self.fig,
           animate,
           fargs=(self.ys,),
           interval=100,
           blit=True)

        return self.canvas.get_tk_widget()
