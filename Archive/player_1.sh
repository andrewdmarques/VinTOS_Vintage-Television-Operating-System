#!/bin/bash
sleep 10
while :
do
	sleep 0.1
	FILE=/home/andrewdmarques/Desktop/TV/player-on.txt
	if [ -f "$FILE" ]; then
		sudo rm -r /home/andrewdmarques/Desktop/TV/player-on.txt
		FILE=/home/andrewdmarques/Desktop/TV/temp.sh
		if [ -f "$FILE" ]; then
			chmod +x /home/andrewdmarques/Desktop/TV/temp.sh
			# export DISPLAY=HDMI-1
			# bash /home/andrewdmarques/Desktop/TV/temp.sh > /home/andrewdmarques/Desktop/TV/bash_log.text 2>&1
			# su -c /home/andrewdmarques/Desktop/TV/temp.sh andrewdmarques > /home/andrewdmarques/Desktop/TV/bash_log.text 2>&1
			#su -c /home/andrewdmarques/Desktop/TV/temp.sh andrewdmarques
			runuser -l andrewdmarques -c '/home/andrewdmarques/Desktop/TV/temp.sh' > /home/andrewdmarques/Desktop/TV/bash_log.text 2>&1
		fi
	fi
done

