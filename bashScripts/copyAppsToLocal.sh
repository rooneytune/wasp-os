#!/bin/bash

# Assign variables
fileName=myble.mpy
fileNameLessExtension=myble
appName=MyBleApp
localDirPath=/home/pi/Documents/Code/rp-wasp-os
remoteDirPath=/home/rooneytune/Documents/Code/rp-wasp-os/wasp/apps

# Move to Code Dir
cd $localDirPath

# --------------------------------------
# Copy mpy app files to local machine
# --------------------------------------

# Remove local file with same name
rm $localDirPath/$fileName

# Copy compiled file to local
scp  -i /home/pi/Documents/Code/Oracle/ssh-key-2022-01-05.key ubuntu@129.151.86.131:$remoteDirPath/$fileName $localDirPath/$fileName
echo $fileName " copied to local"

# Copy code file to local
scp  -i /home/pi/Documents/Code/Oracle/ssh-key-2022-01-05.key ubuntu@129.151.86.131:$remoteDirPath/$fileNameLessExtension".py" $localDirPath/$fileNameLessExtension".py"
echo $fileNameLessExtension ".py copied to local"




#----------------------------------------
#Delete existing mpy files from watch
#----------------------------------------
./tools/wasptool --exec deleteAppsFromWatch.py
echo "Deleted app files from watch "

# --------------------------------------------
# Upload mpy file to watch
# --------------------------------------------
./tools/wasptool --binary --upload $fileName

# ----------------------------------------
# Register apps
# ----------------------------------------

echo "Processing app: "$appName

#Unregister
waspCommand="wasp.system.unregister("$appName")"
echo "WaspCommand1: "$waspCommand
./tools/wasptool --eval $waspCommand
echo "Unregistered app"



# Import
waspCommand="from "$fileNameLessExtension" import "$appName
echo "WaspCommand2: "$waspCommand
./tools/wasptool --eval "$waspCommand"
echo "Imported app"
# Register
waspCommand="wasp.system.register($appName())"
echo "WaspCommand3: " $waspCommand
./tools/wasptool --eval "$waspCommand"
echo "Registered app"


#------------------------------------------------------------------------------------
#Get info about uloaded file (just to make sure the correct file has been uploaded)
#-----------------------------------------------------------------------------------
./tools/wasptool --exec getMyBleAppInfo.py


echo "Press any key to close terminal"
read -n 1 -s

