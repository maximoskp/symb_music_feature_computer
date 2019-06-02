#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 09:41:14 2018

@author: maximoskaliakatsos-papakostas
"""

import music21 as m21
import numpy as np
import scipy.stats as sc
import csv
import copy

def get_most_correlated_rpcp(pcp_in):
    pcp = np.array( pcp_in )
    rpcp = np.array( pcp_in )
    a = m21.analysis.discrete.KrumhanslSchmuckler()
    maj_template = np.array( a.getWeights('major') )
    min_template = np.array( a.getWeights('minor') )
    # initialise max correlation
    max_corr = -1
    # first check major correlations
    for i in range(12):
        tmp_pcp = np.roll( pcp , i )
        tmp_corr = np.corrcoef( tmp_pcp , maj_template )[0][1]
        if tmp_corr > max_corr:
            rpcp = copy.deepcopy( tmp_pcp )
            max_corr = tmp_corr
    # then check major correlations
    for i in range(12):
        tmp_pcp = np.roll( pcp , i )
        tmp_corr = np.corrcoef( tmp_pcp , np.roll( min_template , -3 ) )[0][1]
        if tmp_corr > max_corr:
            rpcp = copy.deepcopy( tmp_pcp )
            max_corr = tmp_corr
    return rpcp

def compute_features_of_m21score(s):
    # f_initial = m21.features.base.allFeaturesAsList(s)
    # put all features in a dictionary
    f_0 = {}
    # melody features
    m = m21.features.jSymbolic.AmountOfArpeggiationFeature(s)
    f_0['AmountOfArpeggiation'] = m.extract().vector
    m = m21.features.jSymbolic.AverageMelodicIntervalFeature(s)
    try:
        f_0['AverageMelodicInterval'] = m.extract().vector
    except ZeroDivisionError:
        print('Zero division error for AverageMelodicInterval - assigning a value of zero')
        f_0['AverageMelodicInterval'] = 0
    m = m21.features.jSymbolic.MostCommonMelodicIntervalFeature(s)
    try:
        f_0['MostCommonMelodicInterval'] = m.extract().vector
    except ZeroDivisionError:
        print('Zero division error for MostCommonMelodicInterval - assigning a value of zero')
        f_0['MostCommonMelodicInterval'] = 0
    m = m21.features.jSymbolic.MostCommonMelodicIntervalPrevalenceFeature(s)
    try:
        f_0['MostCommonMelodicIntervalPrevalence'] = m.extract().vector
    except ZeroDivisionError:
        print('Zero division error for MostCommonMelodicIntervalPrevalence - assigning a value of zero')
        f_0['MostCommonMelodicIntervalPrevalence'] = 0
    m = m21.features.jSymbolic.RelativeStrengthOfMostCommonIntervalsFeature(s)
    try:
        f_0['RelativeStrengthOfMostCommonIntervals'] = m.extract().vector
    except ZeroDivisionError:
        print('Zero division error for RelativeStrengthOfMostCommonIntervals - assigning a value of zero')
        f_0['RelativeStrengthOfMostCommonIntervals'] = 0
    m = m21.features.jSymbolic.RelativeStrengthOfTopPitchesFeature(s)
    f_0['RelativeStrengthOfTopPitches'] = m.extract().vector
    m = m21.features.jSymbolic.RelativeStrengthOfTopPitchClassesFeature(s)
    f_0['RelativeStrengthOfTopPitchClasses'] = m.extract().vector
    m = m21.features.jSymbolic.IntervalBetweenStrongestPitchesFeature(s)
    f_0['IntervalBetweenStrongestPitches'] = m.extract().vector
    m = m21.features.jSymbolic.IntervalBetweenStrongestPitchClassesFeature(s)
    f_0['IntervalBetweenStrongestPitchClasses'] = m.extract().vector
    m = m21.features.jSymbolic.PitchVarietyFeature(s)
    f_0['PitchVariety'] = m.extract().vector
    m = m21.features.jSymbolic.PitchClassVarietyFeature(s)
    f_0['PitchClassVariety'] = m.extract().vector
    m = m21.features.jSymbolic.RangeFeature(s)
    f_0['Range'] = m.extract().vector
    m = m21.features.jSymbolic.PitchClassDistributionFeature(s)
    f_0['PitchClassDistribution'] = m.extract().vector
    f_0['RelativePitchClassDistribution'] = get_most_correlated_rpcp( f_0['PitchClassDistribution'] )
    f_0['PitchClassDistributionEntropy'] = [sc.entropy( m.extract().vector )]
    m = m21.features.jSymbolic.MelodicIntervalHistogramFeature(s)
    try:
        f_0['MelodicIntervalHistogram'] = m.extract().vector[0:24]
    except ZeroDivisionError:
        print('Zero division error for MelodicIntervalHistogram - assigning a value of zero')
        f_0['MelodicIntervalHistogram'] = 0
    m = m21.features.jSymbolic.BasicPitchHistogramFeature(s)
    try:
        f_0['BasicPitchHistogram'] = m.extract().vector
    except ZeroDivisionError:
        print('Zero division error for BasicPitchHistogram - assigning a value of zero')
        f_0['BasicPitchHistogram'] = 0
    try:
        f_0['BasicPitchHistogramEntropy'] = [sc.entropy( m.extract().vector )]
    except ZeroDivisionError:
        print('Zero division error for BasicPitchHistogramEntropy - assigning a value of zero')
        f_0['BasicPitchHistogramEntropy'] = 0
    m = m21.features.jSymbolic.ChromaticMotionFeature(s)
    f_0['ChromaticMotion'] = m.extract().vector
    # rhythm features
    m = m21.features.jSymbolic.AverageNoteDurationFeature(s)
    f_0['AverageNoteDuration'] = m.extract().vector
    m = m21.features.jSymbolic.VariabilityOfNoteDurationFeature(s)
    f_0['VariabilityOfNoteDuration'] = m.extract().vector
    m = m21.features.jSymbolic.AverageTimeBetweenAttacksFeature(s)
    f_0['AverageTimeBetweenAttacks'] = m.extract().vector
    m = m21.features.jSymbolic.VariabilityOfTimeBetweenAttacksFeature(s)
    f_0['VariabilityOfTimeBetweenAttacks'] = m.extract().vector
    m = m21.features.jSymbolic.NoteDensityFeature(s)
    f_0['NoteDensity'] = m.extract().vector
    return f_0
# end compute_features_of_m21score

def compute_features_of_file_parts(f, p=[]):
    # f: full file path
    # p: array of part numbers
    # create a new stream and include only the parts of interest
    s_in = m21.converter.parse(f)
    result = -1 # to be returned if given parts are irrelevant
    # check if user has wants all parts to be included -> p is empty
    if len(p) == 0:
        print('all parts selected')
        p = range(len(s_in.parts))
    if len(p) <= len(s_in.parts) and max(p) < len(s_in.parts):
        s_out = m21.stream.Score()
        for i in p:
            s_out.insert(0, s_in.parts[i])
        result = compute_features_of_m21score(s_out)
    return result
# end compute_features_of_file_parts

def extract_features_of_parts_to_csv(f_in, parts, f_out):
    # compute features dictionary
    f0 = compute_features_of_file_parts(f_in, parts)
    # write to csv
    with open(f_out,'w') as f:
        w = csv.writer(f)
        # get keys and values as lists
        keys = list( f0.keys() )
        values = list( f0.values() )
        for i in range( len(keys) ):
            w.writerow( [keys[i], values[i]] )
    return f0
# end extract_features_of_parts_to_csv