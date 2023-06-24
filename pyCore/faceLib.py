# Copyright (c) 2023 imSauravB
#
# -*- coding:utf-8 -*-
# @Script: faceLib.py
# @Author: imSauravB
# @Email: sauravkumarbehera@gmail.com
# @Create At: 2023-06-24 21:49:14
# @Last Modified By: imSauravB
# @Last Modified At: 2023-06-25 01:32:09
# @Description: This is description.


import insightface
import pyCore.config

FACE_ANALYSER = None

def getInsightFaceAnalyser():
    """
     Returns insight face analyser. It is used to detect faces in an Image Frame.
     
     @return an instance of : class : ` FaceAnalysis ` that can be used to detect faces in the Image
    """
    global FACE_ANALYSER
    if FACE_ANALYSER is None:
        FACE_ANALYSER = insightface.app.FaceAnalysis(name='buffalo_l', providers=pyCore.config.providers)
        FACE_ANALYSER.prepare(ctx_id=0, det_size=(640, 640))
    return FACE_ANALYSER

def getSourceFace(imgFrame):
    """
     @param imgFrame - ImageFrame to look up the source face
     
     @return Source face or None
    """
    try:
        faces = getInsightFaceAnalyser().get(imgFrame)
        sourceFace = sorted(faces, key=lambda x: x.bbox[0])[0]
        return sourceFace
    except Exception as e:
        print("Exception Occured in getSourceFace!: " + str(e))
        return None

def getAllFaces(imgFrame):
    """
     @param imgFrame - Image to detecte faces from
     
     @return List of faces or None
    """
    try:
         return getInsightFaceAnalyser().get(imgFrame)
    except Exception as e:
        print("Exception Occured in getAllFaces!: " + str(e))
        return None