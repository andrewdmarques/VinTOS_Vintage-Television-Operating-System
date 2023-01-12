#!/usr/bin/python3
# import the libraries.
from gpiozero import MCP3008   # To interpret the potentiometers
import time                    # To allow for gaps in time before going through the while loop again.
from datetime import datetime, timedelta  # To get time and make the tv program list
import os                      # To get the directories that are present
import subprocess

while True == True:
    time.sleep(0.2)
    pot2 = MCP3008(channel = 2)
    #channel_curr = round(12.25-(pot2.value/(1/10)+1),0)
    #channel_curr = round(pot2.value,2)
    channel_curr = round(12.25-(pot2.value/(1/10)),1)
    print(channel_curr)
            