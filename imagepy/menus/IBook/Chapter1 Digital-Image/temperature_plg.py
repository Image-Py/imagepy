from imagepy.core.engine import Free
import numpy as np
from imagepy import IPy
import wx

import matplotlib
#matplotlib.use('WXAgg')
import matplotlib.pyplot as plt

class Plugin(Free):
	title = 'Chengdu Temperature'
	asyn = False


	def run(self, para = None):
		xs = [1,2,3,4,5,6,7,8,9,10,11,12]
		ys = [10,12,16,22,26,28,30,30,25,21,16,11]
		lbs = ['Jan','Feb','Mar','Apr','May','June',
		       'Jul','Aug','Sep','Oct','Nov','Dec']
		plt.xticks(xs, lbs)

		plt.plot(xs, ys, '-o')
		plt.grid()

		plt.title('Temperature in ChengDu')
		plt.xlabel('Month')
		plt.ylabel('Temperature (C)')

		plt.show()

		area = np.zeros((12,30,30), dtype=np.uint8)
		temp = np.array([10,12,16,22,26,28,30,30,25,21,16,11])
		area.T[:] = temp
		area = (area-5) * 8
		IPy.show_img([np.hstack(area)], 'Chengdu Temperature')
		