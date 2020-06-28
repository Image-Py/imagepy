# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 00:26:45 2016
@author: yxl
"""
import numpy as np
from skimage.morphology import skeletonize
from skimage.morphology import medial_axis
from imagepy.ipyalg.graph import skel2d
from sciapp.action import Filter
from imagepy.ipyalg import find_maximum, watershed, distance_transform_edt
from skimage.filters import apply_hysteresis_threshold
import scipy.ndimage as ndimg

class Skeleton(Filter):
  title = 'Skeleton'
  note = ['all', 'auto_msk', 'auto_snap','preview']

  def run(self, ips, snap, img, para = None):
    img[:] = skeletonize(snap>0)
    img *= 255

class EDT(Filter):
	"""EDT: derived from sciapp.action.Filter """
	title = 'Distance Transform'
	note = ['all', 'auto_msk', 'auto_snap','preview']

	def run(self, ips, snap, img, para = None):
		return distance_transform_edt(snap)

class MedialAxis(Filter):
	title = 'Medial Axis'
	note = ['all', 'auto_msk', 'auto_snap', 'preview']
	para = {'dis':False}
	view = [(bool, 'dis', 'distance transform')]

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
	view = [(int, 'tor', (0,255), 0, 'tolerance', 'value'),
			(bool, 'con', 'full connectivity')]

	## TODO: Fixme!
	def run(self, ips, snap, img, para = None):
		img[:] = snap>0
		dist = distance_transform_edt(snap, output=np.uint16)
		pts = find_maximum(dist, para['tor'], True)
		buf = np.zeros(ips.shape, dtype=np.uint32)
		buf[pts[:,0], pts[:,1]] = img[pts[:,0], pts[:,1]] = 2
		markers, n = ndimg.label(buf, np.ones((3,3)))
		line = watershed(dist, markers, line=True, conn=para['con']+1, up=False)
		msk = apply_hysteresis_threshold(img, 0, 1)
		img[:] = snap * ~((line==0) & msk)

class Voronoi(Filter):
	"""Mark class plugin with events callback functions"""
	title = 'Binary Voronoi'
	note = ['8-bit', '16-bit', 'auto_msk', 'auto_snap', 'preview']

	para = {'type':'segment with ori'}
	view = [(list, 'type', ['segment with ori', 'segment only', 'white line', 'gray line'], str, 'output', '')]
	## TODO: Fixme!
	def run(self, ips, snap, img, para = None):
		dist = distance_transform_edt(snap, output=np.uint16)
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