from imagepy.core.engine import Filter
from imagepy import IPy
import numpy as np 
from scipy.cluster.vq import kmeans, vq
class K_mean(Filter):
	title = 'K-Mean'
	note = ['all','2float', 'not_channel','auto_msk', 'auto_snap','preview']
	para = {'k':8,'iter':20,'thresh':1e-5}
	view = [(int, 'k', (1,99999), 0,  'k', ''),
		(int, 'iter', (0,99999), 0,  'iter', ''),
        (float, 'thresh', (0,99999), 10,  'thresh', '')]
	def run(self, ips, snap, img, para = None):
                pts = snap.reshape((-1,(1,3)[snap.ndim-2]))
                ms = kmeans(pts.astype(np.float32), para['k'],para['iter'],para['thresh'])[0]
                img[:] = ms[vq(pts, ms)[0]].reshape(img.shape)

plgs = [K_mean]
