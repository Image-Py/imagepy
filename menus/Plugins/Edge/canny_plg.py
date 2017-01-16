# -*- coding: utf-8 -*
from skimage import feature
from core.engines import Filter



class Plugin(Filter):
    title = 'Canny'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    
    para = {'sigma':1.0, 'low_threshold':10, 'high_threshold':20}
    
    #parameter
    view = [(float, (0,10), 1,  'sigma', 'sigma', 'pix'),
            ('slide',(0,30), 'low_threshold', 'low_threshold',''),
            ('slide',(0,30), 'high_threshold', 'high_threshold','')]

    #process
    def run(self, ips, img, buf, para = None):
        return feature.canny(img, sigma=para['sigma'], low_threshold=para[
            'low_threshold'], high_threshold=para['high_threshold'], mask=ips.get_msk())*255