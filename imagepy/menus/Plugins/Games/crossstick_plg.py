from sciapp.action import Filter
import numpy as np 
from scipy.cluster.vq import kmeans, vq

class Plugin(Filter):
	title = 'Cross Stick'

	note = ['rgb', 'not_channel', 'auto_msk', 'auto_snap', 'preview']
	para = {'block':8, 'k':12, 'grid':False}

	view = [(int, 'k', (1,100), 0,  'k', ''),
			(int, 'block', (5, 50), 0,  'block', ''),
			(bool, 'grid', 'show grid')]

	def run(self, ips, snap, img, para = None):
		k, block = para['k'], para['block']
		buf = snap[::block,::block].copy()
		pts = buf.reshape((-1,3)).astype(np.float32)
		ms = kmeans(pts, k)[0]
		buf[:] = ms[vq(pts, ms)[0]].reshape(buf.shape)
		xs, ys = np.where(img[:,:,0]>-1)
		img[xs, ys] = buf[xs//block, ys//block]
		if para['grid']: 
			img[::block], img[:,::block] = 0, 0