from imagepy.core.engine import Free
import numpy as np
from imagepy import IPy
import wx

import matplotlib
#matplotlib.use('WXAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

class AddMultiply(Free):
	title = 'Orignal Line'
	asyn = False


	def run(self, para = None):
		xs = [1,2,3,4,5,6,7,8,9,10]
		ys = np.array([30,57,93,105,110,117,108,87,52,39])
		l1 = plt.plot(xs, ys, '-o', label='orignal')
		l2 = plt.plot(xs, ys+100, '-o', label='add')
		l3 = plt.plot(xs, ys*2, '-o', label='multiply')
		plt.grid()
		plt.title('Math Operator')
		plt.gca().set_ylim(0,255)
		plt.gca().legend()
		plt.show()

		ori = np.zeros((10,30,30), dtype=np.uint8)
		add = np.zeros((10,30,30), dtype=np.uint8)
		mul = np.zeros((10,30,30), dtype=np.uint8)
		ori.T[:], add.T[:], mul.T[:] = ys, ys+100, ys*2

		#area = (area-5) * 8
		IPy.show_img([np.hstack(ori)], 'Orignal Line')
		IPy.show_img([np.hstack(add)], 'Add 100')
		IPy.show_img([np.hstack(mul)], 'Multiply 2')
		
class Extend(Free):
	title = 'Extend Full'
	asyn = False


	def run(self, para = None):
		xs = [0, 30, 117, 255]
		ys = [0, 0,  255, 255]
		data = np.array([30,57,93,105,110,117,108,87,52,39])
		l1 = plt.plot(xs, ys, 'r', lw=3)
		plt.grid()
		plt.title('y = 2.931 * x - 87.931')
		plt.gca().set_ylim(0,256)
		plt.gca().set_xlim(0,256)
		plt.figure()
		plt.grid()
		xs = [1,2,3,4,5,6,7,8,9,10]
		ys = np.round(data * 2.931 - 87.931)
		l1 = plt.plot(xs, ys, '-o')
		plt.show()

		data = np.array([30,57,93,105,110,117,108,87,52,39])
		ori = np.zeros((10,30,30), dtype=np.uint8)
		ori.T[:] = np.round(data * 2.931 - 87.931)

		#area = (area-5) * 8
		IPy.show_img([np.hstack(ori)], 'Extend')

class Surface(Free):
	title = '3D Surface'
	asyn = False


	def run(self, para = None):
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		X, Y, Z = axes3d.get_test_data(0.05)
		ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
		plt.show()

		#area = (area-5) * 8
		IPy.show_img([(Z+80).astype(np.uint8)], '3D Surface')

class Garmma(Free):
	title = 'Garmma Curve'
	asyn = False

	def run(self, para = None):
		xs = np.linspace(0,1,100)
		ks = [0.5, 0.8, 1, 1.2, 1.5]
		ys = [xs ** i for i in ks]

		for i in (0,1,2,3,4):
			plt.plot(xs, ys[i], '-', label='k=%s'%ks[i])
		plt.grid()
		plt.title('Garmma Function')
		plt.gca().legend()
		plt.show()

plgs = [AddMultiply, Extend, Surface, '-', Garmma]