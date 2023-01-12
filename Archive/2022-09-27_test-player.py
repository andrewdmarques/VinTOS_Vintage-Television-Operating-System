prog_time_start = [4.2]
with open("temp.py", "w") as job_file:
    job_file.write("#!/usr/bin/python3\n")
    job_file.write("import os\n")
    #job_file.write("media = '"+prog_dir_curr[0]+"'\n")
    job_file.write("os.system('DISPLAY=:0 vlc /media/andrewdmarques/UNTITLED/TV/Channels/01_Science/Arteries1941.mp4 --start-time="+str(prog_time_start[0])+"')")
    
# Indicate to the player script that it should begin playing the program.
with open("player-on.txt", "w") as job_file: # xhost + local: # to give the permissions
    job_file.write(str('datetime.now()'))
