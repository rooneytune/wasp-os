#!/bin/bash

mpCompilerPath="/home/rooneytune/Documents/Code/rp-wasp-os/micropython/mpy-cross/"
#Set path for source code
sourceFilePath=/home/rooneytune/Documents/Code/rp-wasp-os/wasp/apps/
# Move to Code Dir
cd /home/rooneytune/Documents/Code/rp-wasp-os

# ----------------------------------------------
# Compile app files
# ----------------------------------------------

# -----------------------
# Process myble App
# -----------------------
# Set filename (no spaces near =)
fileNameLessExtension="myble"

# Delete existing source Files
sudo rm -f $mpCompilerPath$fileNameLessExtension".py" 
# Delete existing PreCompile Files
sudo rm -f $mpCompilerPath$fileNameLessExtension".mpy" 

# Copy source file to Apps dir
sudo cp $sourceFilePath$fileNameLessExtension".py" $mpCompilerPath$fileNameLessExtension".py"  

echo "Compiling: " $mpCompilerPath$fileNameLessExtension".py" 

cd $mpCompilerPath

# Crosscompile app file

sudo ./mpy-cross -mno-unicode -march=armv7m "myble.py"  
# Confirm file creation
echo "Compiled: " $fileNameLessExtension".mpy" 

# Copy compiled file to Apps dir
sudo cp $mpCompilerPath$fileNameLessExtension".mpy"  $sourceFilePath$fileNameLessExtension".mpy" 