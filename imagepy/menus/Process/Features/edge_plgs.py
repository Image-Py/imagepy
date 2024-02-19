# -*- coding: utf-8 -*
from skimage import feature
from sciapp.action import Filter

class Canny(Filter):
    title = 'Canny'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'sigma':1.0, 'low_threshold':10, 'high_threshold':20}
    view = [(float, 'sigma', (0,10), 1,  'sigma', 'pix'),
            ('slide', 'low_threshold',  (0,50), 4, 'low_threshold'),
            ('slide', 'high_threshold', (0,50), 4, 'high_threshold')]

    def run(self, ips, snap, img, para = None):
        return feature.canny(snap, sigma=para['sigma'], low_threshold=para[
            'low_threshold'], high_threshold=para['high_threshold'], mask=ips.mask())*255

plgs = [Canny]