#!/usr/bin/python3
import os
import time 
from os.path import exists

while True == True:
    time.sleep(0.1) # Pause just to the processors a break
    if exists('/home/andrewdmarques/Desktop/TV/player-on.txt'):
        os.system('rm -r /home/andrewdmarques/Desktop/TV/player-on.txt')
        if exists('/home/andrewdmarques/Desktop/TV/temp.sh'):
            time.sleep(0.1) # Pause to allow the text to be finished writting
            os.system('sudo chmod +x /home/andrewdmarques/Desktop/TV/temp.sh')
            os.system('bash /home/andrewdmarques/Desktop/TV/temp.sh')
            # time.sleep(1) # Pause to prevent the video from being played immediately after something has closed it.
    