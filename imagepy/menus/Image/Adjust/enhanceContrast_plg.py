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
    view = [(float, 'percentage', (0,100), 1, 'Saturated pixels', '%')]
    
    def run(self, ips, snap, img, para = None):
        p2, p98 = np.percentile(snap, (0, 100 - para['percentage']))
        exposure.rescale_intensity(snap, in_range=(p2, p98))
