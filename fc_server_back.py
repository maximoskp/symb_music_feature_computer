#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 17:38:52 2019

@author: maximoskaliakatsos-papakostas
"""

import os
cwd = os.getcwd()
import FC_feature_computation_functions as fcf

folder_in = 'input_files' + os.sep
folder_out = 'output_files' + os.sep

file_in_name = 'BC_001_026900B_a1.xml';
file_in_path = cwd + os.sep + folder_in + file_in_name
file_out_name = file_in_name.split('.')[0] + '.csv'
file_out_path = cwd + os.sep + folder_out + file_out_name

# which parts to show features for
parts_in = [0,1]

f = fcf.extract_features_of_parts_to_csv(file_in_path, parts_in, file_out_path)