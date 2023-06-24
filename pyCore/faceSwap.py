# Copyright (c) 2023 imSauravB
#
# -*- coding:utf-8 -*-
# @Script: faceSwap.py
# @Author: imSauravB
# @Email: sauravkumarbehera@gmail.com
# @Create At: 2023-06-24 21:58:48
# @Last Modified By: imSauravB
# @Last Modified At: 2023-06-24 23:26:00
# @Description: This is description.

import os
import time
import cv2
import insightface
import pyCore.config
from  pyCore.faceLib import getSourceFace, getAllFaces
import threading

FACE_SWAPPER = None

currentMilliSecTime = lambda: int(round(time.time() * 1000))

#TOTAL_TIME = 0
#TOTAL_FRAMES = 0

def getInsightFaceSwapper():
    global FACE_SWAPPER
    if FACE_SWAPPER is None:
        model_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../faceSwapModel.onnx')
        FACE_SWAPPER = insightface.model_zoo.get_model(model_path, providers=pyCore.config.providers)
    return FACE_SWAPPER

def swapFace(sourceFace, faceToBeSwaped, imageFrame):
    if faceToBeSwaped:
        processedFrame = getInsightFaceSwapper().get(imageFrame, faceToBeSwaped, sourceFace, pasteBack=True)
        return processedFrame
    else:
        return imageFrame

def processOneVideoFrame(sourceFace, videoFrame):
    # stratTime = currentMilliSecTime()
    totalFacesFound = getAllFaces(videoFrame)
    if totalFacesFound:
        for eachFace in totalFacesFound:
            videoFrame = swapFace(sourceFace, eachFace, videoFrame)
        print("-", end='', flush=True) # print - if faces found in frame
        # endTime = currentMilliSecTime()
        # timeTakenPerFrame = endTime - stratTime
        return videoFrame, True
    else:
        print('S', end='', flush=True) # print 'S' for "skip" if faces not found in frame
        return videoFrame, False

def processFramesBatch(sourceFaceImagePath, framesBatchPath):
    try:
        sourceFaceImage = cv2.imread(sourceFaceImagePath)
        sourceFace = getSourceFace(sourceFaceImage)
        for eachFramePath in framesBatchPath:
            eachFrame = cv2.imread(eachFramePath)
            processedFrame, faceFound = processOneVideoFrame(sourceFace, eachFrame)
            if faceFound:
                cv2.imwrite(eachFramePath, processedFrame)
    except Exception as e:
        print("Exception Occured!: " + str(e))

def processTargetVideo(sourceFaceImagePath, totalVideoFramesPath):
    try:
        totalThreads = []
        numOfThread = pyCore.config.GPU_THREADS
        framesPerBatch = len(totalVideoFramesPath) // numOfThread
        leftOverFramesBatch = len(totalVideoFramesPath) % numOfThread
        startIndex = 0
        for i in range(numOfThread):
            endIndex = startIndex + framesPerBatch
            if leftOverFramesBatch > 0:
                endIndex += 1
                leftOverFramesBatch -= 1
            framesBatchPath = totalVideoFramesPath[startIndex:endIndex]
            thread = threading.Thread( target=processFramesBatch, args=(sourceFaceImagePath, framesBatchPath) )
            totalThreads.append(thread)
            thread.start()
            startIndex = endIndex

        for eachthread in numOfThread:
            eachthread.join()
    except Exception as e:
        print("Exception Occured!: " + str(e))
