# -*- coding: utf-8 -*
import scipy.ndimage as nimg
from core.engines import Filter, Simple
from core.graph import builder, graph2d
import numpy as np

class Marker(Filter):
    title = 'Skeleton Point Marker'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']

    #process
    def run(self, ips, snap, img, para = None):
    	builder.mark(img)

class Builder(Simple):
	title = 'Build Graph2D'
	note = ['8-bit']

	def run(self, ips, imgs, para):
		img = ips.get_img() 
		img /= 100
		rst = builder.build_graph(img)
		ips.data = [graph2d.Graph(i,j) for i,j in rst]
		print ips.data

class Draw(Filter):
	title = 'Draw Graph2D'
	note = '8-bit'

	def run(self, ips, snap, img, para = None):
		for i in ips.data:graph2d.draw(i, img)

plgs = [Marker, Builder, Draw]