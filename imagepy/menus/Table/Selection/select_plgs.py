from sciapp.action import Table
import pandas as pd
import numpy as np

class Select(Table):
	title = 'Sel By C Name R Count'

	para = {'cn':[], 'call':False, 'r1':0, 'r2':0, 'rall':False}
	view = [('fields', 'cn', 'fields'),
			(bool, 'call', 'all columns'),
			('any', 'r1', 'start rows'),
			('any', 'r2', 'end rows'),
			(bool, 'rall', 'all rows')]

	def run(self, tps, snap, data, para=None):
		if not para['call']:
			cmsk = para['cn']
		else: cmsk=[]
		if not para['rall']:
			rmsk = data.index[slice(para['r1'], para['r2'])]
		else: rmsk=[]
		print(para)
		print('plugins', rmsk, cmsk)
		tps.select(rmsk, cmsk)

plgs = [Select]