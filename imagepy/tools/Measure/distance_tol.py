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

import itertools
import six
import copy

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
	def delLine(self, x, y):
		lines = self.buf

		# 先将 线段 切块；
		# 再 计算每个线段和 点击点的位置
		# 如果 点距离线段的距离 小于 0.3， 则删除这个点
		tempList = []
		for i in range(len(lines)):
			tempList.append((lines[i][0]-x , lines[i][1]-y ))


		absDist = [ (np.abs(i[0]) + np.abs(i[1])) for i in tempList ]

		pntPos = np.argmin(absDist)

		if absDist[pntPos] > 10:
			return

		blockIndex = [ i for i,j in enumerate(lines) if j==(-1,-1) ]

		blockIndex.insert(0,0)

		blockIndex3 = [ i-pntPos for i in blockIndex]

		# print('blockIndex3:{}\n'.format(blockIndex3))

		blockIndex2 = [ blockIndex3[i] * blockIndex3[i+1] <= 0   for i,j in enumerate(blockIndex3[:-1])]

		# print('blockIndex2:{}\n'.format(blockIndex2))


		curIndex = 0
		if blockIndex2:
			curIndex = np.argmax(blockIndex2)

		# print('curIndex:{}\n'.format(curIndex))
		# print('before self.body:{}\n',self.body)
		
		if  blockIndex2:
			startIndexToDelete = blockIndex[curIndex]
		else:
			startIndexToDelete = -1

		tempBody = copy.deepcopy(self.buf)

		# print('before tempBody:{}\n',tempBody)
		# print('before self.body:{}\n',self.buf)
		# print('startIndexToDelete:{}\n',startIndexToDelete)

		removedIndex = []
		for i, j in enumerate(self.buf):
			if i >= startIndexToDelete and j[0] != -1:
				removedIndex.append(i)
				if self.buf[i+1][0] == -1:
					removedIndex.append(i+1)
					break

		curBody = [ y for i,y in enumerate(self.buf) if i not in removedIndex ] 
		
		self.buf = curBody
		self.addline()


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

		if self.buf:
			line = self.buf
			curLine = []
			if len(line)!=2 or line[0] !=line[-1]:
					for i in line:
						if i[0] !=-1 and i[1]!=-1:
							curLine.append(i)
							dc.DrawCircle(f(*i),2)
						else:
							if len(curLine) >1:
								dc.DrawLines([f(*i) for i in curLine if i[0] != -1 ])
								curLine=[]

		self.unit = Setting['ratioRuler']

		font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
		dc.SetFont(font)
		dc.SetTextForeground(Setting['tcolor'])

		for line in self.body:
			tempDist = 0
			if len(line) <=1 or line[0] == -1 and line[-1]== -1:
				continue		

			dc.DrawLines([f(*i) for i in line ])

			for i in line : dc.DrawCircle(f(*i),2)

		  	# if g_DebugMode == True:
			# 	print('line:{}'.format(line))

			pts = np.array(line)
			mid = (pts[:-1]+pts[1:])/2
			midPnt =  (pts[-1]+pts[0]+(20,20))/2

			dis = norm((pts[:-1]-pts[1:]), axis=1)
			unit = 1 if self.unit is None else self.unit

			for i,j in zip(dis, mid):
					tempDist += i
					if j[0]>6:
						j-=5
					if i <=0:
						continue
					dc.DrawText('%.2f'%(i * unit), f(*j))

			font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
			# dc.SetTextForeground(Setting['hcolor'])
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
		
		lineTitle = ['{}'.format(i+1) for i in range(len(self.body))]
		newLine = [list(row) for row in six.moves.zip_longest(*rst, fillvalue=0.0)]

		IPy.show_table(pd.DataFrame(newLine, columns=lineTitle), title)

	def updateReport(self, title):
		if not (IPy.get_tps()):
			return
		data = IPy.get_tps().data
		tempbuf = []
		self.buf = []
		for indexs in range(len(data.columns.values.tolist())):
			
			tempIndex = int(data.columns[indexs])
			print('cur index:{}'.format(tempIndex))

			tempbuf.append(self.body[tempIndex][:])
			print('tempbuf:{}'.format(self.body[tempIndex]))
			tempbuf.append([(-1,-1)])

		for i in range(len(tempbuf)):
			for x in  range(len(tempbuf[i])):
				self.buf.append(tempbuf[i][x] )
		self.addline()

class Plugin(Tool):
	"""Define the diatance class plugin with the event callback functions"""
	title = 'Distance'
	def __init__(self):

		self.curobj = None
		self.doing = False
		self.odx,self.ody = 0, 0
		self.list_items = ['del', 'copy','move']
		self.popUpMenuInitialized = False
	
	def mouse_down(self, ips, x, y, btn, **key):

		if key['shift'] and isinstance(ips.mark, Distance):
			print('updateReport!')
			ips.mark.updateReport(ips.title)

		if key['ctrl'] and key['alt']:
			# print('key mouse_down:{}'.format(key))	
			# print('table in')
			if isinstance(ips.mark, Distance):
					ips.mark.report(ips.title)
			return

		lim = 5.0/key['canvas'].get_scale()
		if btn==1:# 按下了左键
			if not self.doing:
				if isinstance(ips.mark, Distance):
					self.curobj = ips.mark.pick(x, y, lim)
				if not isinstance(ips.mark, Distance):
					ips.mark = Distance(unit=ips.unit)
					self.doing = True
					print('A new Distance instance is added!')
				elif key['shift']:
					self.doing = True
				else:
					x = 1

			if self.doing:
				ips.mark.buf.append((x,y))
				self.curobj = (ips.mark.buf, -1)
				self.odx, self.ody = x, y

		elif btn==3: ### btn == 3 代表是右键被按下；
			# print('Right bottom is pushed!')
			if self.doing:
					# ips.mark.buf.append((x,y))
					ips.mark.buf.append((-1,-1))
					lineNum = [i for i,x in enumerate(ips.mark.buf) if x == (-1,-1)]
					ips.mark.addline()
		elif btn==2:
			if key['shift']:
				if isinstance(ips.mark, Distance):
					self.curobj = ips.mark.pick(x, y, lim)
					# ips.mark.buf.append((x,y))
					# self.odx, self.ody = x, y
					ips.mark.delLine(x,y)

				# if not self.popUpMenuInitialized:
				# 	self.popUpInit(**key)
				# 	self.popUpMenuInitialized  = True
				# self.OnContextMenu(**key)
		ips.update = True

	def mouse_up(self, ips, x, y, btn, **key):
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

	def OnContextMenu(self, **key):
		print("OnContextMenu\n")

		# only do this part the first time so the events are only bound once
		#
		# Yet another anternate way to do IDs. Some prefer them up top to
		# avoid clutter, some prefer them close to the object of interest
		# for clarity. 
		if not hasattr(self, "popupID1"):

			self.popupID1 = wx.NewId()
			self.popupID2 = wx.NewId()
			self.popupID3 = wx.NewId()

			self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
			self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
			self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
	
		# make a menu
		menu = wx.Menu()
		# Show how to put an icon in the menu
		item = wx.MenuItem(menu, self.popupID1,"Del Current Line")
		# bmp = images.Smiles.GetBitmap()
		# item.SetBitmap(bmp)
		menu.AppendItem(item)
		# add some other items
		menu.Append(self.popupID2, "Two")
		menu.Append(self.popupID3, "Three")

		# Popup the menu.  If an item is selected then its handler
		# will be called before PopupMenu returns.
		key['canvas'].PopupMenu(menu)
		menu.Destroy()

	def OnPopupOne(self, event):
		print("Popup one\n")


	def OnPopupTwo(self, event):
		print("Popup two\n")

	def OnPopupThree(self, event):
		print("Popup three\n")
