#!/bin/bash

# Assign variables
fileName=myble.mpy
fileNameLessExtension=myble
appName=MyBleApp
appDirPath=/home/rooneytune/Documents/Code/wasp-os/wasp/apps
currentDirPath=/home/rooneytune/Documents/Code/wasp-os
pythonScriptsPath=$currentDirPath/bashScripts/pythonScripts

# Move to Code Dir
echo "appFilePath: " $appDirPath/$fileName
echo "currentDirPath: " $currentDirPath

cd $currentDirPath

# Restart watch as app removal appears not to work
#./tools/wasptool --reset
echo "Reset watch - waiting 5 seconds" 

#sleep 5s

#Get battery level (ensures communication is OK after restart)
./tools/wasptool --battery

# Crosscompile app file
./micropython/mpy-cross/mpy-cross -mno-unicode -march=armv7m $appDirPath/$fileNameLessExtension".py" 
# Confirm file creation
echo "Compiled: " $fileNameLessExtension".mpy" 

#----------------------------------------
#Delete existing mpy files from watch
#----------------------------------------
./tools/wasptool --exec $pythonScriptsPath/deleteAppsFromWatch.py
echo "Deleted app files from watch "

# --------------------------------------------
# Upload mpy file to watch
# --------------------------------------------
./tools/wasptool --binary --upload $appDirPath/$fileName

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
#./tools/wasptool --exec $pythonScriptsPath/getMyBleAppInfo.py


echo "Press any key to close terminal"
read -n 1 -s

