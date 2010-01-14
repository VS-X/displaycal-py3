#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

import colormath

# from xcolorants.c
icx_ink_table = {
	"C": [
	  [ 0.12, 0.18, 0.48 ],	
	  [ 0.12, 0.18, 0.48 ] ],	
	"M": [
	  [ 0.38, 0.19, 0.20 ],	
	  [ 0.38, 0.19, 0.20 ] ],	
	"Y": [
	  [ 0.76, 0.81, 0.11 ],	
	  [ 0.76, 0.81, 0.11 ] ],	
	"K": [
	  [ 0.01, 0.01, 0.01 ],	
	  [ 0.04, 0.04, 0.04 ] ],	
	"O": [
	  [ 0.59, 0.41, 0.03 ],	
	  [ 0.59, 0.41, 0.05 ] ],	
	"R": [
	  [ 0.412414, 0.212642, 0.019325 ],
	  [ 0.40, 0.21, 0.05 ] ],	
	"G": [
	  [ 0.357618, 0.715136, 0.119207 ],
	  [ 0.11, 0.27, 0.21 ] ],	
	"B": [
	  [ 0.180511, 0.072193, 0.950770 ],
	  [ 0.11, 0.27, 0.47 ] ],	
	"W": [
	  [ 0.950543, 1.0,  1.089303 ],		# D65 ?
	  [ 0.9642,   1.00, 0.8249 ] ],		# D50
	"LC": [
	  [ 0.76, 0.89, 1.08 ],	
	  [ 0.76, 0.89, 1.08 ] ],	
	"LM": [
	  [ 0.83, 0.74, 1.02 ],	
	  [ 0.83, 0.74, 1.02 ] ],	
	"LY": [
	  [ 0.88, 0.97, 0.72 ],	
	  [ 0.88, 0.97, 0.72 ] ],	
	"LK": [
	  [ 0.56, 0.60, 0.65 ],	
	  [ 0.56, 0.60, 0.65 ] ],	
	"MC": [
	  [ 0.61, 0.81, 1.07 ],	
	  [ 0.61, 0.81, 1.07 ] ],	
	"MM": [
	  [ 0.74, 0.53, 0.97 ],	
	  [ 0.74, 0.53, 0.97 ] ],	
	"MY": [
	  [ 0.82, 0.93, 0.40 ],	
	  [ 0.82, 0.93, 0.40 ] ],	
	"MK": [
	  [ 0.27, 0.29, 0.31 ],	
	  [ 0.27, 0.29, 0.31 ] ],	
	"LLK": [
	  [ 0.76, 0.72, 0.65 ],		# Very rough - should substiture real numbers
	  [ 0.76, 0.72, 0.65 ] ],	
	"": [ [ 0.0, 0.0, 0.0 ], [ 0.0, 0.0, 0.0 ] ]
}

s = {
	"Ynorm": 0.0,
	"iix": {
		0: "R",
		1: "G",
		2: "B"
	}
}

s["Ynorm"] = 0.0
for e in xrange(3):
	s["Ynorm"] += icx_ink_table[s["iix"][e]][0][1]
s["Ynorm"] = 1.0 / s["Ynorm"]


def XYZ_denormalize_remove_glare(X, Y, Z):
	XYZ = [X, Y, Z]
	# De-Normalise Y from 1.0, & remove black glare
	for j in xrange(3):
		XYZ[j] = (XYZ[j] - icx_ink_table["K"][0][j]) / (1.0 - icx_ink_table["K"][0][j])
		XYZ[j] /= s["Ynorm"]
	return tuple(XYZ)


def XYZ_normalize_add_glare(X, Y, Z):
	XYZ = [X, Y, Z]
	# Normalise Y to 1.0, & add black glare
	for j in xrange(3):
		XYZ[j] *= s["Ynorm"]
		XYZ[j] = XYZ[j] * (1.0 - icx_ink_table["K"][0][j]) + \
				 icx_ink_table["K"][0][j]
	return tuple(XYZ)


def RGB2XYZ(R, G, B):  # from xcolorants.c -> icxColorantLu_to_XYZ
	d = (R, G, B)
	# We assume a simple additive model with gamma
	XYZ = [0.0, 0.0, 0.0]
	for e in xrange(3):
		v = d[e]
		if (v < 0.0):
			v = 0.0
		elif (v > 1.0):
			v = 1.0
		if (v <= 0.03928):
			v /= 12.92
		else:
			v = math.pow((0.055 + v) / 1.055, 2.4)		# Gamma
		for j in xrange(3):
			XYZ[j] += v * icx_ink_table[s["iix"][e]][0][j]
	return XYZ_normalize_add_glare(*XYZ)


def XYZ2RGB(X, Y, Z):
	# RGB = [0.0, 0.0, 0.0]
	# for e in xrange(3):
		# c = []
		# cc = []
		# for j in xrange(3):
			# v = XYZ[j]
			# c += [round(v / icx_ink_table[s["iix"][e]][0][j], 10)]
			# cc += [round(icx_ink_table[s["iix"][e]][0][j] / v, 10)]
		# if c[0] == c[1] == c[2]:  # primary color
			# v = c[0]
			# v = math.pow(v, 1.0 / 2.4)
			# v = v * 1.055 - 0.055
			# RGB[e] = v
			# break
		# for j in xrange(3):  # white
			# v = cc[j]
			# RGB[j] += v
	return colormath.XYZ2RGB(*XYZ_denormalize_remove_glare(X, Y, Z))


if __name__ == '__main__':
	from safe_print import safe_print
	# 100.00 100.00 100.00 95.106 100.00 108.84 
	safe_print(RGB2XYZ(1.0, 1.0, 1.0))
	# 0.0000 0.0000 0.0000 1.0000 1.0000 1.0000 
	safe_print(RGB2XYZ(0.0, 0.0, 0.0))
	# 50.000 0.0000 0.0000 9.7393 5.5060 1.4095 
	safe_print(RGB2XYZ(0.5, 0.0, 0.0))
	# 100.00 0.0000 0.0000 41.830 22.052 2.9132 
	safe_print(RGB2XYZ(1.0, 0.0, 0.0))
	# 0.0000 50.000 0.0000 8.5782 16.154 3.5261 
	safe_print(RGB2XYZ(0.0, 0.5, 0.0))
	# 50.000 50.000 0.0000 17.318 20.660 3.9356 
	safe_print(RGB2XYZ(0.5, 0.5, 0.0))
	# 100.00 50.000 0.0000 49.408 37.206 5.4393 
	safe_print(RGB2XYZ(1.0, 0.5, 0.0))
	# 0.0000 100.00 0.0000 36.405 71.801 12.802 
	safe_print(RGB2XYZ(0.0, 1.0, 0.0))
	# 50.000 100.00 0.0000 45.145 76.307 13.211 
	safe_print(RGB2XYZ(0.5, 1.0, 0.0))
	# 100.00 100.00 0.0000 77.235 92.853 14.715 
	safe_print(RGB2XYZ(1.0, 1.0, 0.0))
	# 0.0000 0.0000 50.000 4.8252 2.5298 21.147 
	safe_print(RGB2XYZ(0.0, 0.0, 0.5))
	# 50.000 0.0000 50.000 13.564 7.0358 21.557 
	safe_print(RGB2XYZ(0.5, 0.0, 0.5))
	# 100.00 0.0000 50.000 45.655 23.582 23.061 
	safe_print(RGB2XYZ(1.0, 0.0, 0.5))
	# 0.0000 50.000 50.000 12.403 17.684 23.674 
	safe_print(RGB2XYZ(0.0, 0.5, 0.5))
	# 50.000 50.000 50.000 21.143 22.190 24.083 
	safe_print(RGB2XYZ(0.5, 0.5, 0.5))
	# 100.00 50.000 50.000 53.233 38.736 25.587 
	safe_print(RGB2XYZ(1.0, 0.5, 0.5))
	# 0.0000 100.00 50.000 40.230 73.330 32.949 
	safe_print(RGB2XYZ(0.0, 1.0, 0.5))
	# 50.000 100.00 50.000 48.970 77.836 33.359 
	safe_print(RGB2XYZ(0.5, 1.0, 0.5))
	# 100.00 100.00 50.000 81.061 94.383 34.863 
	safe_print(RGB2XYZ(1.0, 1.0, 0.5))
	# 0.0000 0.0000 100.00 18.871 8.1473 95.129 
	safe_print(RGB2XYZ(0.0, 0.0, 1.0))
	# 50.000 0.0000 100.00 27.610 12.653 95.538 
	safe_print(RGB2XYZ(0.5, 0.0, 1.0))
	# 100.00 0.0000 100.00 59.701 29.199 97.042 
	safe_print(RGB2XYZ(1.0, 0.0, 1.0))
	# 0.0000 50.000 100.00 26.449 23.302 97.655 
	safe_print(RGB2XYZ(0.0, 0.5, 1.0))
	# 50.000 50.000 100.00 35.189 27.808 98.065 
	safe_print(RGB2XYZ(0.5, 0.5, 1.0))
	# 100.00 50.000 100.00 67.279 44.354 99.568 
	safe_print(RGB2XYZ(1.0, 0.5, 1.0))
	# 0.0000 100.00 100.00 54.276 78.948 106.93 
	safe_print(RGB2XYZ(0.0, 1.0, 1.0))
	# 50.000 100.00 100.00 63.016 83.454 107.34 
	safe_print(RGB2XYZ(0.5, 1.0, 1.0))
