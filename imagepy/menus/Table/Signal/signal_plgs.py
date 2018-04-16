from imagepy.core.engine import Table
import pandas as pd
import numpy as np
from scipy import signal
import scipy.ndimage as nimg

class Statistic(Table):
	title = 'Signal Uniform Filter'
	note = ['snap', 'only_num', 'col_msk', 'preview']

	para = {'size':2}
		
	view = [(int, (0,30), 0, 'size', 'size', '')]

	def run(self, tps, data, snap, para=None):
		for s in snap.columns:
			data[s] = nimg.uniform_filter(snap[s], para['size'])
			#signal.order_filter(snap[s], np.ones(para['r']*2+1), n)
		#IPy.table(tps.title+'-statistic', pd.DataFrame(rst))

plgs = [Statistic]