from sciapp.action import Table
import pandas as pd
import numpy as np
from scipy import signal
import scipy.ndimage as nimg

class Statistic(Table):
	title = 'Signal Uniform Filter'
	note = ['auto_snap', 'only_num', 'auto_msk', 'preview']

	para = {'size':2}
		
	view = [(int, 'size', (0,30), 0, 'size', '')]

	def run(self, tps, snap, data, para=None):
		for s in snap.columns:
			data[s] = nimg.uniform_filter(snap[s], para['size'])

plgs = [Statistic]