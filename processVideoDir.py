
# Copyright (c) 2023 imSauravB
#
# -*- coding:utf-8 -*-
# @Script: processVideoDir.py
# @Author: imSauravB
# @Email: sauravkumarbehera@gmail.com
# @Create At: 2023-06-25 00:44:14
# @Last Modified By: imSauravB
# @Last Modified At: 2023-06-25 02:20:19
# @Description: This is description.

import os
import time

from os import listdir
from os.path import isfile, join

sourcePath = "C:/Users/saurav/sourceVideos/"
sourceImage = "C:/Users/saurav/sourceImage.jpg"
destPath = "C:/Users/saurav/destination/"
procressedFilesPath = "C:/Users/saurav/done/"

onlyfiles = [f for f in listdir(sourcePath) if isfile(join(sourcePath, f))]

if not onlyfiles:
    print("No Videos Found in the given directory!")

for sourceFileName in onlyfiles:
    sourceFilePath = os.path.join( sourcePath, sourceFileName )
    print (sourceFilePath)
    currentEpoch = str ( int( time.time() ) )
    destFilePath = os.path.join( destPath, currentEpoch + ".mp4" )
    print (destFilePath)
    print ( "python swapFacesMain.py --gpu --keep-fps -f " + sourceImage + " -t " + sourceFilePath + " -o " + destFilePath )
    os.system ( "python swapFacesMain.py --gpu --keep-fps -f " + sourceImage + " -t " + sourceFilePath + " -o " + destFilePath )
    time.sleep(5)
    procressedFilesPathName = os.path.join( procressedFilesPath, sourceFileName )
    sourceFilePathWindows = sourceFilePath.replace("/", "\\" )
    procressedFilesPathWindows = procressedFilesPathName.replace("/", "\\" )
    os.rename(sourceFilePathWindows, procressedFilesPathWindows)
    time.sleep(2)
