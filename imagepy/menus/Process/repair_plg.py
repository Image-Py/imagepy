from sciapp.action import Filter
import numpy as np
import scipy.ndimage as ndimg
from imagepy.ipyalg import distance_transform_edt

class Plugin(Filter):
	title = 'Fragment Repair'
	note = ['all', 'req_roi', 'auto_msk', 'auto_snap', 'preview']
	para = {'mode':'nearest'}
	view = [(list, 'mode', ['nearest', 'mean'], str, 'replace by', 'pix')]

	def run(self, ips, snap, img, para = None):
		msk = ips.mask()
		if self.para['mode']=='nearest':
			rr, cc = ndimg.distance_transform_edt(msk, return_distances=False, return_indices=True)
			img[:] = snap[rr, cc]
		else: 
			lab1, n = ndimg.label(msk)
			lab2 = ndimg.maximum_filter(lab1, 3)
			idx = ndimg.mean(img, lab2-lab1, np.arange(1,n+1))
			img[msk] = idx[lab1[msk]-1]