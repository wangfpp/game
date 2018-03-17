# -*- coding: utf-8 -*-
# @Author: wangjb
# @Date:   2018-03-01 11:46:42
# @Last Modified by:   wangjb
# @Last Modified time: 2018-03-16 19:58:09
import numpy as np
import time
class Rotate(object):
	"""docstring for ClassName"""
	def __init__(self):
		pass	
	def rotateArray(self,arr):#输入一个数组进行旋转  应该添加direct
		row = np.shape(arr)[0]
		col = np.shape(arr)[1]
		newarr = np.zeros((col,row))
		for i in range(len(arr)):
			for j in range(len(arr[i])):
				newarr[j][len(arr) - 1 - i] = arr[i][j]
		return newarr














