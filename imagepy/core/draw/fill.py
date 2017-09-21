# -*- coding: utf-8 -*-
import numpy as np
from scipy.ndimage import label, generate_binary_structure

def floodfill(img, x, y, thr, con):
	color = img[int(y), int(x)]
	buf = np.subtract(img, color, dtype=np.int16)
	msk = np.abs(buf)<=thr
	if buf.ndim==3:
		msk = np.min(msk, axis=2)
		buf = buf[:,:,0]
	strc = generate_binary_structure(2, con+1)
	label(msk, strc, output = buf)
	msk = buf == buf[int(y), int(x)]
	#msk[[0,-1],:], msk[:,[0,-1]] = 0, 0

	#imsave('test.png', msk.astype(np.uint8))
	
	return msk