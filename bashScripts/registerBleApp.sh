#!/bin/bash
currentDirPath=/home/rooneytune/Documents/Code/wasp-os
$currentDirPath/tools/wasptool --battery
$currentDirPath/tools/wasptool --eval "from myble import MyBleApp"
echo "Imported app"
$currentDirPath/tools/wasptool --eval "wasp.system.register(MyBleApp())"
echo "Registered app"
