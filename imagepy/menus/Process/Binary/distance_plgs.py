# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 00:26:45 2016
@author: yxl
"""
import numpy as np
from skimage.morphology import skeletonize
from skimage.morphology import medial_axis
from imagepy.ipyalg.graph import skel2d
from imagepy.core.engine import Filter
from imagepy.ipyalg import find_maximum, watershed
#from skimage.morphology import watershed
import scipy.ndimage as ndimg

class Skeleton(Filter):
  title = 'Skeleton'
  note = ['all', 'auto_msk', 'auto_snap','preview']

  def run(self, ips, snap, img, para = None):
    img[:] = skeletonize(snap>0)
    img *= 255

class EDT(Filter):
	"""EDT: derived from imagepy.core.engine.Filter """
	title = 'Distance Transform'
	note = ['all', 'auto_msk', 'auto_snap','preview']

	def run(self, ips, snap, img, para = None):
		return ndimg.distance_transform_edt(snap)

class MedialAxis(Filter):
	title = 'Medial Axis'
	note = ['all', 'auto_msk', 'auto_snap', 'preview']
	para = {'dis':False}
	view = [(bool,'distance transform', 'dis')]

	#process
	def run(self, ips, snap, img, para = None):
		dis = skel2d.mid_axis(snap)
		if not para['dis']:
			img[:] = dis>0
			img *= 255
		else: img[:] = dis

class Watershed(Filter):
	"""Mark class plugin with events callback functions"""
	title = 'Binary Watershed'
	note = ['8-bit', 'auto_msk', 'auto_snap', 'preview']


	para = {'tor':2, 'con':False}
	view = [(int, (0,255), 0, 'tolerance', 'tor', 'value'),
			(bool, 'full connectivity', 'con')]

	## TODO: Fixme!
	def run(self, ips, snap, img, para = None):
		img[:] = snap
		dist = -ndimg.distance_transform_edt(snap)
		pts = find_maximum(dist, para['tor'], False)
		buf = np.zeros(ips.size, dtype=np.uint16)
		buf[pts[:,0], pts[:,1]] = 1
		markers, n = ndimg.label(buf, np.ones((3,3)))
		line = watershed(dist, markers, line=True, conn=para['con']+1)
		img[line==0] = 0

class Voronoi(Filter):
	"""Mark class plugin with events callback functions"""
	title = 'Binary Voronoi'
	note = ['8-bit', '16-bit', 'auto_msk', 'auto_snap', 'preview']

	para = {'type':'segment with ori'}
	view = [(list, ['segment with ori', 'segment only', 'white line', 'gray line'], str, 'output', 'type', '')]
	## TODO: Fixme!
	def run(self, ips, snap, img, para = None):
		dist = ndimg.distance_transform_edt(snap)
		markers, n = ndimg.label(snap==0, np.ones((3,3)))

		line = watershed(dist, markers, line=True)
		if para['type']=='segment with ori':
			img[:] = np.where(line==0, 0, snap)
		if para['type']=='segment only':
			img[:] = (line>0) * 255
		if para['type']=='white line':
			img[:] = (line==0) * 255
		if para['type']=='gray line':
			img[:] = np.where(line==0, dist, 0)


plgs = [Skeleton, MedialAxis, '-', EDT, Watershed, Voronoi]