#!/usr/bin/python3
# import the libraries.
from gpiozero import MCP3008   # To interpret the potentiometers
import time                    # To allow for gaps in time before going through the while loop again.
from datetime import datetime, timedelta  # To get time and make the tv program list
import os                      # To get the directories that are present
import subprocess              # To determine the lengths of each of the programs

###############################################################
#User input variables.
###############################################################
dir_channels = '/media/andrewdmarques/UNTITLED/TV/Channels' # This is the location that the data is stored.
time_delay_sensor = 0.05    # Time (seconds) to pause before checking the potentiometer inputs.
time_delay_channel_input=2 # Time (seconds) to pause before committing to changing the channel.
time_delay_channel = 10     # Time (seconds) to allow for transition before playing the program after a channel change or a program ends.
time_bri_steps = 2         # Time (seconds) to incrementally brighten the screen before a channel is displayed.
time_bri_rate = 30         # Rate (steps/second) to incrementally brighten the screen before a channel is displayed.

###############################################################
# Define Functions
###############################################################
# Determine the duration of the mp4 files.
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "fatal", "-show_entries",
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
prog_end = []              # The time that a scheduled program should end
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
        print('Processing program: '+yy)
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
            
    # Determine when the scheduled program should end (seconds).
    temp_prog_end = []
    time_end = 0
    i = 0
    for yy in temp_prog_len:
        # Determine the time in seconds that a scheduled program should end.
        time_end = time_end + temp_prog_len[i]
        temp_prog_end.append(time_end)
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
        prog_end.append(temp_prog_end[i])
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
prog_time_end = [100] # Sets the scheduled end time for the program to a dummy starting value, this will become the expected time (seconds) that the program is scheduled to end.
while x < 1200:
    # Wait the specified amount of time between taking potentiometer readings.
    time.sleep(time_delay_sensor)
    
    # Get the current programming time (seconds).
    time_sec = datetime.now() - time_start
    time_sec = time_sec.total_seconds()
    
    # Get the potentiometers' readings.
    #print('\n==================Potentiometer Reading==================')
    pot0 = MCP3008(channel = 0)
    #print('Pot 0:',round(pot0.value,2))
    pot1 = MCP3008(channel = 1)
    #print('Pot 1:',round(pot1.value,2))
    pot2 = MCP3008(channel = 2)
    #print('Pot 2:',round(pot2.value,2))
    x += 1
    
    # Make brightness adjustments.
    bri = round(pot0.value,2)
    bri_command = 'xrandr --output HDMI-1 --brightness '+str(bri)
    os.system(bri_command)
    
    # Make volume adjustments.
    vol = round(pot1.value*100,0)
    vol_command = 'amixer set Master ' + str(int(vol)) + '%'
    os.system(vol_command)
    
    # Determine which channel is currently selected.
    channel_curr = int(round(pot2.value/(1/12)+1,0)) # There are 13 channels, so which potentiometer reading is most close to a channel. This will give values 1 to 13
    
    # Determine if it is time for the next program on the same channel.
    next_prog = False
    if(prog_time_end[0] < (time_sec+0.5)): # If it is about time for the scheduled program to end, then begin playing the next program.
        next_prog = True
        channel_curr = 0 # To trigger the next program to play, set the channel to 0. 
    
    # Determine if channel should be changed.
    if channel_curr != channel_prev:
        print('Channel changed from '+str(channel_prev)+' to '+str(channel_curr))
        # Set the brightness to 0.
        os.system('xrandr --output HDMI-1 --brightness 0.2')
        
        # Stop the current program.
        os.system('killall -9 vlc') # Stops the player from playing
        os.system('rm -r temp.sh')  # Prevents the player.py from replaying the same movie. 
        
        # If it is time to play the next program on the same channel, then reset to the same channel.
        if next_prog == True:
            next_prog = False
            channel_curr = channel_prev
        
        # Check that the channel has not been changed for xxx seconds, this makes sure that it does not skip to just the first channel 
        change_time1 = datetime.now()
        change_time2 = datetime.now()
        time_sec2 = change_time2-change_time1
        while time_sec2.total_seconds() < time_delay_channel_input:
            time.sleep(0.1)
            pot2 = MCP3008(channel = 2)
            channel_curr2 = int(round(pot2.value/(1/12)+1,0))
            if(channel_curr2 != channel_curr): # If the channel has changed, then reset the change_time1 to make the process start the timer again
                #print(channel_curr)
                #print(channel_curr2)
                channel_curr = channel_curr2
                change_time1 = datetime.now()
                print('Channel change detected again')
            change_time2 = datetime.now()
            time_sec2 = change_time2-change_time1
            print('Waiting to confirm channel')
        print('Channel confirmed')
        
        # Determine which channel directory corresponds with the inputted channel number.
        temp = str(channel_curr).rjust(2,'0')
        prog_channel_curr = [match for match in channels if temp in match] # The input channel will be a number, like 2, so this will find any directories that have 02 in them, the first one that matches will be considered the channel to play.
        
        # Determine which program should start.
        i = 0
        prog_i = 0
        play = False
        prog_dir_curr = []
        prog_time_start = []
        prog_time_end = []
        # Determin the list of programs that could be played -- all programs from that channel that are are supposed to be aired before the current time (seconds).
        for yy in prog:
            if prog_channel_curr[0] == prog_channel[i]:
                if(prog_after_start[i] < (time_sec+time_delay_channel)): # Should the show have already started?
                    if(prog_end[i] > time_sec):     # Should the program still be playing?
                        prog_dir_curr.append(prog_dir[i]) # Save the directory for the current program
                        prog_time_start.append(max(0,time_sec - prog_after_start[i]))          # Save the time that the video should begin playing from
                        prog_time_end.append(prog_end[i]) # Record the time that the program is expected to end.
                        prog_i = i                        # Record which program should be played.
                        play = True # Indicate that a program has been found.
            i += 1
        
        # Start the next program if there is one found.
        if play == True:
            # Begin playing the program.
            chan_command = 'vlc '+prog_dir_curr[0]+' --video-on-top --start-time='+str(prog_time_start[0])
            with open("temp.sh", "w") as job_file:
                job_file.write("#!/bin/bash\n")
                job_file.write(chan_command)
                
            # Indicate to the player script that it should begin playing the program.
            with open("player-on.txt", "w") as job_file:
                job_file.write(str(datetime.now()))
                
            # Wait the specified time to allow VLC player to boot up the program.
            time.sleep(time_delay_channel)
            
            # Ramp up the brightness for the number of steps and rate. 
            # Determine how many brightness steps there should be.
            bri_num_step = list(range(0,time_bri_steps*time_bri_rate+1))
            # Determine where the brightness should start and end at.
            bri_low = 0.2
            bri_high = max(bri,0.0001)
            # Determine how bright each step should be.
            bri_step = (bri_high - bri_low)/(time_bri_steps*time_bri_rate)
            # Determine how long to wait between steps.
            bri_wait = time_bri_steps/(time_bri_steps*time_bri_rate)
            for yy in bri_num_step:
                bri_step_command = 'xrandr --output HDMI-1 --brightness '+str(bri_low + (bri_step*yy))
                #print(bri_step_command)
                os.system(bri_step_command)
                time.sleep(bri_wait)
            play = False
    channel_prev = channel_curr
    
    




