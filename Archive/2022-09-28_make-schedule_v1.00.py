#!/usr/bin/python3
# import the libraries.
from gpiozero import MCP3008   # To interpret the potentiometers
import time                    # To allow for gaps in time before going through the while loop again.
from datetime import datetime, timedelta  # To get time and make the tv program list
import os                      # To get the directories that are present
import subprocess              # To determine the lengths of each of the programs
import pandas as pd            # To save the program schedules as csv files. sudo apt-get install python3-pandas
import random                  # To randomize the programs when making a list.
from pandas import *           # To read in the program schedule.

###############################################################
#User input variables.
######################v#########################################
dir_channels = '/media/andrewdmarques/FLASHDRIVE/TV/Channels' # This is the location that the data is stored.
dir_os = '/home/andrewdmarques/Desktop/TV'
time_delay_sensor = 0.0005  # Time (seconds) to pause before checking the potentiometer inputs.
time_delay_channel_input=2  # Time (seconds) to pause before committing to changing the channel.
time_delay_channel = 10.5   # Time (seconds) to allow for transition before playing the program after a channel change or a program ends.
time_bri_steps = 4          # Time (seconds) to incrementally brighten the screen before a channel is displayed.
time_bri_rate = 30          # Rate (steps/second) to incrementally brighten the screen before a channel is displayed.
make_new_schedule = True    # Make new schedules.
sched_count = 10             # Number of new schedules to generate that will be randomly pulled from.
bri_min = 0.0               # The minimum brightness (0-1).  

###############################################################
# Define Functions
###############################################################
# Determine the duration of the mp4 files.
def get_length(filename):
    time_out = os.popen("mediainfo --Inform='Video;%Duration/String3%' " + filename).read()
    time_out1 = time_out.split('.', 1)[0]
    time_out_sec = sum(int(x) * 60 ** i for i, x in enumerate(reversed(time_out1.split(':'))))
    time_out_sec = float(time_out_sec) + float('.'+time_out.split('.', 1)[1].strip())
    time_out_sec
    return float(time_out_sec)

###############################################################
# Initialization
###############################################################
# Get the current time
time_start = datetime.now()

# Make new schedules if directed.
if make_new_schedule == True:

    # Make a new directory if it doesn't already exist.
    isExist = os.path.exists(dir_os+'/Program-Schedule')
    if not isExist: 
      os.makedirs(dir_os+'/Program-Schedule')
    sched_num = list(range(0,sched_count,1))
    for sn in sched_num:
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
            random.shuffle(temp_prog) # This line randomizes the lists when making the schedule for each program.
            
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
        # Make a dictionary.
        dict1 = {'prog_channel':prog_channel,'prog':prog,'prog_dir':prog_dir,'prog_len':prog_len,'prog_end':prog_end,'prog_after_start':prog_after_start,'prog_time':prog_time}
        
        # Creating a dataframe.
        df = pd.DataFrame(dict1)
        
        # Conver dataframe to csv.
        data = df.to_csv(dir_os+'/Program-Schedule/schedule_'+str(sn)+'.csv', index = False)
