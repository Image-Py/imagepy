# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 05:43:50 2016
@author: yxl
"""
from sciapp.action import Free

class Plugin(Free):
	title = 'Exit'
	asyn = False

	def run(self, para = None):
		self.app.Close()