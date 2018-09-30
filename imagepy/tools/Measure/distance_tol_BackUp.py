# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 22:21:32 2017

@author: yxl
"""

import wx
from imagepy.core.engine import Tool
import numpy as np
import pandas as pd
from numpy.linalg import norm
from .setting import Setting
from imagepy import IPy

class Distance:
	"""Define the distance class"""
	dtype = 'distance'
	def __init__(self, body=None, unit=None):
		self.body = body if body!=None else []
		self.buf, self.unit = [], unit

	def addline(self):
		line = self.buf
		self.body = []
		curLine = []
		if len(line)!=2 or line[0] !=line[-1]:
			for i in line:
					if i[0] !=-1 and i[1]!=-1:
						curLine.append(i)
					else:
						self.body.append(curLine)
						curLine=[]
			
		# self.buf = []

	def snap(self, x, y, lim):
		minl, idx = 1000, None
		for i in self.body:
			for j in i:
					d = (j[0]-x)**2+(j[1]-y)**2
					if d < minl:minl,idx = d,(i, i.index(j))
		return idx if minl**0.5<lim else None

	def pick(self, x, y, lim):
		return self.snap(x, y, lim)

	def draged(self, ox, oy, nx, ny, i):
		i[0][i[1]] = (nx, ny)

	def draw(self, dc, f, **key):
		dc.SetPen(wx.Pen(Setting['color'], width=1, style=wx.SOLID))
		dc.SetTextForeground(Setting['tcolor'])

		font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
		dc.SetFont(font)

		if self.buf:
			line = self.buf
			curLine = []
			if len(line)!=2 or line[0] !=line[-1]:
					for i in line:
						if i[0] !=-1 and i[1]!=-1:
							curLine.append(i)
							dc.DrawCircle(f(*i),2)
						else:
							# self.body.append(curLine)
							# print('curLine:{}'.format(i))
							if len(curLine) >1:
								dc.DrawLines([f(*i) for i in curLine if i[0] != -1 ])
								curLine=[]
		# dc.DrawLines([f(*i) for i in self.buf)
		# for i in self.buf:
		#     if i[0]!=-1 and i[1] != -1:
		#         dc.DrawCircle(f(*i),2)
		# print('current pixel ratio is:{}'.format(Setting['ratioRuler']))
		self.unit = Setting['ratioRuler']

		print('body:{}'.format(len(self.body)))
		for line in self.body:
			tempDist = 0
			# print('line:{}'.format(line))
			if len(line) <=1 or line[0] == -1 and line[-1]== -1:
				continue		
			dc.DrawLines([f(*i) for i in line ])

			for i in line:dc.DrawCircle(f(*i),2)
			pts = np.array(line)
			mid = (pts[:-1]+pts[1:])/2
			
			midPnt = np.median( pts, axis=1)
			
			dis = norm((pts[:-1]-pts[1:]), axis=1)
			# unit = 1 if self.unit is None else self.unit[0]
			unit = 1 if self.unit is None else self.unit

			for i,j in zip(dis, mid):
					tempDist += i
					if j[0]>6:
						j-=5
					if i <=0:
						continue
					dc.DrawText('%.2f'%(i * unit), f(*j))

			font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
			dc.SetFont(font)    
			dc.DrawText('%.2f mm'%(tempDist * unit), f(midPnt[0],midPnt[1]))
			
	def report(self, title):
		rst = []
		for line in self.body:
			pts = np.array(line)
			dis = norm((pts[:-1]-pts[1:]), axis=1)
			dis *= 1 if self.unit is None else self.unit
			rst.append(list(dis.round(2)))
		lens = [len(i) for i in rst]
		maxlen = max(lens)
		fill = [[0]*(maxlen-i) for i in lens]
		rst = [i+j for i,j in zip(rst, fill)]
		titles = ['L{}'.format(i+1) for i in range(maxlen)]
		# searchTitle = [1, len(self.body)]
		IPy.show_table(pd.DataFrame(rst, columns=titles), title)
	def updateReport(self, title):
		data = IPy.get_tps().data
		tempbuf = []
		self.buf = []
		for indexs in data.index:
			print('cur index:{}'.format(indexs))
			# temp = list(filter(lambda a: a != 0.0, data.loc[indexs].values[0:-1]))
			tempbuf.append(self.body[indexs][:])
			print('tempbuf:{}'.format(self.body[indexs]))
			tempbuf.append([(-1,-1)])
		for i in range(len(tempbuf)):
			for x in  range(len(tempbuf[i])):
				self.buf.append(tempbuf[i][x] )

		# self.buf = [ tempbuf[i][x] for x in len(tempbuf[i]) for i in len(tempbuf)]
		print('buf:{}'.format(self.buf))

		self.addline()

		# rst = []
		# for line in self.body:
		# 	pts = np.array(line)
		# 	dis = norm((pts[:-1]-pts[1:]), axis=1)
		# 	dis *= 1 if self.unit is None else self.unit
		# 	rst.append(list(dis.round(2)))
		# lens = [len(i) for i in rst]
		# maxlen = max(lens)
		# fill = [[0]*(maxlen-i) for i in lens]
		# rst = [i+j for i,j in zip(rst, fill)]
		# titles = ['L{}'.format(i+1) for i in range(maxlen)]
		# # searchTitle = [1, len(self.body)]
		# IPy.show_table(pd.DataFrame(rst, columns=titles), title)

class Plugin(Tool):
	"""Define the diatance class plugin with the event callback functions"""
	title = 'Distance'
	def __init__(self):
		self.curobj = None
		self.doing = False
		self.odx,self.ody = 0, 0

	def mouse_down(self, ips, x, y, btn, **key):

		if key['shift'] and isinstance(ips.mark, Distance):
			ips.mark.updateReport(ips.title)

		if key['ctrl'] or key['alt']:
			print('key mouse_down:{}'.format(key))	
			print('table in')
			if isinstance(ips.mark, Distance):
					ips.mark.report(ips.title)
					
			return

		lim = 5.0/key['canvas'].get_scale()
		if btn==1:
			if not self.doing:
				if isinstance(ips.mark, Distance):
					self.curobj = ips.mark.pick(x, y, lim)
				# if self.curobj!=None:return						
				if not isinstance(ips.mark, Distance):
					ips.mark = Distance(unit=ips.unit)
					self.doing = True
					print('A new Distance instance is added!')
				elif key['shift']:
					self.doing = True
				else:
					x = 1
						# ips.mark = None
					# if not isinstance(ips.mark, Distance):
					#     ips.mark = Distance(unit=ips.unit)
					#     self.doing = True
					#     print('A new Distance instance is added!')
					# elif key['shift']:
					#     self.doing = True
					# else: ips.mark = None
			if self.doing:
				ips.mark.buf.append((x,y))
				self.curobj = (ips.mark.buf, -1)
				self.odx, self.ody = x,y

		elif btn==3: ### btn == 3 代表是右键被按下；
			print('Right bottom is pushed!')
			if self.doing:
					ips.mark.buf.append((x,y))
					ips.mark.buf.append((-1,-1))
					lineNum = [i for i,x in enumerate(ips.mark.buf) if x == (-1,-1)]
					# self.doing = False
					ips.mark.addline()
		ips.update = True

	def mouse_up(self, ips, x, y, btn, **key):
		# self.curobj = None
		print('mouse is up!')

	def mouse_move(self, ips, x, y, btn, **key):
		if not isinstance(ips.mark, Distance):return
		lim = 5.0/key['canvas'].get_scale()
		if btn==None:
			self.cursor = wx.CURSOR_CROSS
			if ips.mark.snap(x, y, lim)!=None:
					self.cursor = wx.CURSOR_HAND
		elif btn==1:
			if self.curobj is not None:
					ips.mark.draged(self.odx, self.ody, x, y, self.curobj)
			ips.update = True
		self.odx, self.ody = x, y

	def mouse_wheel(self, ips, x, y, d, **key):
		pass
