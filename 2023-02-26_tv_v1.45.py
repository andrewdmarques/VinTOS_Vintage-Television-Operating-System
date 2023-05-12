#!/usr/bin/python3
# import the libraries.
from gpiozero import MCP3008   # To interpret the potentiometers when using a raspberry pi
import serial                  # To interpret the potentiometers when using an arduino
import time                    # To allow for gaps in time before going through the while loop again.
from datetime import datetime, timedelta  # To get time and make the tv program list
import os                      # To get the directories that are present
import subprocess              # To determine the lengths of each of the programs
import pandas as pd            # To save the program schedules as csv files. sudo apt-get install python3-pandas
import random                  # To randomize the programs when making a list.
from pandas import *           # To read in the program schedule.
import math                    # To help with determining the channel for the potentiometer.

###############################################################
#User input variables.
######################v#########################################
dir_channels = '/home/andrewdmarques/Desktop/TV/Channels' # This is the location that the data is stored.
dir_os = '/home/andrewdmarques/Desktop/TV/Bin' # Location of the bin, scripts, and files needed to run the operating system.
dir_default = '/home/andrewdmarques/Desktop/TV/Channels/03_Tucker-Documentary-1/' # This is the directory that, if the arduino is not detected, will then be played by default.
time_delay_sensor = 0.05    # Time (seconds) to pause before checking the potentiometer inputs.
time_delay_channel_input=2  # Time (seconds) to pause before committing to changing the channel.
time_delay_channel = 2      # Time (seconds) to allow for transition before playing the program after a channel change or a program ends.
time_bri_steps = 4          # Time (seconds) to incrementally brighten the screen before a channel is displayed.
vol_max = 0.9               # Volume (proportion of max) to limit the volume to. If potentiomter reads 100 and vol_max is 0.6, then it will be scaled to 60%.
bri_min = 0.0               # The minimum brightness (0-1).
board = 'ard'               # Indicate where the hardware set up has the potentiometer being read by 'pi' for raspberry pi or 'ard' for arduino.
ard_path = '/dev/ttyACM0'   # The port that the arduino will communicate with. If a reaspberry pi is used, then this will take any value.
tv_on_file = '/home/andrewdmarques/Desktop/TV/Bin/Scripts/tv-on.txt' # The file that, if deleted, will allow the script to be stopped.
sched_count = 10            # Number of new schedules to generate that will be randomly pulled from.
prog_min = 36               # Time (hours) that the minimum playlist length should be made.
time_reboot = 23.9          # Time (hours) that the program will run before automatically forcing a reboot. ***This should be at least several hours shorter than prog_min
make_new_schedule = not bool(os.listdir(dir_os+'/Program-Schedule/'))  # Make new schedules set as True or False depending on if the direcotry is empty.

time.sleep(20)
os.system('pulseaudio -D')

###############################################################
# Define Functions
###############################################################

# function for playing a video through player.sh.
def play_video(dir_os,pdc,pts,tt):
    # Begin playing the program.
    with open(dir_os + "/Scripts/temp.py", "w") as job_file:
        job_file.write("#!/usr/bin/python3\n")
        job_file.write("import os\n")
        #job_file.write("media = '"+prog_dir_curr[0]+"'\n")
        # Set the start time to play the video a little early.
        pts = max(pts-5,0) # sets the program start time to either 0 or 5 seconds early 
        job_file.write("os.system('DISPLAY=:0 vlc " + pdc + " --video-wallpaper --qt-start-minimized --start-time="+str(pts)+"')")
    # Indicate to the player script that it should begin playing the program.
    with open(dir_os + "/Scripts/player-on.txt", "w") as job_file: # xhost + local: # to give the permissions
        job_file.write(str(tt))
#play_video(dir_os,prog_dir_curr[0],prog_time_start[0],datetime.now())
        
# Function for getting potentiomter readings if using a Raspberry Pi.
if board == 'pi':
    def get_pot():
        numbers = [str(MCP3008(channel = 0)),str(MCP3008(channel = 1)),str(MCP3008(channel = 2))]
        pot0, pot1, pot2 = map(int,numbers)
        numbers2 = [pot0*100, pot1*100, pot2*100]
        return numbers2

# Function for getting potentiomter readings if using an arduino.
if board == 'ard':
    # The arduino must be connected for this to continue.
    if os.path.exists(ard_path):
        # set up the serial connection to the Arduino
        ser = serial.Serial(ard_path, 9600)
        time.sleep(2) # wait for the Arduino to reset
        def get_pot():
            # send a command to the Arduino to read the potentiometer values
            ser.write(b'r')
            
            # read the response from the Arduino
            response = ser.readline().decode().strip()
            values = response.split(',')
            
            # check if we received the expected number of values
            if len(values) != 3:
                raise ValueError("Expected 3 values, but received {}".format(len(values)))
            
            # normalize the values and return them as a list
            pots = [round(int(val) / 1023 * 100) for val in values]
            return pots
    else:
        print('arduino not connected')

# Function to determine the duration of the mp4 files.
def get_length(filename):
    time_out = os.popen("mediainfo --Inform='Video;%Duration/String3%' " + filename).read()
    time_out1 = time_out.split('.', 1)[0]
    time_out_sec = sum(int(x) * 60 ** i for i, x in enumerate(reversed(time_out1.split(':'))))
    time_out_sec = float(time_out_sec) + float('.'+time_out.split('.', 1)[1].strip())
    time_out_sec
    return float(time_out_sec)

# Function for generating the program schedule.
def get_schedule(time_start,dir_channels,dir_os,sn,prog_min,time_delay_channel):
    # Initialize the lists to record the scheduled programming.
    prog_channel = []          # The channel that the program is played on
    prog = []                  # The program file name
    prog_dir = []              # The program file and directory name
    prog_len = []              # The length of the program in seconds
    prog_end = []              # The time that a scheduled program should end
    prog_after_start = []      # The time since start that the program should begin in seconds
    prog_time = []             # The time that the program should begin playing
    prog_min_sec = prog_min * 60 * 60 # 60 seconds in a minute and 60 minutes in an hour
    # Get the channels and programs to play.
    channels = os.listdir(dir_channels)
    channels.sort()
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
        # Determine when the scheduled program should end (seconds).
        temp_prog_end = []
        time_end = 0
        i = 0
        for yy in temp_prog_len:
            # Determine the time in seconds that a scheduled program should end.
            time_end = time_end + temp_prog_len[i]
            temp_prog_end.append(time_end)
            i += 1
            
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
                temp_prog_after_start.append(temp_prog_end[i-1])
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
        # While the program schedule is less than the minimum time limit, keep appending the existing content until the time is met.
        temp_last_time = temp_prog_end[-1]
        while temp_last_time < prog_min_sec:
            i = 0
            for yy in temp_prog:
                prog_channel.append(temp_prog_channel[i])
                prog.append(temp_prog[i])
                prog_dir.append(temp_prog_dir[i])
                prog_len.append(temp_prog_len[i])
                prog_end.append(prog_end[-1]+temp_prog_len[i])
                prog_after_start.append(prog_end[-2])
                prog_time.append(prog_time[-1] + timedelta(seconds=prog_end[-1]))
                temp_last_time = prog_end[-1]+temp_prog_len[i]
                i += 1
    # Make a dictionary.
    dict1 = {'prog_channel':prog_channel,'prog':prog,'prog_dir':prog_dir,'prog_len':prog_len,'prog_end':prog_end,'prog_after_start':prog_after_start,'prog_time':prog_time}
    # Creating a dataframe.
    df = pd.DataFrame(dict1)
    # Conver dataframe to csv.
    data = df.to_csv(dir_os+'/Program-Schedule/schedule_'+str(sn)+'.csv', index = False)

# Function to determine which channel is selected:
def get_channel(num):
    lookup_table = {
        (0, 3): 3,
        (3, 12): 4,
        (12, 23): 5,
        (23, 33): 6,
        (33, 44): 7,
        (44, 55): 8,
        (55, 65): 9,
        (65, 75): 10,
        (75, 85): 11,
        (85, 95): 12,
        (95, 100): 13
    }
    for key, value in lookup_table.items():
        if key[0] <= num <= key[1]:
            return value

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
        get_schedule(time_start,dir_channels,dir_os,sn,prog_min,time_delay_channel)

# Randomly select one of the premade program schedules to run.
# Determine which schedules are available.
sched_list = os.listdir(dir_os+'/Program-Schedule')
random.shuffle(sched_list) # Randomly shuffle the schedules, then we will pick the first in this randomized list.
sched = sched_list[0]

# Make sure there is a location where the error logs can be written.
path = dir_os + "/Log-Files/"
if not os.path.exists(path):
    os.makedirs(path)

# Open the randomly selected schedule.
df = pd.read_csv(dir_os+'/Program-Schedule/'+sched)
data = read_csv(dir_os+'/Program-Schedule/'+sched)
prog_channel = data['prog_channel'].tolist()      # The channel that the program is played on
prog = data['prog'].tolist()                      # The program file name
prog_dir = data['prog_dir'].tolist()              # The program file and directory name
prog_len = data['prog_len'].tolist()              # The length of the program in seconds
prog_end = data['prog_end'].tolist()              # The time that a scheduled program should end
prog_after_start = data['prog_after_start'].tolist()      # The time since start that the program should begin in seconds
prog_time = data['prog_time'].tolist()

x = 1
prog_time_end = [100] # Sets the scheduled end time for the program to a dummy starting value, this will become the expected time (seconds) that the program is scheduled to end.
prog_time_end_hold = 100
# Get the channels and programs to play.
channels = os.listdir(dir_channels)

# tv-on.txt must be present for the for loop to work. This is one of the fail safes -- delete this 
tv_on = os.path.exists(tv_on_file)
if tv_on == False:
    print('TV program set to stop because tv-on.txt file is not present at location ' + str(tv_on_file))

# If the arduino is disconnected, then move to defauly mode.
if board == 'ard':
    if not os.path.exists(ard_path):
        tv_on = False
        print('TV program set to default mode because arduino is disconnected')

# Determine the starting channel (this will be labeled the "previous channel").
if tv_on == True:
    pots = get_pot()
    pot2 = pots[2]
    print('retrieved pot 2 before running script')
    channel_prev = 0 # Set the previous channel to 0 so that it will initialize the first time through the main loop.

# Refresh the current time.
time_start = datetime.now()

###############################################################
# Main script
###############################################################
print('Executing main script')

while True == tv_on: # If tv_on is false, then tv-on.txt is not present and the script should not be executed.
    # Wait the specified amount of time between taking potentiometer readings.
    time.sleep(time_delay_sensor)
    # tv-on.txt must be present for the for loop to work. This is one of the fail safes -- delete this 
    tv_on = os.path.exists(tv_on_file)
    if tv_on == False:
        print('TV program set to stop because tv-on.txt file is not present at location ' + str(tv_on_file))
    # Get the current programming time (seconds).
    time_sec = datetime.now() - time_start
    time_sec = time_sec.total_seconds()
    # For computer health, reboot the television at least once a day
    if(time_sec > (time_reboot*60*60)): # This will reboot about 23 hours and 59 minutes into the running session (time in seconds calulcated here)
        os.system('sudo reboot')
    # Get the potentiometers' readings.
    print('\n==================Potentiometer Reading==================')
    pots = get_pot()
    pot0 = pots[0]
    print('Pot 0:',round(pot0,2))
    pot1 = pots[1]
    print('Pot 1:',round(pot1,2))
    pot2 = pots[2]
    print('Pot 2:',round(pot2,2))
    x += 1
    # Make brightness adjustments.
    bri = round(pot0/100,2)
    bri_command = 'DISPLAY=:0 xrandr --output HDMI-1 --brightness '+str(bri)
    os.system(bri_command)
    # Make pactl -- set-sink-pactl set-sink-volume @DEFAULT_SINK@ 1  adjustments.
    vol = round(pot1*vol_max,0)
    vol_command = 'pactl set-sink-volume @DEFAULT_SINK@ ' + str(int(vol)) + '%'
    os.system(vol_command)
    # Determine which channel is currently selected.
    channel_curr = get_channel(pot2) # There are 11 channels, so which potentiometer reading is most close to a channel. This will give values 2 to 12
    # Determine if it is time for the next program on the same channel.
    next_prog = False
    if((time_sec+0.2) > prog_time_end_hold): # If it is about time for the scheduled program to end, then begin playing the next program.
        #if((time_sec) > prog_time_end[0]): # If it is about time for the scheduled program to end, then begin playing the next program.
        time.sleep(0.21)
        # Get the current programming time (seconds).
        time_sec = datetime.now() - time_start
        time_sec = time_sec.total_seconds()
        next_prog = True
        channel_curr = 0 # To trigger the next program to play, set the channel to 0.
    # Determine if channel should be changed.
    if channel_curr != channel_prev:
        print('Channel changed from '+str(channel_prev)+' to '+str(channel_curr))
        # Set the brightness to 0.
        os.system('DISPLAY=:0 xrandr --output HDMI-1 --brightness '+str(bri_min))
        # Stop the current program.
        os.system('killall -9 vlc') # Stops the player from playing
        os.system('rm -r ' + dir_os + '/Scripts/temp.py')  # Prevents the player.py from replaying the same movie.
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
            pots = get_pot()
            pot2 = pots[2]
            channel_curr2 = get_channel(pot2)
            if(channel_curr2 != channel_curr): # If the channel has changed, then reset the change_time1 to make the process start the timer again
                print(channel_curr)
                print(channel_curr2)
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
        # Get the current programming time (seconds).
        time_sec = datetime.now() - time_start
        time_sec = time_sec.total_seconds()
        # For computer health, reboot the television at least once a day
        if(time_sec > (time_reboot*60*60)): # This will reboot about 23 hours and 59 minutes into the running session (time in seconds calulcated here)
            os.system('sudo reboot')
        # Determine which program should start.
        i = 0
        prog_i = 0
        play = False
        prog_dir_curr = []
        prog_time_start = []
        prog_time_end = []
        # Determine the list of programs that could be played (all programs from that channel that are supposed to be aired before the current time (seconds)).
        print(prog_channel[i])
        print(time_sec)
        for yy in prog:
            if prog_channel_curr[0] == prog_channel[i]:
                #print('got channel')
                if(prog_after_start[i] <= time_sec): # Should the show have already started?
                    #print('got start time')
                    if(prog_end[i] > time_sec):     # Should the program still be playing?
                        #print('got end time')
                        prog_dir_curr.append(prog_dir[i]) # Save the directory for the current program
                        prog_time_start.append(max(0,time_sec - prog_after_start[i]) - (time_delay_channel*3))          # Save the time that the video should begin playing from: This is adjusted by the time delay *3 so that it guarentees somethinhg plays before the channel change finishes
                        prog_time_end.append(prog_end[i]) # Record the time that the program is expected to end.
                        prog_i = i                        # Record which program should be played.
                        prog_time_end_hold = prog_time_end[0] # This is in the loop to ensure that the time a program should end is held constant and not overwritten as blank so long as a channel end time has previosly been selected.
                        play = True # Indicate that a program has been found.
                        #print(i)
            i += 1
        # If there is not a program next, then play the static
        if play == False:
            play_video(dir_os,'/home/andrewdmarques/Desktop/TV/Bin/Backgounds/static.mov',0,datetime.now())
            
            # Wait the specified time to allow VLC player to boot up the program.
            # Get the current time.
            time_curr_channel0 = datetime.now()
            time_curr_channel1 = datetime.now() - time_curr_channel0
            time_curr_channel = time_curr_channel1.total_seconds()
            while time_curr_channel < time_delay_channel:
                time.sleep(0.1)
                # Check if enought time has passed.
                time_curr_channel1 = datetime.now() - time_curr_channel0
                time_curr_channel = time_curr_channel1.total_seconds()
                
                # Allow the volume to be changed while the brightness is ramping up.
                pots = get_pot()
                pot1 = pots[1]
                # Make volume adjustments.
                vol = round(pot1*vol_max,0)
                vol_command = 'pactl set-sink-volume @DEFAULT_SINK@ ' + str(int(vol)) + '%'
                print('In channel waiting loop')
                print(vol_command)
                os.system(vol_command)
            
            time.sleep(time_delay_channel)
            # Ramp up the brightness for the number of steps and rate.
            # Determine how many brightness steps there should be.
            bri_num_step = list(range(0,time_bri_steps*time_bri_rate+1))
            # Determine where the brightness should start and end at.
            bri_low = bri_min
            bri_high = max(bri,0.0001)
            # Determine how bright each step should be.
            bri_step = (bri_high - bri_low)/(time_bri_steps*time_bri_rate)
            # Determine how long to wait between steps.
            bri_wait = time_bri_steps/(time_bri_steps*time_bri_rate)
            for yy in bri_num_step:
                bri_step_command = 'DISPLAY=:0 xrandr --output HDMI-1 --brightness '+str(bri_low + (bri_step*yy))
                #print(bri_step_command)
                os.system(bri_step_command)
                time.sleep(bri_wait)
                
                # Allow the volume to be changed while the brightness is ramping up.
                pots = get_pot()
                pot0 = pots[0]
                print('Pot 0:',round(pot0,2))
                pot1 = pots[1]
                # Make volume adjustments.
                vol = round(pot1*vol_max,0)
                vol_command = 'pactl set-sink-volume @DEFAULT_SINK@ ' + str(int(vol)) + '%'
                os.system(vol_command)
            play = False
        # Start the next program if there is one found.
        if play == True:
            play_video(dir_os,prog_dir_curr[0],prog_time_start[0],datetime.now())
            
            # Wait the specified time to allow VLC player to boot up the program.
            # Get the current time.
            time_curr_channel0 = datetime.now()
            time_curr_channel1 = datetime.now() - time_curr_channel0
            time_curr_channel = time_curr_channel1.total_seconds()
            while time_curr_channel < time_delay_channel: # While loop for confirming the selected channel.
                time.sleep(0.1)
                # Check if enought time has passed.
                time_curr_channel1 = datetime.now() - time_curr_channel0
                time_curr_channel = time_curr_channel1.total_seconds()
                
                # Allow the volume to be changed.
                pots = get_pot()
                pot1 = pots[1]
                # Make volume adjustments.
                vol = round(pot1*vol_max,0)
                vol_command = 'pactl set-sink-volume @DEFAULT_SINK@ ' + str(int(vol)) + '%'
                print('In channel waiting loop')
                print(vol_command)
                os.system(vol_command)
                
            # Ramp up the brightness for the number of steps and rate.
            tb = datetime.now()
            time_bri_1 = (datetime.now() - tb).total_seconds()
            bri_low = bri_min
            bri_high = max(bri,0.0001)
            while time_bri_1 < time_bri_steps: # While loop for ramping up brightness.
                # Prepare for next loop.
                time.sleep(0.05)
                time_bri_1 = (datetime.now() - tb).total_seconds()
                
                # Determine the proportion of the ramp up time that has passed.
                bri_prop = time_bri_1/time_bri_steps
                # Calculate the current ramped up brightness base on time time in this loop.
                pot0 = pots[0]
                bri_level = max(0.0001,((round(pot0/100,2))*bri_prop))
                bri_step_command = 'DISPLAY=:0 xrandr --output HDMI-1 --brightness '+str(bri_level)
                #print(bri_step_command)
                os.system(bri_step_command)
                
                # Allow the volume to be changed while the brightness is ramping up.
                pots = get_pot()
                pot1 = pots[1]
                # Make volume adjustments.
                vol = round(pot1*vol_max,0)
                vol_command = 'pactl set-sink-volume @DEFAULT_SINK@ ' + str(int(vol)) + '%'
                print('In ramp up loop')
                print(vol_command)
                os.system(vol_command)
                
                # Check if the channel has been changed.
                pot2 = pots[2]
                channel_curr2 = get_channel(pot2)
                if(channel_curr2 != channel_curr): 
                    time_bri_1 = time_bri_steps # This breaks the loop.
                    channel_curr = 0            # This initiates a channel change.
            play = False
    channel_prev = channel_curr



# Move to default mode if an arduino is indicated as connected but it is disconnected.
if board == 'ard':
    if not os.path.exists(ard_path):
        video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']
        # Set default brightness and volume to max.
        os.system('DISPLAY=:0 xrandr --output HDMI-1 --brightness 1')
        os.system('pactl set-sink-volume @DEFAULT_SINK@ ' + str(int(vol_max*100)) + '%')
        tv_on = os.path.exists(tv_on_file)
        while True == tv_on: # While the tv-on.txt file is present, continue playing the video.
            tv_on = os.path.exists(tv_on_file)
            time.sleep(0.1)
            # Check that vlc player is not running already.
            for filename in os.listdir(dir_default):
                # Determine the filepath to the video that should be played.
                filepath = dir_default+filename
                print(filepath) 
                # Determine if the file is a video that should be played.
                ext = os.path.splitext(filename)[1].lower()
                if ext in video_extensions:
                    # Determine how long the video is.
                    default_time = get_length(filepath)
                    dt = datetime.now()
                    default_curr = (datetime.now() - dt).total_seconds()
                    time.sleep(1)
                    # Stop any ongoing videos.
                    os.system('killall -9 vlc')
                    time.sleep(2)
                    # Initiate the video to be played.
                    play_video(dir_os,filepath,0,datetime.now())
                    # Wait while the video is being played.
                    while default_curr < default_time:
                        time.sleep(1)
                        default_curr = (datetime.now() - dt).total_seconds()
                        print('vlc playing')
                        # Check that the script should continue running.
                        tv_on = os.path.exists(tv_on_file)
                        if tv_on == False:
                            break
                            # Get the current programming time (seconds).
                        time_sec = datetime.now() - time_start
                        time_sec = time_sec.total_seconds()
                        # For computer health, reboot the television at least once a day
                        if(time_sec > (time_reboot*60*60)): # This will reboot about 23 hours and 59 minutes into the running session (time in seconds calulcated here)
                            os.system('sudo reboot')
                    if tv_on == False:
                        break
    os.system('killall -9 vlc')
