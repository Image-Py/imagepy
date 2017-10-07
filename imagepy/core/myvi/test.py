import sys, wx
sys.path.append('..')
from scipy.misc import imread
import scipy.ndimage as ndimg
import numpy as np
from glob import glob
import threading
import myvi

def dem(frm):
	
	img = imread('C:/Users/Administrator/Desktop/dem.png')
	vts, fs, ns, cs = myvi.util.build_surf2d(img, lut=None, ds=1, k=0.3, sigma=2)
	frm.add_obj_ansy('dem', vts, fs, ns, cs)
	
	
	vts, fs, ns, cs = myvi.util.build_balls([(100,100,100)],[50], [(1,0,0)])
	frm.add_obj_ansy('balls', vts, fs, ns, cs)
	
	'''
	fs = glob('C:/Users/Administrator/Desktop/ipygl/imgs/*.png')
	imgs = np.array([imread(i, True) for i in fs])
	imgs = ndimg.gaussian_filter(imgs, 1)
	vts, fs, ns, vs = myvi.build_surf3d(imgs, 128, step=1)
	print(vts.shape, fs.shape, ns.shape, vs.shape)
	frm.add_obj_ansy('volume', vts, fs, ns, (1,0,0))
	'''

if __name__ == '__main__':
	app = wx.App(False)
	frm = myvi.GLFrame.get_frame(None, title='GLCanvas Sample')
	t = threading.Thread(target=dem,args=(frm,))
	t.setDaemon(True)
	t.start()
	app.MainLoop()