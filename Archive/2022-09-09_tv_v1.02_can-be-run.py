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
time_bri_steps = 2         # Time (seconds) to incrementally brighten the screen before a channel is displayed.
time_bri_rate = 10         # Rate (steps/second) to incrementally brighten the screen before a channel is displayed.

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
prog_channel = []          # The channel that the program is played on
prog = []                  # The program file name
prog_dir = []              # The program file and directory name
prog_len = []              # The length of the program in seconds
prog_after_start = []      # The time since start that the program should begin in seconds
prog_time = []             # The time that the program should begin playing

# Get the channels and programs to play.
channels = os.listdir(dir_channels)
for xx in channels:
    print('Processing channel: '+xx)
    
    # Get the programs in the channel
    temp_prog = os.listdir(dir_channels+'/'+xx)
    
    # Record the channel that this program is located on.
    temp_prog_channel = []
    for yy in temp_prog:
        temp_prog_channel.append(xx)
    
    # Get all the programs for the channel.
    temp_prog_dir = []
    for yy in temp_prog:
        def dir_prog(yy): return dir_channels+'/'+xx+'/'+yy
        temp_prog_dir.append(dir_prog(yy))
    
    # Get the runtimes for all of the mp4 files.
    temp_prog_len = []
    for yy in temp_prog_dir:
        #print('Processing runtime for: '+xx+' '+yy)
        temp_prog_len.append(get_length(yy))
    
    # Determine how many seconds after start to play the program.
    temp_prog_after_start = []
    first = True
    i = 0
    for yy in temp_prog_len:
        #print('Processing program start time for: '+xx+' '+yy)
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
    i = 0
    for yy in temp_prog:
        prog_channel.append(temp_prog_channel[i])
        prog.append(temp_prog[i])                  
        prog_dir.append(temp_prog_dir[i])              
        prog_len.append(temp_prog_len[i])              
        prog_after_start.append(temp_prog_after_start[i])      
        prog_time.append(temp_prog_time[i])
        i += 1

# Determine the starting channel (this will be labeled the "previous channel").
pot2 = MCP3008(channel = 2)
channel_prev = 0 # Set the previous channel to 0 so that it will initialize the first time through the main loop.

# Refresh the current time.
time_start = datetime.now()

###############################################################
# Main script
###############################################################
print('Executing main script')

x = 1
while x < 60:
    # Wait the specified amount of time between taking potentiometer readings.
    time.sleep(time_delay_sensor)
    
    # Get the current programming time (seconds).
    time_sec = datetime.now() - time_start
    time_sec = time_sec.total_seconds()
    
    # Get the potentiometers' readings.
    print('\n==================Potentiometer Reading==================')
    pot0 = MCP3008(channel = 0)
    print('Pot 0:',round(pot0.value,2))
    pot1 = MCP3008(channel = 1)
    print('Pot 1:',round(pot1.value,2))
    pot2 = MCP3008(channel = 2)
    print('Pot 2:',round(pot2.value,2))
    x += 1
    
    # Make brightness adjustments.
    bri = round(pot0.value,2)
    bri_command = 'xrandr --output HDMI-1 --brightness '+str(bri)
    os.system(bri_command)
    
    # Make volume adjustments.
    vol = round(pot1.value*100,0)
    vol_command = 'amixer set Master ' + str(int(vol)) + '%'
    os.system(vol_command)
    
    # Determine if channel should be changed.
    channel_curr = int(round(pot2.value/(1/12)+1,0)) # There are 13 channels, so which potentiometer reading is most close to a channel. This will give values 1 to 13
    if channel_curr != channel_prev:
        print('Channel changed from '+str(channel_prev)+' to '+str(channel_curr))
        # Set the brightness to 0.
        #os.system('xrandr --output HDMI-1 --brightness 0.2')
        
        # Stop the current program.
        # killall -9 vlc
        
        # XXX Check that the channel has not been changed for xxx seconds, this makes sure that it does not skip to just the first channel 
        
        # Determine which channel directory corresponds with the inputted channel number.
        temp = str(channel_curr).rjust(2,'0')
        prog_channel_curr = [match for match in channels if temp in match] # The input channel will be a number, like 2, so this will find any directories that have 02 in them, the first one that matches will be considered the channel to play.
        # Determine which program should start.
        i = 0
        play = False

        
        
        # Start the next program.
        
        # Pause for the appropriate amount of time.
        
        # Increase the brightness to the set level.
        
    channel_prev = channel_curr
    
    # Determin if it is time for the next program.
    
    
