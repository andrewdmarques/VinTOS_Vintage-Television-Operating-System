# Play a video in VLC player in full screen
vlc VTS_01_1.mp4 --fullscreen

# Kill vlc once it is playing
killall -9 vlc

# Change the volume
amixer set Master 100%

# Change the brightness
xrandr --query # To determine what the monitor name is. It should be something like HDMI-1.
xrandr --output HDMI-1 --brightness 0.4

# Interpret the potentiometers
from gpiozero import MCP3008
import time

x = 1
while x < 60:
    print('\n==================Potentiometer Reading==================')
    pot0 = MCP3008(channel = 0)
    print('Pot 0:',round(pot0.value,2))
    pot1 = MCP3008(channel = 1)
    print('Pot 1:',round(pot1.value,2))
    pot2 = MCP3008(channel = 2)
    print('Pot 2:',round(pot2.value,2))
    time.sleep(1)
    x += 1
    
    
