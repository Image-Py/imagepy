# -*- coding: utf-8 -*-
"""
Created on 12/21/2018
@author: BioinfoTongLI
"""
from imagepy.core import ImagePlus
from imagepy.core.engine import Free
from imagepy import IPy
from imagepy.core.roi import roiio
from shapely.geometry import Polygon
import wx
from imagepy.core.roi.convert import shape2roi
import numpy as np


class Plugin(Free):
    """load_ij_roi: use read_roi and th pass to shapely objects"""
    title = 'Import Rois from IJ'
    para = {'path': '', 'name': 'Undefined', 'width': 2560, 'height': 2160}
    view = [(str, 'name', 'name', ''),
            (int, 'width',  (1, 3000), 0,  'width', 'pix'),
            (int, 'height', (1, 3000), 0,  'height', 'pix')]

    def load(self):
        filt = '|'.join(['%s files (*.%s)|*.%s' % (i.upper(), i, i) for i in ["zip"]])
        rst = IPy.getpath(self.title, filt, 'open', self.para)
        if not rst: return rst
        return True

    def run(self, para=None):
        roi_set = roiio.read_roi_zip(self.para["path"])
        n_roi = len(roi_set)
        print("Loaded %i rois" % n_roi)

        mask_ips = ImagePlus([np.zeros((para['height'], para['width']), dtype=np.int32)], self.para["name"])

        for one_id in roi_set:
            # none of the roi are send to the roi manager
            one_roi = shape2roi(Polygon(list(zip(roi_set[one_id]["x"], roi_set[one_id]["y"]))))
            one_roi.fill(mask_ips.img, color=int(one_id))

        IPy.showips(mask_ips)
        mask_ips.update = "pix"


if __name__ == '__main__':
    print(Plugin.title)
    app = wx.App(False)
    Plugin().run()