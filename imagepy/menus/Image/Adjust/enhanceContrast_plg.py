"""
Created on Sun Jan 25 17:00:00 2020
@author: weisong
"""
from imagepy.core.engine import Filter
from skimage import exposure
import numpy as np

class Plugin(Filter):
    title = 'Enhance contrast'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    para = {'percentage': 0.3}
    view = [(float, 'percentage', (0,100), 4, 'Saturated pixels', '%')]
    
    def run(self, ips, snap, img, para = None):
        up, down = np.percentile(snap, (para['percentage']/2, 100 - para['percentage']/2))
        return exposure.rescale_intensity(snap, in_range=(up, down))
