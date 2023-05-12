#!/bin/bash
sleep 1
while :
do
	sleep 0.1
	FILE=/home/andrewdmarques/Desktop/TV/Bin/Scripts/player-on.txt
	if [ -f "$FILE" ]; then
		rm -r /home/andrewdmarques/Desktop/TV/Bin/Scripts/player-on.txt
		FILE=/home/andrewdmarques/Desktop/TV/Bin/Scripts/temp.py
		if [ -f "$FILE" ]; then
			chmod +x /home/andrewdmarques/Desktop/TV/Bin/Scrripts/temp.py
			# export DISPLAY=HDMI-1
			python3 /home/andrewdmarques/Desktop/TV/Bin/Scripts/temp.py > /home/andrewdmarques/Desktop/TV/Bin/Log-Files/bash_log.text 2>&1
			# su -c /home/andrewdmarques/Desktop/TV/Bin/Scripts/temp.sh andrewdmarques > /home/andrewdmarques/Desktop/TV/bash_log.text 2>&1
			#su -c /home/andrewdmarques/Desktop/TV/Bin/Scripts/temp.sh andrewdmarques
			# runuser -l andrewdmarques -c '/home/andrewdmarques/Desktop/TV/Bin/Scripts/temp.sh' > /home/andrewdmarques/Desktop/TV/Bin/Scripts/bash_log.text 2>&1
		fi
	fi
done

