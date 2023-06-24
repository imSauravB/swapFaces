# Copyright (c) 2023 imSauravB
#
# -*- coding:utf-8 -*-
# @Script: swapFacesMain.py
# @Author: imSauravB
# @Email: sauravkumarbehera@gmail.com
# @Create At: 2023-06-24 21:28:47
# @Last Modified By: imSauravB
# @Last Modified At: 2023-06-25 00:40:35
# @Description: This is description.

import sys, os
import time
import argparse
import torch
import shutil
import glob
from pathlib import Path
import multiprocessing as MP
import psutil
from opennsfw2 import predict_image as checkFaceExist
import cv2

import pyCore.config
from pyCore.videoUtils import is_img, detect_fps, set_fps, create_video, add_audio, extract_frames, rreplace
from pyCore.faceLib import getSourceFace
from pyCore.faceSwap import processTargetVideo, processFramesBatch

"""
File path separator based on Linux/Mac or Winodws
"""
separator = "/"
if os.name == "nt":
    separator = "\\"

if '--gpu' in sys.argv:
    print("You have selected GPU accelaration, plse make sure you have a working Nvidia GPU and Cuda install")
    # Incase of AMD GPU check which AMD architectures are supported by pytorc(e.x. RX6700XT: <gpu_arch>=gfx1031 ), and install rcom/hid

args = {}
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--face', help='use this face', dest='source_img')
parser.add_argument('-t', '--target', help='replace this face', dest='target_path')
parser.add_argument('-o', '--output', help='save output to this file', dest='output_file')
parser.add_argument('--gpu', help='use gpu', dest='gpu', action='store_true', default=False)
parser.add_argument('--keep-fps', help='maintain original fps', dest='keep_fps', action='store_true', default=False)

for name, value in vars(parser.parse_args()).items():
    args[name] = value

def checkDependencies():
    if not shutil.which('ffmpeg'):
        quit('Please install ffmpeg and try again!')
    faceModelPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'faceSwapModel.onnx')
    if not os.path.isfile(faceModelPath):
        quit('Model file "faceSwapModel.onnx" not found!')
    if '--gpu' in sys.argv:
        print("GPU option is selected. Not adding any execution provider here.")
    else:
        print("Adding CPUExecutionProvider!")
        pyCore.config.providers = ['CPUExecutionProvider']

def startVideoProcessing():
    start_time = time.time()
    if args['gpu']:
        print("GPU Option is selected!")
        processTargetVideo(args['source_img'], args["frame_paths"])
        end_time = time.time()
        print(flush=True)
        print(f"Processing time: {end_time - start_time:.2f} seconds", flush=True)
    else:
        print("Going to run on CPU only!")
        global pool
        numberOfCPUCores = psutil.cpu_count() - 2
        pool = MP.Pool( numberOfCPUCores ) # Run the code in maxcpucore - 2
        frame_paths = args["frame_paths"]
        n = len(frame_paths)//(numberOfCPUCores)
        processes = []
        for i in range(0, len(frame_paths), n):
            p = pool.apply_async(processFramesBatch, args=(args['source_img'], frame_paths[i:i+n],))
            processes.append(p)
        for p in processes:
            p.get()
        pool.close()
        pool.join()
        end_time = time.time()
        print(flush=True)
        print(f"Processing time: {end_time - start_time:.2f} seconds", flush=True)


def startMain():
    try:
        if not args['source_img'] or not os.path.isfile(args['source_img']):
            print("\n[WARNING] Please select an image containing a face.")
            return
        elif not args['target_path'] or not os.path.isfile(args['target_path']):
            print("\n[WARNING] Please select a video/image to swap face in.")
            return
        if not args['output_file']:
            target_path = args['target_path']
            args['output_file'] = rreplace(target_path, "/", "/swapped-", 1) if "/" in target_path else "swapped-" + target_path
        testSourceFace = getSourceFace(cv2.imread(args['source_img']))
        if not testSourceFace:
            print("\n[WARNING] No face detected in source image. Please try with another one.\n")
            return
        
        videoNameFull = target_path.split("/")[-1]
        videoName = os.path.splitext(videoNameFull)[0]
        output_dir = os.path.dirname(target_path) + "/" + videoName
        Path(output_dir).mkdir(exist_ok=True)
        
        print("Going to detect Video FPS!")
        fps, exact_fps = detect_fps(target_path)
        print("### GOT FPS: " + str(fps) + ", " + str(exact_fps) + " ###")
        if not args['keep_fps'] and fps > 30:
            this_path = output_dir + "/" + videoName + ".mp4"
            set_fps(target_path, this_path, 30)
            target_path, exact_fps = this_path, 30
        else:
            shutil.copy(target_path, output_dir)
        
        print("Going to extract the video frames!")
        extract_frames(target_path, output_dir)
        args['frame_paths'] = tuple(sorted(
            glob.glob(output_dir + "/*.jpeg"),
            key=lambda x: int(x.split(sep)[-1].replace(".jpeg", ""))
        ))

        print("Face swaping in progress!")
        startVideoProcessing()
        print("Swaping Done, now creating Video!")
        create_video(videoName, exact_fps, output_dir)
        print("Video creation done, now adding audio to the video file!")
        add_audio(output_dir, target_path, videoNameFull, args['keep_frames'], args['output_file'])
        save_path = args['output_file'] if args['output_file'] else output_dir + "/" + videoName + ".mp4"
        print("\nVideo saved as:", save_path, "\n")
        print("Face swap successful!")
    except Exception as e:
        print("Exception Occured!: " + str(e))

if __name__ == "__main__":
    checkDependencies()
    startMain()
    quit()