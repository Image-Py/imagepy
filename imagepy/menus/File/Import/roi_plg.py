# -*- coding: utf-8 -*-
"""
Created on 12/21/2018
@author: BioinfoTongLI
"""
import numpy as np
import read_roi
from imagepy.core.engine import Free
from imagepy import IPy
from skimage.draw import polygon

class Plugin(Free):
    """load_ij_roi: use read_roi and th pass to shapely objects"""
    title = 'Import Rois from IJ'

    para = {'path': '', 'name': 'Undefined', 'width': 512, 'height': 512}

    view = [(str, 'name', 'name', ''),
            (int, 'width',  (1, 3000), 0,  'width', 'pix'),
            (int, 'height', (1, 3000), 0,  'height', 'pix')]

    def load(self):
        filt = '|'.join(['%s files (*.%s)|*.%s' % (i.upper(), i, i) for i in ["zip"]])
        return IPy.getpath(self.title, filt, 'open', self.para)

    def run(self, para=None):
        ls = read_roi.read_roi_zip(para['path'])
        img = np.zeros((para['height'], para['width']), dtype=np.int32)
        for i in ls:
            img[polygon(ls[i]['y'], ls[i]['x'], img.shape)] = int(i)
        IPy.show_img([img], para['name'])
