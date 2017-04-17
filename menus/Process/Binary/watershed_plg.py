# -*- coding: utf-8 -*-
from core.engines import Filter
from skimage.morphology import watershed
from skimage.feature import peak_local_max
import numpy as np
from scipy.ndimage import label
import wx

'''
class Plugin(Filter):
    title = 'Watershed Abs'
    note = ['8-bit', 'preview']
    
    para = {'thr':128}
    view = [('slide', (0,255), 'Threshold', 'thr', '')]
        
    def load(self, ips):
    	self.buf = np.zeros(ips.size, dtype=np.uint16)
        self.lut = ips.lut
        ips.lut = self.lut.copy()
        return True
        
    def preview(self, para):
        self.ips.lut[:] = self.lut
        self.ips.lut[para['thr']:] = [255,0,0]
        self.ips.update = 'pix'
        
    #process
    def run(self, ips, snap, img, para = None):
        ips.lut = self.lut
        label(img>para['thr'], np.ones((3,3)), output = self.buf)
        img[:] = watershed(-img, self.buf, mask = img, watershed_line=True)
        img[img>0] = 255
'''
class Mark:
    def __init__(self, data):
        self.data = data

    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen((255,255,0), width=1, style=wx.SOLID))
        dc.SetTextForeground((255,255,0))

        for i in self.data:
            pos = f(*(i))
            dc.DrawCircle(pos[1], pos[0], 2)


class Plugin(Filter):
	title = 'Watershed'
	note = ['8-bit', 'preview']

	para = {'dis':5, 'thr':10}
	view = [('slide', (1,255), 'min distance', 'dis', ''),
			('slide', (1,255), 'min local value', 'thr', '')]
	def load(self, ips):
		self.buf = np.zeros(ips.size, dtype=np.uint16)
		self.lut = ips.lut
		ips.lut = self.lut.copy()
		return True

	def preview(self, para):
		lst = peak_local_max(self.ips.get_img(), para['dis'], para['thr'], num_peaks=1000)
		self.ips.mark = Mark(lst)
		self.ips.update = True

	#process
	def run(self, ips, snap, img, para = None):
		ips.lut = self.lut
		peak = peak_local_max(self.ips.get_img(), para['dis'], para['thr'], indices=False, num_peaks=1000)
		label(peak, np.ones((3,3)), output = self.buf)
		img[:] = watershed(-img, self.buf, mask = img, watershed_line=True)
		img[img>0] = 255
		ips.mark = None