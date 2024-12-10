
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

sourcePath = "/Users/saurav/Pictures/vids/sourceVideos/"
sourceImage = "/Users/saurav/Pictures/vids/source/6.3.jpg"
destPath = "/Users/saurav/Pictures/vids/destination/"
procressedFilesPath = "/Users/saurav/Pictures/vids/done/"

onlyfiles = [f for f in listdir(sourcePath) if isfile(join(sourcePath, f))]

startTime = int( time.time() )

if not onlyfiles:
    print("No Videos Found in the given directory!")

for sourceFileName in onlyfiles:
    sourceFilePath = os.path.join( sourcePath, sourceFileName )
    print (sourceFilePath)
    currentEpoch = str ( int( time.time() ) )
    destFilePath = os.path.join( destPath, currentEpoch + ".mp4" )
    #destFilePath = os.path.join( destPath, sourceFileName )
    print (destFilePath)
    print ( "/usr/bin/python3 swapFacesMain.py --keep-fps -f " + sourceImage + " -t " + sourceFilePath + " -o " + destFilePath )
    os.system ( "/usr/bin/python3 swapFacesMain.py --keep-fps -f " + sourceImage + " -t " + sourceFilePath + " -o " + destFilePath )
    time.sleep(5)
    procressedFilesPathName = os.path.join( procressedFilesPath, sourceFileName )
    #sourceFilePathWindows = sourceFilePath.replace("/", "\\" )
    #procressedFilesPathWindows = procressedFilesPathName.replace("/", "\\" )
    os.rename(sourceFilePath, procressedFilesPathName)
    time.sleep(8)

endTime = int( time.time() )
print("total time: " + str(endTime - startTime) )