# -*- coding: utf-8 -*-
"""
Created on 12/21/2018
@author: BioinfoTongLI
"""

from imagepy.core.manager import RoiManager
from imagepy.core.engine import Free
from imagepy import IPy
from imagepy.core.roi import roiio
from shapely.geometry import Polygon

from imagepy.core.roi.convert import shape2roi


class Plugin(Free):
    """load_ij_roi: use read_roi and th pass to shapely objects"""
    title = 'Import Rois from ImageJ'
    para = {'path': 'test'}

    def load(self):
        filt = '|'.join(['%s files (*.%s)|*.%s' % (i.upper(), i, i) for i in ["zip"]])
        rst = IPy.getpath(self.title, filt, 'open', self.para)
        if not rst: return rst
        return True

    def run(self, para=None):
        roi_set = roiio.read_roi_zip(self.para["path"])
        n_roi = len(roi_set)
        print("Loaded %i rois" % n_roi)
        for cell_nb in roi_set:
            print("%s  added " % cell_nb)
            RoiManager.add(str(cell_nb),
                           shape2roi(Polygon(list(zip(roi_set[cell_nb]["x"], roi_set[cell_nb]["y"])))))

        mask = ""
        # view(imgs, para['title'])


if __name__ == '__main__':
    print(Plugin.title)
    app = wx.App(False)
    Plugin().run()