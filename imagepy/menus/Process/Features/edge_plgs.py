# -*- coding: utf-8 -*
from skimage import feature
from imagepy.core.engine import Filter

class Canny(Filter):
    title = 'Canny'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'sigma':1.0, 'low_threshold':10, 'high_threshold':20}
    view = [(float, (0,10), 1,  'sigma', 'sigma', 'pix'),
            ('slide',(0,50), 'low_threshold', 'low_threshold',''),
            ('slide',(0,50), 'high_threshold', 'high_threshold','')]

    def run(self, ips, snap, img, para = None):
        return feature.canny(snap, sigma=para['sigma'], low_threshold=para[
            'low_threshold'], high_threshold=para['high_threshold'], mask=ips.get_msk())*255

plgs = [Canny]