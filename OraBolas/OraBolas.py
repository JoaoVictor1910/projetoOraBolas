#Adicionando path dependencias#
from pathlib import Path; import sys
path_root = Path(__file__).parents[0]
sys.path.insert(0, str(path_root) + "\\Dependencias")
#---------------------------------#

#Importando dependecias
import time; import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation
###Fim das dependecias###

# The parametrized function to be plotted
def freq(t, amplitude, frequency):
    return amplitude * np.sin(2 * np.pi * frequency * t)

t = np.linspace(0, 1, 1000)

# Define initial parameters
init_amplitude = 5
init_frequency = 3

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line, = plt.plot(t, freq(t, init_amplitude, init_frequency), lw=2)
ax.set_xlabel('Time [s]')

axcolor = 'lightgoldenrodyellow'
ax.margins(x=0)

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the frequency.
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
freq_slider = Slider(
    ax=axfreq,
    label='Time elepsed',
    valmin=0.1,
    valmax=100,
    valinit=init_frequency,
)

# Make a vertically oriented slider to control the amplitude
axamp = plt.axes([0.1, 0.25, 0.0225, 0.63], facecolor=axcolor)
amp_slider = Slider(
    ax=axamp,
    label="Amplitude",
    valmin=0,
    valmax=10,
    valinit=init_amplitude,
    orientation="vertical"
)


# The function to be called anytime a slider's value changes
def update(val):
    line.set_ydata(freq(t, amp_slider.val, freq_slider.val))
    #fig.canvas.draw_idle()


# register the update function with each slider
#freq_slider.on_changed(update)
amp_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def reset(event):
    freq_slider.reset()
    amp_slider.reset()
button.on_clicked(reset)

t_end = time.time() + 10

def animate(i):
    if time.time() < t_end:
        freq_slider.val = t_end - time.time()
        print("ELEPSED: {0:.2f}".format( t_end - time.time()))
    line.set_ydata(freq(t, amp_slider.val , freq_slider.val))
    return line,

ani = animation.FuncAnimation(fig, animate, interval=25, blit=True, save_count=20)

plt.show()
