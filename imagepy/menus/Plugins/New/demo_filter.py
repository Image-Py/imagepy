# -*- coding: utf-8 -*-
import scipy.ndimage as nimg
from sciapp.action import Filter

# this is a Filter Sample, implements the Gaussian Blur
class Plugin(Filter):
    # the title on the menu
    title = 'Gaussian'
    # the describe parameter
    note = ['all', 'auto_msk', 'auto_snap','preview']

    # parameter
    para = {'sigma':2}
    # how to interact with the para, it is in 0~30, and 1 decimal
    view = [(float, 'sigma', (0,30), 1,  'sigma', 'pix')]

    # handle the image, img -> buf
    def run(self, ips, snap, img, para = None):
        nimg.gaussian_filter(snap, para['sigma'], output=img)
        
# you can also write muti class in the current modal then:
# plgs = [class1, class2...]