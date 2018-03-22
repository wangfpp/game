# -*- coding: utf-8 -*-
# @Author: wangjb
# @Date:   2018-02-23 16:56:24
# @Last Modified by:   wangjb
# @Last Modified time: 2018-03-22 11:38:17

import numpy as np
import random
import copy

t = {
		'shape' : [[0,1,0],
				   [1,1,1]],
		'color' : ''
	}
l = {
		'shape' : [
					[1,0],
					[1,0],
					[1,1]
				]
	}
j = {
		'shape' : [
					[0,1],
					[0,1],
					[1,1]
				]
	}
o = {
		'shape' : [
					[1,1],
					[1,1]
				]
	}
z = {
		'shape' : [
					[1,1,0],
					[0,1,1]
				]
	}
i = {
		'shape' : [
					[1],
					[1],
					[1],
					[1]
				]
	}
y = {
		'shape' : [
					[1,1,1,1]
				]
	}
shape = [t,l,j,o,z,i,y]
color = [
	[193,59,253],
	[252,249,41],
	[104,243,18],
	[239,139,38],
	[227,57,192],
	[14,25,152],
	[117,49,247],
	[209,81,68]
]
class createBlock(object):
	"""docstring for createBlock"""
	def __init__(self):
		self.shape = shape
		self.color = color
	def random_block(self):
		num = int(random.random()*6)
		self.shape[num]['color'] = color[num]
		self.shape[num]['index'] = [0,4]#x y第几列第几行
		random_shape = self.shape[num]
		return copy.deepcopy(random_shape)



		

