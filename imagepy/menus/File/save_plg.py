# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 03:19:13 2016
@author: yxl
"""
from sciapp.action import dataio
from sciapp.action import Simple

class SaveImage(dataio.ImageWriter):
	title = 'Save'

	def load(self, ips):
		self.filt = [i for i in sorted(dataio.WriterManager.names())]
		return True

class WindowCapture(dataio.ImageWriter):
	title = 'Save With Mark'
	filt = ['PNG']

	def run(self, ips, imgs, para = None):
		self.app.get_img_win().canvas.save_buffer(para['path'])

plgs = [SaveImage, WindowCapture]