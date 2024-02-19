# -*- coding: utf-8 -*-
"""
Created on 12/21/2018
@author: BioinfoTongLI
"""
import numpy as np
import read_roi
from sciapp.action import Free
from skimage.draw import polygon, ellipse

class Plugin(Free):
    """load_ij_roi: use read_roi and th pass to shapely objects"""
    title = 'Import Rois from IJ'

    para = {'path': '', 'name': 'Undefined', 'width': 512, 'height': 512}

    view = [(str, 'name', 'name', ''),
            (int, 'width',  (1, 3000), 0,  'width', 'pix'),
            (int, 'height', (1, 3000), 0,  'height', 'pix')]

    def load(self):
        filt = 'zip'
        self.para['path'] = self.app.get_path(self.title, filt, 'open', self.para['name'])
        return not self.para['path'] is None

    def run(self, para=None):
        ls = read_roi.read_roi_zip(para['path'])
        img = np.zeros((para['height'], para['width']), dtype=np.int32)
        for i in ls:
            current_roi = ls[i]
            roi_type = current_roi["type"]
            if roi_type is "freehand":
                rs, cs = polygon(ls[i]['y'], ls[i]['x'], img.shape)
            elif roi_type is "oval":
                rs, cs = ellipse(current_roi["top"]+current_roi["height"]/2,
                        current_roi["left"]+current_roi["width"]/2,
                        current_roi["height"]/2,
                        current_roi["width"]/2)
            try:
                ind = int(i)
            except Exception:
                ind = int(i.split("-")[-1])
            img[rs, cs] = ind
        self.app.show_img([img], para['name'])
