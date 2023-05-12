# Vintage

# **Television**

# **Operating**

#**System**

Contact: Andrew D. Marques

Website: www.AndrewDMarques.com

Version: 7

Updated: 4/13/2023

##**Introduction**

This manual serves as a comprehensive guide for using and maintaining the television set. While it covers the hardware build process, the primary focus is on the accompanying software, Vintage Television Operating System (VINTOS). VINTOS is an operating system designed to "reanimate" vintage tube television sets for use in modern applications.

For television sets that are beyond economical repair, VINTOS provides a viable solution to give them new life. It populates the shell of the vintage set to emulate any preferred television or film period. VINTOS aims to retain the original functionality of the unit for power, channel, volume, and brightness controls.

Each channel that the owner selects can be dedicated to specific types of content. For example, channel 1 may be dedicated to 1950's period sitcoms, channel 2 to the owner's private 8mm home film collection, channel 3 to 1940s movies, and so on. Alternatively, each channel could be set to specific content for a museum exhibit.

Operation Modes:

1.  **Front Mode**: Control the television using original knobs located in the front of the cabinet.
2.  **Internal Mode**: Control the television using the internal knobs while disabling the front knobs.
3.  **Default Mode**: Disable all front and internal knobs. Only play content from the first channel by default with no knob controls to change channels, volume, or brightness.

For use in museums, a "curator override" system can be added to disable front knobs and provide control through an internal set of knobs. A "default" mode is also available to disable all knob inputs and play the content of channel 1 on repeat in case of issues with the front or internal knobs.

The cabinet used in this project is an RCA 6-T-76 with a 16" black and white TV and a maple cabinet built between 1949-1951. The updated set includes a Samsung S24D360HL monitor, JBL Platinum Series SP08A11 speakers, an Arduino UNO REV3 microcontroller board, and a Lenovo ThinkCentre M93p i5-4570T 2.90GHz 8GB RAM 250GB SSD main computer.

A video describing the finished product can be found at this link: <https://photos.app.goo.gl/2rV23QRDTUTvKgD26>.

Together, this modified cabinet and VINTOS software provide an immersive viewing experience that simulates interactive vintage television.

##**Quickstart Guide**

**Operating Steps**:

1.  Plug in the television.
2.  Wait approximately 1 minute for the system to boot up.
3.  Control of the TV depends on which mode is running:
    1.  **Front mode** (front controls activated)
        1.  Power the monitor, speaker, and indicator light with the front left-most knob.
        2.  Change screen brightness with the front's middle left knob.
        3.  Change volume with the front's middle right knob.
        4.  Change channels with the front's right-most knob.
    2.  **Internal mode** (internal controls activated, except power)
        1.  Power the monitor, speaker, and indicator light with the front left-most knob.
        2.  Change screen brightness with the internal top knob.
        3.  Change volume with the internal middle knob.
        4.  Change channels with the internal bottom knob.
    3.  **Default mode** (limit control of knobs)
        1.  Power the monitor, speaker, and indicator light with the front left-most knob.
        2.  Screen brightness will be set to max by default, no knob controls this.
        3.  Volume will be set to max by default, no knob controls this.
        4.  Channel will be set to play channel 1 content by default, no knob controls this.
4.  To disable the front left-most knob from powering on the monitor, speaker, and indicator light, the included surge protector could be used. All devices could be connected to this, bypassing the GFCI outlets. When connected to the surge protector, please disconnect the brown vintage cable. This is recommended for units to be displayed in museums.

**Change Modes:**

-   To activate **Front mode**:
    -   Connect Arduino plug to Arduino socket.
    -   Turn "internal control" switch to **OFF**.
    -   Reboot the system by disconnecting and reconnecting the main power and power cycle the Lenovo computer.
-   To activate **Internal mode**:
    -   Connect Arduino plug to Arduino socket.
    -   Turn "internal control" switch to **ON**.
    -   Reboot the system by disconnecting and reconnecting the main power and power cycle the Lenovo computer.
-   To activate **Default mode**:
    -   Disconnect Arduino plug from Arduino socket.
    -   Reboot the system by disconnecting and reconnecting the main power and power cycle the Lenovo computer.

**Adding New Programs:**

1.  Adding new programs is easy, begin by powering on the system.
2.  Use the included Keyboard/Trackpad.
3.  Press the "Windows" key and search for "Files".
4.  Insert a USB drive to the main computer that contains the video file (mp4 is preferred but most common video types are accepted).
5.  Select the files from the flashdrive you would like too add.
6.  Go to "/home/andrewdmarques/Desktop/TV/Channels" on the main computer and copy the selected files to the designated channel you would like to add them to.
7.  Disconnect the flashdrive.
8.  Generate a new set of program schedules.
    1.  Go to "/home/andrewdmarques/Desktop/TV/Bin/Program-Schedule/" and delete ALL the contents of this folder. All files should have been CSV files.
    2.  Disconnect and reconnect the main power supply to the cabinet.
    3.  This will automatically generate a new list of schedules that now include the added program.

**Moving the Cabinet:**

1.  Moving the cabinet should be done carefully -- first disconnect the main power.
2.  Unplug and remove the following devices, it is recommended to leave the wires in the cabinet.
    1.  Monitor
    2.  Main computer
    3.  Speakers
3.  The Arduino board should remain in the cabinet. It is recommended to secure the board using tape to not strain the jumper wires.
4.  Transport the cabinet in an upright position. You may want to secure the cabinet doors closed.
5.  After transporting the TV, plug in the devices and place the components back in their locations. See the images in this document for where the devices belong.
    1.  TIP: Make it so the bottom of the monitor is pressed as closely to the tan bakelite mount as possible.

**Long-Term Storage:**

1.  The cabinet should be stored in dry cool spaces without rodents. This cabinet should be thought of like a computer, so make sure that it is stored appropriately.
2.  Check the integrity of the wiring connections.
3.  The internal clock for the main computer may be reset if stored for more than a few weeks without power. You may have to manually input the time in the settings.
    1.  Open the Activities overview (press "Windows" button and start typing Settings.
    2.  Click on Settings.
    3.  Click Date & Time in the sidebar to open the panel.
    4.  If you have the Automatic Date & Time switch set to on, your date and time should update automatically if you have an internet connection. To update your date and time manually, set this to off.
    5.  Click Date & Time, then adjust the time and date.
    6.  You can change how the hour is displayed by selecting 24-hour or AM/PM for Time Format.

**Fast Facts:**

-   **System reboot:** For system health, it is recommended to power on and off the main power supply (not just the front knob) at least 1x a day. A fail safe is built into the software which will reboot the computer once a day. This will occur several minutes before the 24 hour mark before the last time it was turned on.
-   **System stopping/starting**: If you wish to stop the operating system and keep the computer running, while the system is rebooting press the "Windows" key and navigate to Desktop/TV/Bin/Scripts. At this location, delete "tv-on.txt". This will indicate to the system that it should stop immediately. If a video is already playing while this file is deleted, the video will continue to play. You can close the video's tab.
-   **Main computer power:** The main computer power will remain on even after the front power knob is turned off. This is because it stays running in the background for a seemingly instantaneous "on" experience when the front left-most knob is turned.
-   **On always outlets**: Two outlets will always have power sent to them, regardless of the state of the power knob.
-   **On with switch outlets**: 4 outlets will have power only when the front left-most knob is set to power.
-   **5A max**: Power consumption is limited to 5A maximum. This is controlled by a 5A circuit breaker.
-   **Plugging in other devices to GFCI outlets**: Do not use the empty outlets for powering non-TV related devices. This may overdraw current and trip the breaker.
-   **GFCI outlets:** GFCI outlets are used for non-grounded 3-pronged receptacles. This follows local and federal code. Electrical code 406.4(D)(2) Non-Grounding-Type Receptacles states that when replacing a non-grounding type receptacle with a GFCI type, the receptacle or the cover plate must be marked “No equipment ground”. It is recommended to test outlets 1x per month.
-   **Changing file locations:** It is not recommended to change file locations from their current directories. If this must be done, then the operating system code will need to be modified to have the correct locations.
-   **Channel directories:** The channel directories should be named with a "00_name" format, where "00" is a two-digit number and "name" can be anything without spaces or special characters. Non-video files should not be placed in these channel directories. All channels
-   **Wifi:** The computer is configured to connect to the internet, but it requires a wifi dongle (USB connector). For internet security reasons, and to prevent issues with updating popups, this should be left disconnected. If a wifi dongle is not included in your package, you can purchase one. It is recommended to use the following dongle: TP-Link TL-WN725N N150 150Mbps Wireless Nano USB WiFi Network Adapter Dongle.

##**Diagrams**![](media/10d09d62132669a40958c95fa41fbfe4.png)

The main electrical wiring diagram shown above can be used as a reference when troubleshooting if connections are not made to the appropriate devices.

![](media/83b2171f6cea1dd4f528ae2f2323716b.png)

The Arduino wiring diagram indicates how the jumper wires should be connected to the breadboard and controls. Remember to disconnect power before touching any cables. Failure to follow the diagram may result in dysfunctional connections or destruction of potentiometers by overheating.

![](media/be950dd162e1c6973ea985a39373a653.png)

The VINTOS file structure is shown above, and all relevant files are located on the Desktop. To run VINTOS, the potentiometer-reader.ino file must be uploaded to the Arduino, but a reference copy is kept in Desktop/TV/Bin/Scripts.

For proper organization, all mp4 files should be placed in their respective channel directories. The channel directories should be named with a "00_name" format, where "00" is a two-digit number and "name" can be anything without spaces or special characters. Non-video files should not be placed in these channel directories.

**File Descriptions:**

-   **tv-on.txt**: File that allows the tv script to run. Delete this file to prevent the script from playing. Make a file with this name to get it to play. The content of this file is not important, what matters is that there is a file with this name. File location: /home/andrewdmarques/Desktop/TV/Bin/Scripts/tv-on.txt
    -   ![](media/fe28708254f0c4a83ddcd84112e18208.png)
-   **player-on.txt**: File that allows the player.sh script to run. This file is automatically made by the tv.py script to indicate to player.sh that there is a new video to play i.e. the channel has changed or the computer is booting up for the first time. The contents of this script are written as the time that it was written. It will be deleted by the player.sh script once the video has begun playing. File location: /home/andrewdmarques/Desktop/TV/Bin/Scripts/player-on.txt
-   **tv.py**: The main script that controls volume, brightness, and indicates what video should be played. This coordinates the operation. When channel changes are prompted, it will write the temp.py script with the command to commence the vlc player, and generate the player-on.txt file to initiate the player.sh script to execute the command located in temp.py. File location: /home/andrewdmarques/Desktop/TV/Bin/Scripts/tv.py
    -   ![](media/9f350896dcf9254e2746a98de036cdf6.png)
-   **temp.py**: Script that contains the command to begin running the vlc player. It is created by the tv.py script and executed by the player.sh script. File location: /home/andrewdmarques/Desktop/TV/Bin/Scripts/temp.py
    -   ![](media/568d9425ff4e0a462fdc938fdae8aa89.png)
-   **player.sh**: An auxiliary script that waits for the cue to begin playing a new video. The queue to play a new video will be if player-on.txt is present. Once player.sh is activated, it will delete player-on.txt and run the command written in temp.py. File location: /home/andrewdmarques/Desktop/TV/Bin/Scripts/player.sh
    -   ![](media/6561ce1f0d8f0fb131384ce9cfa10379.png)
-   **schedule_\#.csv**: CSV file that is the program schedule. There are n number of program schedules and they are numbers schedule_0.csv, schedule_1.csv, etc. It includes information such as channel, the program on the channel, the file location of the program on that channel, the program length in seconds, the Location: /home/andrewdmarques/Desktop/TV/Bin/Program-Schedule/schedule_0.csv
    -   ![](media/be0dce41f27e4ed2ab84f69652469d25.png)

##**Build Documentation**

1/4/2023

![](media/3aa40bdc7295a88711d76e81c1c9b9f8.png)![](media/d8c9965eb73bd2cf60c0f9cfe1a91e13.png)

The cabinet of the original television set showed signs of age and water damage. It appears the television cabinet sat in about 1.5 feet of water at some point of its life. There was also extensive damage to the coating on the top and front cabinets.

![](media/b4bdf3635f58a86e19bab4bb0c9a2816.png)![](media/a2624161a9bc6b268899e26d08060acb.png)

More images of the front of the console with the cabinet door open shows the surface damage present on the unit.

![](media/00e368ad5be3bb51dd52052ada9ee100.png)![](media/a1ba52bd18c3cccbf4fd82776f4bb813.png)![](media/a60ed1f023034fc609be7ea8c0df2519.png)

The first two images show the cabinet before and after being cleaned and re-varnished. This illustrates the condition of damage. The third image shows the condition of the original electronics. There was some minor evidence of water damage, but there was clear damage from rodents. Evidence of rust from urine, and the presence of feces was found throughout the unenclosed locations. Rust did not appear on surfaces that could not be accessed by rodents.

1/10/2023

![](media/b6ac6c92dea306d11ba7caa323530cad.png)![](media/88466befb2619a72b167e5570721b381.png)![](media/921720b570ce55c83a21d4b5f585eaf2.png)

Above are the original electronics being removed. Some of these components will be cleaned and reused and others will be either disposed of responsibly, or made to be reused in other antique electronics.

1/14/2023![](media/cfd2c1d0871375b05aef89166c7d9b7a.png)

The cathode-ray tube was physically damaged and did not appear to be salvageable. It was placed at the Philadelphia waste department site for televisions.

1/15/2023

![](media/7e80e84a50883d5388235d371992da2e.png)![](media/6eee6ca62f3655226a0f9b63fdda4f7b.png)![](media/12b170bbd91d471bb1aedb06a8d013e7.png)

The tan bakelite mount that the cathode-ray tube mounts to had to be cut to fit the monitor. While being cut, the material appeared to melt while being cut, rather than simply being cut.

![](media/021daf7459cc55ea91f141bf792925fe.png)![](media/2039fe4a08da51d4073bfc9956787d43.png)

The board of this RCA television is attached to the potentiometer knobs. These must be cut from the main electronics board to maintain the position and sturdiness of the dial connections to the cabinet.

![](media/5a56fde0a359df9d00eb7e3ea344187d.png)![](media/6f64a35ba73f5d2323f4781de8f6dfc6.png)

The cuts show the portion of the main board that is kept.

1/17/2023

![](media/62d8582e24b7bf09674452cdc81c7af6.png)

A USB-powered LED light strip will be used as a light indicator. This will be the backlight for the channel dial. Several of the diodes would illuminate parts of the cabinet that are not behind the channel selector diode. These are simply covered with black electrical tape to limit light leaks.

![](media/6dc9953c4be05d6149459f409d48ac54.png)

A fridge-switch is used in conjunction with the front left-most dial to cut power to the monitor and speakers. A 5A fuse breaker will act as a safety breaker to prevent passing current through the switch beyond what it is rated.

1/19/2023

![](media/620afe0b371aca6bae136144fa574eea.png)![](media/5e009a260795b8a12146647233681bd2.png)![](media/f0f6f85d1824b3f19a2ade17dcd0077d.png)

The original dials are disassembled and prepared to be used with the modern potentiometers.

1/21/2023

![](media/663d3f99e8a180fc0da651925879a685.png)![](media/5d854511a6e0c9b73b4685f4f404d940.png)![](media/106e9b4ebab3e5594a198c4d07d0b708.png)

After removing the cathode-ray tube, the bakelite mount, and the glass front, the components are cleaned and sized to mount the new monitor. New mounts and further cuts are made for the unit to fit together.

![](media/47e88302f7f20e111b257d201d91e0fa.png)![](media/111e779059bc245b3050a43b2b2d9cfd.png)

For the first time, the computer is turned on and booted up in the cabinet.

1/28/2023

![](media/710f71359aa2a3375d46439928a45a13.png)![](media/9f434d90e4481a182d591d73742996bf.png)![](media/b20fdf4e1b5d35ea6c3357863dffd83a.png)

![](media/c61a67725d197239144817576a3ccb03.png)![](media/6158f610eef2fb6d6ac845950de0fa22.png)

A new potentiometer is placed in the control unit. A piece of scrap metal is used as a limiter to prevent the dial from spinning beyond the potentiometer’s ability to interpret. This was first measured using the manilla paper for sizing before making metal cuts.

1/29/2023

![](media/4967e2cfb99f48fdc08e2de468f93783.png)![](media/dc596937164ebdbd6054201cb75fc311.png)![](media/f630f9f34a9ecef67d56b185a3459cea.png)

The bakelite tv mount is measured for fit with the monitor and the case for the electrical equipment.

1/30/2023

![](media/2ea372e9cda2784368b2febe4fe83f4c.png)![](media/008d3fa9e94fd2d9d6c8818309dc2b5f.png)

The damaged wood is sanded and refinished. The results are better, but the damage is still clearly noticeable.

2/4/2023

![](media/0578ba6ce6157356b4ec00b39d379463.png)![](media/1ad3e8345cdf06dceaa29e099de814db.png)![](media/5a03f96084fe83e7476998c0fd2381b7.png)

![](media/d919c3b41f5374e0b45e9ff418a8c816.png)![](media/8f7ef05f7e1ce8de49b01fc47849b913.png)

A custom case is built from wood and painted to house the electrical equipment. For the first time, the electronics are connected and tested together.

2/8/2023![](media/6f92911cc3ea0516b5bfe8535ef97abc.png)

Improvements are made to the knob mounts. Additionally, the jumper wires are soldered to the potentiometers.

2/15/2023![](media/5f6b36724a0c605e1ef00161bf4f2ab7.png)

Electrical wires are shown once connected to the outlets.

2/17/2023

![](media/7998308dd688c25b4737d64d7e94c65b.png)![](media/c80771005782d4f8e3c8e35cfa786188.png)

Cable management is performed and the automatic fire extinguisher is installed.

2/24/2023

**![](media/05d7234f3424ab20fbf30c6ff2ac48ca.png)**![](media/b72070e85aaf4e5c7d95045641735823.png)![](media/05c348f6447361650c51afc90da70115.png)

The internal knobs are connected to the main computer. The components and cables are labeled.

Completed back-view, with and without the cardboard backing.

3/30/2023

![](media/a8815aa9ce5b2ea9e6c0d5c76059eadc.png)![](media/39077d3db125ca6a2143047f3f897994.png)

Completed cabinet, front view before delivery (left image). VINTOS 2023 TV after installation in the AACA Hershey Museum as part of the Tucker Exhibit (right image). In the photo is Rob Kain (Director of Museum Advancement) and Andrew Marques (creator of VINTOS 2023 TV). Photo credit for the right image goes to Stanley Spiko (Museum Curator).

![](media/c8446cf880fa1121cc6c9afb53f6abfb.png)

The television is on display in the Tucker Sales Center section of the AACA Hershey Museum 161 Museum Dr, Hershey, PA 17033.

**Installation guide: For first time installing VINTOS**

1.  Using the command terminal, install the dependencies and prepare the files with the following commands:

    sudo apt update && sudo apt upgrade

    sudo apt install htop

    sudo snap install mediainfo \# For getting the duration of videos

    sudo snap install vlc

    sudo visudo

    sudo apt install thonny

    chmod +x player.sh

    chmod +x tv.py

    1.  username ALL=(ALL) NOPASSWD: /sbin/reboot \# Add this line to the end of visudo
2.  Install python dependencies.

    sudo apt install python3-pip

    pip3 install pyserial \# For potentiometer reading on Arduino

    pip3 install gpiozero \# For potentiometer reading on raspberry pi

    pip3 install pandas \# For main script

3.  Install arduino dependencies.
    1.  https://linuxconfig.org/how-to-install-Arduino-ide-on-ubuntu-20-04-focal-fossa

        sudo snap install arduino

4.  Prepare scripts to be run at boot.

    crontab -e

    1.  At the end of the crontab file, add:

        @reboot /home/andrewdmarques/Desktop/TV/Bin/Scripts/tv.py 1\> /home/andrewdmarques/Desktop/TV/Bin/Log-Files/log-root.txt 2\>&1

        @reboot /home/andrewdmarques/Desktop/TV/Bin/Scripts/player.sh

    2.  Save by CTRL+X, "y", ENTER
5.  Allow volume to be changed by the root user. https://unix.stackexchange.com/questions/473769/sound-doesnt-work-properly-in-root-but-does-in-normal-user

    sudo apt install pulseaudio

    sudo su

    mkdir /root/.config/pulse

    cp -r /home/andrewdmarques/.config/pulse/\* /root/.config/pulse/

    mkdir /root/.config/autostart

    cp /home/andrewdmarques/Desktop/TV/Bin/Archive/pulseaudio.desktop /root/.config/autostart/

6.  Prepare VLC player
    1.  In Tools\>Preferences\>Interface

        1) Uncheck "Resize interface to video size"

        2) Uncheck "Show controls in full screen mode"

        3) Check "Start in minimal view mode"

        4) Change "Show media change popup" to never

        5) Check "Use only one instance when started from file manager"

    2.  In Tools\>Preferences\>Subtitles/OSD then uncheck "Enable On Screen Display" and "Show media title on video start"
    3.  Save the preferences before exiting
7.  Enable screen brightness control
    1.  when booting up ubuntu go to the log in page and select the user but before putting the password, click the gear settings icon on the bottom right then change this to xorg -- this will allow the xrandr operation to
8.  Remove the automatic login prompt:
    1.  https://linuxconfig.org/wp-content/uploads/2020/01/04-how-to-enable-automatic-login-on-ubuntu-20-04-focal-fossa.png
    2.  https://linuxconfig.org/how-to-disable-keyring-popup-on-ubuntu\#:\~:text=The%20first%20option%20is%20you,master%20password%20for%20your%20keyring
    3.  Set the screen to never sleep (settings\>power\>screen blank set to never)
9.  Prepare the Arduino by uploading the potentiometer reader script. Follow popup window instructions from the Arduino software.

##**Build Costs**

**Total: \$433.35**

-   \$100 RCA Victor TV cabinet
-   \$16.21 vintage electrical cable <https://www.etsy.com/listing/181921564/custom-length-cord-w-plug-attached-26?click_key=cce03646b3c2b5d39c24897df7ff9ba14c7cc9e3%3A181921564&click_sum=40c915ac&ref=shop_home_feat_1&clickFromShopCard=1&frs=1&sts=1>
-   \$23.32 keyboard and trackpad (Logitech K400R) <https://www.ebay.com/itm/185724276957>
-   \$23.06 Processor for interpreting potentiometers (Arduino Uno Rev3) <https://www.ebay.com/itm/354493058859>
-   \$11.21 Extension cables (rated for 13A at 125V) <https://www.amazon.com/gp/product/B0B57V1992/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1>
-   \$8.47 Power switch (rated for 5A at 125V) <https://www.amazon.com/gp/product/B08QMKX7M8/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1>
-   \$50 Monitor (SAMSUNG SD360 Series Monitor 23.6'')
-   \$74.19 Computer (Lenovo ThinkCentre M93p Tiny Desktop i5-4570T 2.90GHz 8GB RAM 250GB SSD) <https://www.ebay.com/itm/225052512428>
-   \$6 Potentiometers (6x items at \$1 each) <https://www.amazon.com/dp/B07DHKQVG5/ref=redir_mobile_desktop?_encoding=UTF8&ref_=yo_ii_img&th=1>
-   \$2.80 Jumper cables (28x items at \$0.10 each, \$11.99 for 120) <https://www.amazon.com/dp/B07GD1TH2K/ref=redir_mobile_desktop?_encoding=UTF8&ref_=ya_aw_od_pi&th=1>
-   \$35.45 Speakers (JBL Platinum Series SP08A11) <https://www.ebay.com/itm/155353679122>
-   \$6.83 Display port to HDMI cable <https://www.amazon.com/dp/B015OW3GJK?psc=1&ref=ppx_yo2ov_dt_b_product_details>
-   \$8.43 One-gang device box for GFCI outlets (3x items at \$3.04 each) <https://www.amazon.com/gp/product/B00H8NUVQK/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1>
-   \$33.49 GFCI outlets rated for 15A at 125V(3x items at \$11.13 each) <https://www.amazon.com/gp/product/B0B7FHMNK7/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&th=1>
-   \$5.29 5A circuit breaker (selected because the power switch is rated for 5A at 125V) <https://www.amazon.com/gp/product/B08RBLTT14/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&th=1>
-   \$13.77 Black & Decker Timer with 7 day setting <https://www.amazon.com/dp/B094PFJ5JW?psc=1&ref=ppx_yo2ov_dt_b_product_details>
-   \$14.83 GE 6-outlet surge protector <https://www.amazon.com/dp/B00DOMYL24?psc=1&ref=ppx_yo2ov_dt_b_product_details>

##**Troubleshooting: General**

Your TV is not working correctly? Start with this checklist!

1.  Reboot the system by disconnecting and reconnecting the main power supply to the unit.
2.  Check that the 5A circuit breaker is not tripped. It should not require force to press it from the up to down position. Use caution, if the breaker is tripped, check that there are no shorts and there are no non-TV related items plugged into the GFCI outlets.
3.  Check the GFCI outlets are reset. All outlets should have a solid green light to indicate that they have power. There are 3x outlets to check.
4.  Check that all cables are fully connected. Cables that are most likely disconnected include:
    1.  Jumper wires (rainbow cables) connected to the breadboard.
    2.  Audio and power cables to the speaker.
    3.  Power, display, and audio cables to the main computer.
    4.  Power and display cables to the monitor.
5.  Check that the system has power cycled to it at least 1x time per day. This is best done with an outlet timer that will cut power to the cabinet without human intervention.
6.  Check that the main computer is powered on with its power button. DO NOT use the main computer power button to cycle power. Once it is pressed on, it should not be pressed again.

##**Troubleshooting: Specific**

**5A breaker keeps cutting power:**

-   Problem: Device does not have power when plugged in.
-   Solution:
    -   If the breaker is tripping, then immediately cut power to the system.
    -   Check that there are no shorts.
    -   Make sure no additional devices (vacuum cleaners, appliances, etc. are connected to the TV's GFCI outlets.
    -   Consider using a surge protector that bypasses the GFCI outlets.
    -   Contact Andrew Marques at email or phone on page 1.

**No power when plugged in:**

-   Problem: Device does not have power when plugged in.
-   Solution:
    -   If using the surge protector, check if it is receiving power. It may need to be reset.
    -   If using the GFCI outlets, check that the 5A breaker is not tripped, and the GFCI outlets are reset (there are 3x outlets to reset).

**Some power when plugged in:**

-   Problem: Some but not all devices are receiving power.
-   Solution:
    -   Try resetting the system by disconnecting and reconnecting the main power supply to the cabinet and rebooting the computer.
    -   Check that all power cables are plugged into outlets and their respective devices. Cables are labeled.
    -   Check that all GFCI outlets are reset. There are 3x outlets to check.
    -   Check that the power knob is working.

**No audio or quiet audio:**

-   Problem: Despite changing controls, the audio remains too quiet to hear.
-   Solution:
    -   Try resetting the system by disconnecting and reconnecting the main power supply to the cabinet and rebooting the computer.
    -   Check that all connections to the speaker and main computer are secure.
    -   Check that the volume knob on the speaker itself is set to the designated position (indicated by arrows).
    -   Check if the audio is louder in Default mode. If it is louder, there is likely an issue with the jumper wire connections. Check that all connections are secure. Check that the alternative knob (front or internal) are functioning). It may require a potentiometer to be replaced.
    -   If the audio is too quiet in default mode, check the sound settings. the sounds for the video file itself may be too low.
        -   Click the "Windows" button on the keyboard.
        -   Search "Sound".
        -   The settings should look like the image below.
    -   ![](media/9cd4fe587339226beddc33745d6b792d.png)

**Audio too loud:**

-   Problem: The audio is playing too loud, typically this occurs in the Default mode.
-   Solution:
    -   Turn down the knob on the speakers themselves (not the knobs on the TV).
    -   The max volume can be edited in the software under the vol_max variable, this accepts values from 0-1.

**No picture:**

-   Problem: The screen is black or does not show a program.
-   Solution:
    -   Try resetting the system by disconnecting and reconnecting the main power supply to the cabinet and rebooting the computer.
    -   Check that all connections to the monitor and main computer are secure.
    -   Try default mode. There should be image and sound. If there is no image or sound, check that there is a "/home/andrewdmarques/Desktop/TV/Bin/Scripts/tv-on.txt" file. If there is no file here, then make a blank file with this "tv-on.txt" at that location.

**Picture turns dark and fades in every few seconds:**

-   Problem: The TV is not operating correctly by showing an image briefly then cutting to black and fading back in. Typically the image is static.
-   Solution:
    -   Try resetting the system by disconnecting and reconnecting the main power supply to the cabinet and rebooting the computer.
    -   Check that there are videos in the channel directory "/home/andrewdmarques/Desktop/TV/Channels". If there are no video files here, then make sure each channel has a video file.
    -   Check that there are directories for channels 03-13 in "/home/andrewdmarques/Desktop/TV/Channels".
    -   Generate a new set of program schedules.
        -   Go to "/home/andrewdmarques/Desktop/TV/Bin/Program-Schedule/" and delete ALL the contents of this folder. They should be a set of CSV files.
        -   Disconnect and reconnect the main power supply to the cabinet.
        -   This will automatically generate a new list of schedules that now include the added program.
    -   This may be a software issue if the problem persists. Try using the default mode.

**Controls show no response:**

-   Problem: The dials are not changing volume, brightness, or channels.
-   Solution:
    -   This may be caused by a loose wire, damaged potentiometer, or the system is in a different setting.
    -   Check that the desired system mode is selected. For example, the front knobs will only work if the front mode is selected. See the Quickstart Guide for details.
    -   Check that there are no loose jumper wire. If there is a loose jumper wire, see the Loose Jumper Wire" section. Do not touch wires while system has power.
    -   Try default mode. There should be image and sound. If there is no image or sound, check that there is a "/home/andrewdmarques/Desktop/TV/Bin/Scripts/tv-on.txt" file. If there is no file here, then make a blank file with this "tv-on.txt" at that location.
    -   If default mode works, and all connections are made, contact Andrew.

**Controls reversed:**

-   Problem: When turning a dial the response is the opposite of what's expected.
-   Solution:
    -   Check the Arduino wiring diagram, it is likely the 5V and GND are switched for that potentiometer.
    -   If all dials are reversed compared to expectations, then 5V and GND to the breadboard as it connects to the Arduino may be switched.
    -   If connections are loose or switches, correct them and ensure a tight connection. .

**The power knob in the front of the TV set is not turning on or off:**

-   Problem: The power knob in the front of the unit is not turning on or off the TV set.
-   Solution:
    -   If your TV is plugged in using a surge protector strip bypassing the GFCI outlets, then this knob is designed to be bypassed too.
    -   If your TV is plugged in using the outlets, check that plugs are connected to the correct outlets: only the main computer should be connected to "On Always". All other plugs should be connected to "On with Switch".
    -   It is possible that the mechanism is broken. Contact Andrew.

**Stuck in default mode:**

-   Problem: When the Arduino is connected, it does not allow the front or internal knobs to be connected.
-   Solution:
    -   Try resetting the system by disconnecting and reconnecting the main power supply to the cabinet and rebooting the computer.
    -   Check that all connections are secure to the main computer, the Arduino, and the breadboard.

**Monitor appears unlevel when viewed from the front:**

-   Problem: The picture appears askew when viewing from the front.
-   Solution:
    -   Readjust the monitor from the inside. With some minor adjustments it should sit level from the viewer's perspective in the front.
    -   TIP: Make it so the bottom of the monitor is pressed as closely to the tan bakelite mount as possible.

**Jumper wires (colored thin cables) disconnected:**

-   Problem: Knobs are not working.
-   Solution:
    -   Use caution when connecting the wires, it is important to connect the positive and negative leads to the appropriate pins. Cables are in groups of three, the outermost wires are the positive and negative wires, the middle wire should be wired to send data to the Arduino.
    -   See the Arduino wiring diagram as a reference.

**Popup windows on monitor:**

-   Problem: Notification popups on monitor.
-   Solution:
    -   Dismiss notification.
    -   Try resetting the system by disconnecting and reconnecting the main power supply to the cabinet and rebooting the computer.
    -   Try to disable notifications by clicking the "Windows" button, searching for "Notifications" and disabling notifications.

**Date/Time incorrect error:**

-   Problem: The main computer has errors because the date and time are incorrect.
-   Solution:
    -   This is usually caused by being unplugged for more than a few weeks.
    -   See the "Long-term Storage" section of the Quickstart Guide for instructions on resetting the internal clock.

##**Disclaimer**

The television cabinet, electronics, and Vintage Television Operating System (VINTOS) described in this manual is provided "as is" with limited warranty at the discretion of the creator (Andrew D. Marques). This discretionary limited warranty includes but is not limited to the implied warranties of merchantability, fitness for a particular purpose, or non-infringement. In addition, the user may return the device at any time. Replacement of the device can be discussed at the discretion of the creator.

The creator strongly recommends bypassing the optional internal power switch and using a UL certified, grounded surge protector. The creator cannot be held liable for any damages arising from the use of this product, including but not limited to direct, indirect, incidental, or consequential damages. The user assumes full responsibility for any risks associated with the use of this product. By accepting and using this product, the user agrees to these terms and conditions.

##**About The Creator**

Andrew D. Marques is a virologist at the University of Pennsylvania's Perelman School of Medicine. Some of his favorite pastimes include spending time with his wife and family, building projects, programming, film photography, amateur birding, cycling, maintaining and driving cars, and restoring antique electronics by finding ways to incorporate them into modern life. Some of his fondest memories are the drives he takes with his wife in their 1969 Volkswagen Beetle. At a young age, he has been interested in taking a holistic perspective of history: where historical and current events are closely connected, and having a physical and mental connection to our past can better shape our present and future.

##**Acknowledgements**

The success of this project was made possible by the assistance of numerous friends, whose contributions I would like to acknowledge. I extend a special thank you to Scott Sherrill-Mix, Carter Merenstein, and Alex McFarland for their invaluable troubleshooting help with programming. I am also grateful to Aoife Doto for reproducing the front control labels and Orlando Ferreira for editing this manual.

Additionally, I owe a debt of gratitude to my wife Caitlyn Mierau-Marques, whose unwavering support was critical to the project's success. Caitlyn was endlessly patient and supportive, providing encouragement throughout the countless nights and many hours spent grinding away using the dremel or on the computer while we watched Netflix.

Their insights, feedback, and support were vital to the completion of this work.
