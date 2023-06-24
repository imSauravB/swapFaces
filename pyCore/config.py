# Copyright (c) 2023 imSauravB
#
# -*- coding:utf-8 -*-
# @Script: config.py
# @Author: imSauravB
# @Email: sauravkumarbehera@gmail.com
# @Create At: 2023-06-24 21:37:03
# @Last Modified By: imSauravB
# @Last Modified At: 2023-06-24 21:47:27
# @Description: This is description.


import onnxruntime

""" 
If you have a good Nvidia GPU enable this
For GPU RAM 6 GB, set the number of Threads to 2
For GPU RAM 8 GB, set the number of Threads to 4
For GPU RAM 12 GB, set the number of Threads to 6 or 8
"""
GPU_THREADS = 4 


"""
Get Availave onnxruntime providers. If CUDA is installed and GPU is detected 
this will return -- ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
From this list remove "TensorrtExecutionProvider" as in case of Transfermers and some other architectures the inferencing will be slower
"""
providers = onnxruntime.get_available_providers()
if 'TensorrtExecutionProvider' in providers:
    providers.remove('TensorrtExecutionProvider')
