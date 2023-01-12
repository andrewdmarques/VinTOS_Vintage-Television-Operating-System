# Interpret the potentiometers
from gpiozero import MCP3008   # To interpret the potentiometers
import time                    # To allow for gaps in time before going through the while loop again.
from datetime import datetime, timedelta  # To get time and make the tv program list
import os                      # To get the directories that are present
import subprocess              # To determine the lengths of each of the programs

###############################################################
#User input variables.
###############################################################
dir_channels = '/media/andrewdmarques/UNTITLED/TV/Channels' # This is the location that the data is stored.
time_delay_sensor = 0.5    # Time (seconds) to pause before checking the potentiometer inputs.
time_delay_channel = 3     # Time (seconds) to allow for transition before playing the program after a channel change or a program ends.

###############################################################
# Define Functions
###############################################################
# Determine the duration of the mp4 files.
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

###############################################################
# Initialization
###############################################################
# Get the current time
time_start = datetime.now()

# Initialize the lists to record the scheduled programming.
prog_channel = []               # The channel that the program is played on
prog = []                  # The program file name
prog_dir = []              # The program file and directory name
prog_len = []              # The length of the program in seconds
prog_after_start = []      # The time since start that the program should begin in seconds
prog_time = []             # The time that the program should begin playing

# Get the channels and programs to play.
channels = os.listdir(dir_channels)
for xx in channels:
    temp_prog = os.listdir(dir_channels+'/'+channels[0])
    
    # Record the channel that this program is located on.
    temp_prog_channel = []
    for yy in temp_prog:
        temp_prog_channel.append(xx)
    
    # Get all the programs for the channel.
    temp_prog_dir = []
    for yy in temp_prog:
        def dir_prog(yy): return dir_channels+'/'+channels[0]+'/'+yy
        temp_prog_dir.append(dir_prog(yy))
    
    # Get the runtimes for all of the mp4 files.
    temp_prog_len = []
    for yy in temp_prog_dir:
        temp_prog_len.append(get_length(yy))
    
    # Determine how many seconds after start to play the program.
    temp_prog_after_start = []
    first = True
    i = 0
    for yy in temp_prog_len:
        # The first item should be 0 seconds after start and the other items would be the previous value + previous runtime.
        if first:
            first = False
            temp_prog_after_start.append(0)
        else:
            temp_prog_after_start.append(temp_prog_after_start[i] + temp_prog_len[i] + time_delay_channel)
            i += 1
    
    # Get the time that the show should start.
    temp_prog_time = []
    i = 0
    for yy in temp_prog_len:
        temp_prog_time.append(time_start + timedelta(seconds = temp_prog_after_start[i]))
        i += 1
        
    # Save all of the variables to their respective master list.
    prog_channel.append(temp_prog_channel)
    prog.append(temp_prog)                  
    prog_dir.append(temp_prog_dir)              
    prog_len.append(temp_prog_len)              
    prog_after_start.append(temp_prog_after_start)      
    prog_time.append(temp_prog_time)






# Play a video in VLC player in full screen
vlc VTS_01_1.mp4 --fullscreen

# Kill vlc once it is playing
killall -9 vlc

# Change the volume
amixer set Master 100%

# Change the brightness
xrandr --query # To determine what the monitor name is. It should be something like HDMI-1.
xrandr --output HDMI-1 --brightness 0.4





# Determine what 
x = 1
while x < 60:
    print('\n==================Potentiometer Reading==================')
    pot0 = MCP3008(channel = 0)
    print('Pot 0:',round(pot0.value,2))
    pot1 = MCP3008(channel = 1)
    print('Pot 1:',round(pot1.value,2))
    pot2 = MCP3008(channel = 2)
    print('Pot 2:',round(pot2.value,2))
    time.sleep(time_delay_sensor)
    x += 1
    
    


