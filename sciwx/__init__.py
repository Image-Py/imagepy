from sciapp import Source
import numpy as np

import matplotlib.pyplot as plt
for i in plt.colormaps()[::-1]:
	cm = plt.get_cmap(i)
	if i[-2:]=='_r': continue
	vs = np.linspace(0, cm.N, 256, endpoint=False)
	lut = cm(vs.astype(np.int), bytes=True)[:,:3]
	Source.manager('colormap').add(i, lut)
graylut = Source.manager('colormap').get('gray')
Source.manager('colormap').add('Grays', graylut)
Source.manager('colormap').remove('gray')