# -*- coding: utf-8 -*-
# @Author: wangjb
# @Date:   2018-02-23 14:44:50
# @Last Modified by:   wangfpp
# @Last Modified time: 2018-03-21 09:15:49
import pygame
from pygame.locals import *
import numpy as np
from sys import exit
import copy
import time

#以下为自用函数
import comb
from createBlock import *
from text import Rotate
rotate = Rotate()

class tetris(object):
	"""docstring for tetris"""
	def __init__(self):#obj 包含画面的宽高 物块的大小等信息
		self.width = 500
		self.begin = True
		self.height = 524
		self.blockWidth = 23
		self.blockHeight = 22
		self.pause = False
		self.SCORE = 0
		self.LINES = 0
		self.LEVEL = 1
		self.speed = 1
		self.background_image = './img/background.jpg'
		self.boomImage = './img/timg.gif'
		self.list_screen = np.zeros((21,10),int)
		self.speed = 0
		self.TEXT = [
			{
				'str' : 'SCORE:  ',
				'val' : self.SCORE,
				'pos' : (302,155)
			},
			{
				'str' : 'LINES:  ',
				'val' : self.LINES,
				'pos' : (302,205)
			},
			{
				'str' : 'LEVEL:  ',
				'val' : self.LEVEL,
				'pos' : (302,255)
			}
		]
		self.Current = copy.deepcopy(self.new_block())
		self.Next = copy.deepcopy(self.new_block())
	def new_block(self):#产生新的物块(包含当前的Current和下一个Next)
		new = createBlock()
		return new.random_block()
	def game_init(self):#游戏初始化
		
		pygame.init()		
		pygame.display.set_caption('俄罗斯方块')
		pygame.key.set_repeat(100)
		
		self.screen = pygame.display.set_mode((self.width,self.height),0,32)
		self.font = pygame.font.SysFont('Arial',24)
		self.background = pygame.image.load(self.background_image).convert()
		self.pygame_init()
		
	def replace_value(self,value):#把方块  替换到游戏区
		array = self.list_screen
		block = self.Current
		shape = block['shape']
		index = block['index']
		x = index[0]
		y = index[1]
		for i,itema in enumerate(shape):
			for j,itemb in enumerate(itema):
				if itemb == 1:
					array[x + i][y + j ] = value
	def delete_value(self):#每次的方块移动删除上一次目标区的内容
		oldblock = copy.deepcopy(self.Current)
		shape = oldblock['shape']
		ox = oldblock['index'][0]
		oy = oldblock['index'][1]
		for i,itema in enumerate(shape):
			for j,itemb in enumerate(itema):
				if self.list_screen[i + ox][j + oy] != 1:
					self.list_screen[i + ox][j + oy] = 0
	def clear(self):#清空填充区
		for i,itema in enumerate(self.list_screen):
			if np.sum(itema == 1) >= 10:
				self.list_screen =  np.delete(self.list_screen,i,0)
				self.list_screen = np.insert(self.list_screen,0,[0,0,0,0,0,0,0,0,0,0],0)
				self.LINES += 1
				self.SCORE = self.LINES * 10
				self.TEXT[0]['val'] = self.LINES * 10
				self.TEXT[1]['val'] = self.LINES
				self.LEVEL = (self.LINES / 20) if (self.LINES / 20 > 0) else 1
				self.TEXT[2]['val'] = self.LEVEL
				#self.boom_effect()
		self.draw_text()
	def boom_effect(self):#消除行的爆炸效果💥
		self.boom = pygame.image.load(self.boomImage).convert()
		self.screen.blit(self.boom, (80,120))
	def draw_line(self):#绘制 游戏区的方框线
		linearray = np.zeros((22,11),int)
		screen = self.screen
		for i,a in enumerate(linearray):
			if i == 0:
				pygame.draw.line(screen,[0,0,0],(15,15),(260,15),1)
			else:
				pygame.draw.line(screen,[0,0,0],(15,i*23.5+15),(260,i*23.5+15),1)
			for j,b in enumerate(a):
				if j == 0:
					pygame.draw.line(screen,[0,0,0],(15,15),(15,510),1)
				else:
					pygame.draw.line(screen,[0,0,0],(j*24.5+15,15),(j*24.5+15,510),1)
	def draw_block(self):#绘制俄罗斯方块  活动的是当前活动的颜色  固定的是黑色
		color = self.Current['color']
		for i,a in enumerate(self.list_screen):
			for j,b in enumerate(a):
				if b == 1:
					pygame.draw.rect(self.screen,[0,0,0],[j*24.5+15.5,i*23.8+15.5,self.blockWidth,self.blockHeight],0)#Surface color rect:[left,top,width,height]		
				elif b == -1:
					pygame.draw.rect(self.screen,color,[j*24.5+15.5,i*23.8+15.5,self.blockWidth,self.blockHeight],0)#Surface color rect:[left,top,width,height]
				elif b != 1 and b != 0 and b != -1:
					pygame.draw.rect(self.screen,[0,0,0],[j*24.5+15.5,i*23.8+15.5,self.blockWidth,self.blockHeight],0)
	def draw_next(self):#绘制下一个 俄罗斯方块
		Next = self.Next
		shape = Next['shape']
		color = Next['color']
		length = len(shape)
		for i,itema in enumerate(shape):
			for j,itemb in enumerate(itema):
				if itemb == 1:
					if length == 1:
						pygame.draw.rect(self.screen,color,[j*24.5+355,i*23.8+40,self.blockWidth,self.blockHeight],0)
					elif length == 2:#xing
						pygame.draw.rect(self.screen,color,[j*24.5+355,i*23.8+40,self.blockWidth,self.blockHeight],0)
					elif length == 3:
						pygame.draw.rect(self.screen,color,[j*24.5+355,i*23.8+25,self.blockWidth,self.blockHeight],0)
					elif length == 4:
						pygame.draw.rect(self.screen,color,[j*24.5+360,i*23.8+20,self.blockWidth,self.blockHeight],0)
					else:
						pass
	def draw_text(self):
		for content in self.TEXT:
			self.screen.blit(self.font.render(comb.comb_str(content['str'],content['val']),True,(88,104,132)),content['pos'])
	def freedom_down(self):
		self.delete_value()
		self.Current['index'][0] += 1
		time.sleep(1)
	def move_down(self):#按向下箭头  控制物块下落 同时进行边缘和碰撞检测		
		shapearr = np.array(self.Current['shape'])
		self_x = np.where(shapearr == 1)[0][len(np.where(shapearr == 1)[0]) - 1]
		#print self_x
		x  = self.Current['index'][0]
		y = self.Current['index'][1]
		if self_x + x > 19 or self.check_vertiacl():
			self.replace_value(1)
			self.Current = copy.deepcopy(self.Next)
			self.Next = self.new_block()
		else:
			self.delete_value()
			self.Current['index'][0] += 1
			self.replace_value(-1)
			self.ratio = time.time()
		
	def check_vertiacl(self):#检测垂直方向上是否有碰撞发生
		for i in range(len(self.list_screen) - 1):
			for j in range(len(self.list_screen[i])):
				if self.list_screen[i][j] == -1 :
					if  self.list_screen[i+1][j] == 1:
						return True
						break
		return False
	def move_up(self):#向上箭头的旋转  其中包含边界条件
		x  = self.Current['index'][0]
		y = self.Current['index'][1]
		rotatearr = rotate.rotateArray(copy.deepcopy(self.Current['shape']))#先旋转一下看是否能够满足不报错
		rotateShape = np.shape(np.array(rotatearr))
		self_y = rotateShape[1]
		self_x = rotateShape[0]
		if (not(y + self_y > 10 or x + self_x > 20)) and self.can_rotate():
			self.delete_value()
			self.Current['shape'] = rotate.rotateArray(self.Current['shape'])
	def can_rotate(self):#判断是否能够旋转
		rotatearr = rotate.rotateArray(copy.deepcopy(self.Current['shape']))#先旋转一下看是否能够满足不报错
		x  = self.Current['index'][0]
		y = self.Current['index'][1]
		for i,itema in enumerate(rotatearr):
			for j,itemb in enumerate(itema):
				if self.list_screen[i + x][j + y] == 1:
					return False
		return True
	def move_left(self):#向左移动
		if (not self.Current['index'][1] <= 0) and self.check_boundary('left'):
			self.delete_value()
			self.Current['index'][1] -= 1
			self.replace_value(-1)
	def move_right(self):#向右移动
		shapearr = np.array(self.Current['shape'])
		self_y =  shapearr.shape[1]
		if (not self.Current['index'][1] + self_y >= 10) and self.check_boundary('right') :
			self.delete_value()
			self.Current['index'][1] += 1
			self.replace_value(-1)
	def check_boundary(self,direct):
		for i in range(len(self.list_screen)):
			for j in range(len(self.list_screen[i]) - 1):
				if self.list_screen[i][j] == -1 :
					if direct == 'right':
						if  self.list_screen[i][j + 1] == 1:
							return False
							break
					else:
						if  self.list_screen[i][j - 1] == 1:
								return False
								break
		return True
	def pygame_init(self):
		#pygame.event.set_allowed([KEYDOWN])
		self.old = time.time()
		while self.begin:
			self.screen.blit(self.background,(0,0))
			self.replace_value(-1)
			self.draw_block()
			self.draw_line()
			self.draw_next()
			self.draw_text()
			if not self.pause:
				if self.speed - self.old > (1 - self.LEVEL * 0.07):
					self.move_down()
					self.old = time.time()
				else:
					self.speed = time.time()
			for event in pygame.event.get():
				if event.type == QUIT:
					exit()	
				if event.type == VIDEORESIZE:
					SCREEN_SIZE = event.size
					self.screen =  pygame.display.set_mode(SCREEN_SIZE, RESIZABLE)
				if event.type == KEYDOWN:
					if not self.pause:
						if event.key == K_DOWN:
							self.move_down()
						elif event.key == K_UP:
							self.move_up()
						elif event.key == K_LEFT:
							self.move_left()
						elif event.key == K_RIGHT:
							self.move_right()
					if event.key == K_p:
						self.pause = not self.pause
					elif event.key == K_q:
						self.begin = False
					elif event.key == K_r:
						self.__init__()
			self.clear()
			pygame.display.update()
if __name__ == '__main__':
	game = tetris()
	game.game_init()








 













