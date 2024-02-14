from sciapp import Manager
import numpy as np

ColorManager = Manager()
import matplotlib.pyplot as plt
for i in plt.colormaps()[::-1]:
	cm = plt.get_cmap(i)
	if i[-2:]=='_r': continue
	vs = np.linspace(0, cm.N, 256, endpoint=False)
	lut = cm(vs.astype(np.uint8), bytes=True)[:,:3]
	ColorManager.add(i, lut)
del plt
graylut = ColorManager.get('gray')
ColorManager.add('Grays', graylut)
ColorManager.remove('gray')