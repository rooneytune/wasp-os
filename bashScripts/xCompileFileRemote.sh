#!/bin/bash
 Output arguments (for debug purposes)
echo "Total number of arguments: $#"
echo "Arg1: $1"

# Connect to Remote server
ssh ubuntu@129.151.86.131 -i /home/pi/Documents/Code/Oracle/ssh-key-2022-01-05.key
ssh rooneytune@129.151.86.131 -i /home/pi/Documents/Code/Oracle/ssh-key-2022-01-05.key


#Wait 5 seconds
sleep 5s

# Move to Code Dir
cd /home/rooneytune/Documents/Code


scp /home/pi/Documents/Code/rp-wasp-os/wasp/apps/helloRooney.py ubuntu@129.151.86.131:/home/rooneytune/Documents/Code

ls

# Keep terminal open
echo "File copied"
read name

#

# Execute this on local machine

# PreCompile File
./micropython/mpy-cross/mpy-cross -mno-unicode -march=armv7m myble.py
# Copy file to local
scp  -i /home/pi/Documents/Code/Oracle/ssh-key-2022-01-05.key ubuntu@129.151.86.131:/home/rooneytune/Documents/Code/rp-wasp-os/myble.mpy /home/pi/Documents/Code/rp-wasp-os/myble.mpy


cd /home/pi/Documents/Code/rp-wasp-os/


# Connect Reset watch
./tools/wasptool --reset
./tools/wasptool --binary --upload myble.mpy


sudo rsync -v -e /home/pi/Documents/Code/rp-wasp-os/wasp/apps/helloRooney.py ubuntu@129.151.86.131:/home/rooneytune/Documents/Code

sudo rsync -avz -e "ssh -i /home/pi/Documents/Code/Oracle/ssh-key-2022-01-05.key" /home/pi/Documents/Code/rp-wasp-os/wasp/apps/ ubuntu@129.151.86.131:/home/rooneytune/Documents/Code/WaspApps



sudo setfacl -m u:pi:rwx /home/rooneytune/Documents/Code/WaspApps

rsync -v -e /home/rooneytune/Documents/Code/rp-wasp-os/myble.mpy pi@192.168.1.51:/home/pi/Documents/Code/rp-wasp-os/
