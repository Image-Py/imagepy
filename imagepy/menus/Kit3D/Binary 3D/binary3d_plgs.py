# -*- coding: utf-8 -*
import scipy.ndimage as ndimg
from sciapp.action import Simple
from skimage.morphology import skeletonize_3d
from imagepy.ipyalg import find_maximum, watershed
from skimage.filters import apply_hysteresis_threshold
from imagepy.ipyalg import distance_transform_edt
import numpy as np

class Dilation(Simple):
    """Dilation: derived from sciapp.action.Filter """
    title = 'Dilation 3D'
    note = ['all', 'stack3d']
    para = {'r':3}
    view = [(int, 'r', (1,15), 0, 'r', 'pix')]

    def run(self, ips, imgs, para = None):
        strc = np.ones((para['r'], para['r'],para['r']), dtype=np.uint8)
        imgs[:] = ndimg.binary_dilation(imgs, strc)
        imgs *= 255

class Erosion(Simple):
    """Dilation: derived from sciapp.action.Filter """
    title = 'Erosion 3D'
    note = ['all', 'stack3d']
    para = {'r':3}
    view = [(int, 'r', (1,15), 0, 'r', 'pix')]

    def run(self, ips, imgs, para = None):
        strc = np.ones((para['r'], para['r'], para['r']), dtype=np.uint8)
        imgs[:] = ndimg.binary_erosion(imgs, strc)
        imgs *= 255

class Opening(Simple):
    """Dilation: derived from sciapp.action.Filter """
    title = 'Opening 3D'
    note = ['all', 'stack3d']
    para = {'r':3}
    view = [(int, 'r', (1,15), 0, 'r', 'pix')]

    def run(self, ips, imgs, para = None):
        strc = np.ones((para['r'], para['r'], para['r']), dtype=np.uint8)
        imgs[:] = ndimg.binary_opening(imgs, strc)
        imgs *= 255

class Closing(Simple):
    """Dilation: derived from sciapp.action.Filter """
    title = 'Closing 3D'
    note = ['all', 'stack3d']
    para = {'r':3}
    view = [(int, 'r', (1,15), 0, 'r', 'pix')]

    def run(self, ips, imgs, para = None):
        strc = np.ones((para['r'], para['r'], para['r']), dtype=np.uint8)
        imgs[:] = ndimg.binary_closing(imgs, strc)
        imgs *= 255

class FillHole(Simple):
    """Dilation: derived from sciapp.action.Filter """
    title = 'Fill Holes 3D'
    note = ['all', 'stack3d']


    def run(self, ips, imgs, para = None):
        imgs[:] = ndimg.binary_fill_holes(imgs)
        imgs *= 255

class Skeleton3D(Simple):
    title = 'Skeleton 3D'
    note = ['all', 'stack3d']

    #process
    def run(self, ips, imgs, para = None):
        imgs[skeletonize_3d(imgs>0)==0] = 0

class Distance3D(Simple):
    title = 'Distance 3D'
    note = ['all', 'stack3d']

    #process
    def run(self, ips, imgs, para = None):
        imgs[:] = imgs>0
        dtype = imgs.dtype if imgs.dtype in (np.float32, np.float64) else np.uint16
        dismap = distance_transform_edt(imgs, output=dtype)
        imgs[:] = np.clip(dismap, ips.range[0], ips.range[1])

class Watershed(Simple):
    """Mark class plugin with events callback functions"""
    title = 'Binary Watershed 3D'
    note = ['8-bit', 'stack3d']


    para = {'tor':2, 'con':False}
    view = [(int, 'tor', (0,255), 0, 'tolerance', 'value'),
            (bool, 'con', 'full connectivity')]

    ## TODO: Fixme!
    def run(self, ips, imgs, para = None):
        imgs[:] = imgs > 0
        dist = distance_transform_edt(imgs, output=np.uint16)
        pts = find_maximum(dist, para['tor'], True)
        buf = np.zeros(imgs.shape, dtype=np.uint32)
        buf[pts[:,0], pts[:,1], pts[:,2]] = 2
        imgs[pts[:,0], pts[:,1], pts[:,2]] = 2
        markers, n = ndimg.label(buf, np.ones((3, 3, 3)))
        line = watershed(dist, markers, line=True, conn=para['con']+1, up=False)
        msk = apply_hysteresis_threshold(imgs, 0, 1)
        imgs[:] = imgs>0; imgs *= 255; imgs *= ~((line==0) & msk)

plgs = [Dilation, Erosion, Opening, Closing, '-', FillHole, Skeleton3D, '-', Distance3D, Watershed]