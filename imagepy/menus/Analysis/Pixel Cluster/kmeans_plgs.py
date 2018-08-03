from imagepy.core.engine import Filter
from imagepy import IPy
import numpy as np 
from scipy.cluster.vq import kmeans, vq

class K_mean(Filter):
	title = 'K-Means'

	note = ['all', 'not_channel', 'auto_msk', 'auto_snap', 'preview']
	para = {'k':8, 'iter':20, 'ds':2, 'thresh':1e-5}

	view = [(int, 'k', (1,100), 0,  'k', ''),
			(int, 'iter', (1, 50), 0,  'iterate', ''),
			(float, 'thresh', (0, 1), 5,  'threshold', ''),
			(int, 'ds', (1, 50), 0,  'resample', ''),]

	def run(self, ips, snap, img, para = None):
		pts = snap.reshape((-1,(1,3)[snap.ndim-2]))
		ms = kmeans(pts[::para['ds']**2].astype(np.float32), 
			para['k'],para['iter'],para['thresh'])[0]
		img[:] = ms[vq(pts, ms)[0]].reshape(img.shape)

plgs = [K_mean]
