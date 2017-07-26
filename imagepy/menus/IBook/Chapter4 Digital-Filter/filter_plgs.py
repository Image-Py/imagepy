from imagepy.core.engine import Free
import scipy.ndimage as ndimg
import numpy as np, wx
from imagepy import IPy
#matplotlib.use('WXAgg')
import matplotlib.pyplot as plt

def block(arr):
	img = np.zeros((len(arr),30,30), dtype=np.uint8)
	img.T[:] = arr
	return np.hstack(img)

class Temperature(Free):
	title = 'Temperature Difference'
	asyn = False

	def run(self, para = None):
		xs = np.array([1,2,3,4,5,6,7,8,9,10,11,12])
		ys = np.array([1,2,1,2,2,3,8,9,8,10,9,10], dtype=np.float32)
		ds = ndimg.convolve1d(ys, [0,1,-1])
		lbs = ['Jan','Feb','Mar','Apr','May','June',
		       'Jul','Aug','Sep','Oct','Nov','Dec']
		plt.xticks(xs, lbs)

		plt.plot(xs, ys, '-o', label='Temperature')
		plt.plot(xs, ds, '-o', label='Difference')
		plt.grid()
		plt.gca().legend()

		plt.title('Temperature in XX')
		plt.xlabel('Month')
		plt.ylabel('Temperature (C)')

		plt.show()
		IPy.show_img([block((ys-ys.min())*(180/ys.max()-ys.min()))], 'Temperature')
		IPy.show_img([block((ds-ds.min())*(180/ds.max()-ds.min()))], 'Difference')

class Shake(Free):
	title = 'Shake Damping'
	asyn = False

	def run(self, para = None):
		xs = np.array([1,2,3,4,5,6,7,8,9,10])
		ys = np.array([10,-9,8,-7,6,-5,4,-3,2,-1], dtype=np.float32)
		ds = ndimg.convolve1d(ys, [1/3,1/3,1/3])
		print(ds)
		plt.plot(xs, ys, '-o', label='Shake')
		plt.plot(xs, ds, '-o', label='Damping')
		plt.grid()
		plt.gca().legend()

		plt.title('Shake Damping')
		plt.xlabel('Time')
		plt.ylabel('Amplitude')
		plt.show()
		IPy.show_img([block(ys*10+128)], 'Shake')
		IPy.show_img([block(ds*10+128)], 'Damping')

class Inertia(Free):
	title = 'Psychological Inertia'
	asyn = False

	def run(self, para = None):
		xs = np.array([1,2,3,4,5,6,7,8,9,10])
		ys = np.array([90,88,93,95,91,70,89,92,94,89], dtype=np.float32)
		ds = ndimg.convolve1d(ys, [1/3,1/3,1/3])
		print(ds)
		plt.plot(xs, ys, '-o', label='Psychological')
		plt.plot(xs, ds, '-o', label='Inertia')
		plt.grid()
		plt.gca().legend()

		plt.title('Psychological Inertia')
		plt.xlabel('Time')
		plt.ylabel('Score')
		plt.show()
		IPy.show_img([block((ys-80)*3+80)], 'Psychological')
		IPy.show_img([block((ds-80)*3+80)], 'Inertia')

plgs = [Temperature, Shake, Inertia]