#!/bin/bash

# Assign variables
fileName=myble.mpy
fileNameLessExtension=myble
appName=MyBleApp
localDirPath=/home/rooneytune/Documents/Code/wasp-os/wasp/apps
compileDirPath=/home/rooneytune/Documents/Code/wasp-os/micropython/mpy-cross

# Move to Code Dir
cd /home/rooneytune/Documents/Code/wasp-os


# ----------------------------------------------
# Compile app files
# ----------------------------------------------

# Set filename (no spaces near =)
fileNameLessExtension=myble

echo "File Path: " $localDirPath/$fileNameLessExtension".py"

# Delete existing PreCompile Files
#rm $compileDirPath/$fileNameLessExtension".mpy" 
#cp $localDirPath/$fileNameLessExtension".py" $compileDirPath/$fileNameLessExtension".py"

# Crosscompile app file
./micropython/mpy-cross/mpy-cross -mno-unicode -march=armv7m $localDirPath/$fileNameLessExtension".py" 
# Confirm file creation
echo "Compiled: " $fileNameLessExtension".mpy" 

