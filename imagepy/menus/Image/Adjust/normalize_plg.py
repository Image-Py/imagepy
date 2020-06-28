"""
Created on Sun Jan 25 9:00:00 2020
@author: weisong
"""
from sciapp.action import Simple
import numpy as np

class Plugin(Simple):
    title = 'Normalize'
    note = ['8-bit','16-bit','float']
    para = {'is3d': False, 'sb':True}
    view = [(bool, 'is3d', '3D stack'),
            (bool, 'sb', 'Subtract background')]

    def run(self, ips, imgs, para = None):
        lim = np.zeros([len(imgs), 2], dtype=imgs[0].dtype)
        dic = {np.uint8:255, np.uint16:65535, np.float32:1, np.float64:1}

        self.app.info('count range ...')
        for i in range(len(imgs)):
            lim[i] = imgs[i].min(), imgs[i].max()
            self.progress(i, len(imgs))
        
        maxvalue = dic[imgs[0].dtype.type]
        if not para['sb']: lim[:,0] = 0
        rg = lim[:,0].min(), lim[:,1].max()
        if para['is3d']: lim[:] = rg
        self.app.info('adjust range ...')
        for i in range(len(imgs)):
            if para['sb']: imgs[i] -= lim[i,0]
            np.multiply(imgs[i], maxvalue/(lim[i].ptp()), out=imgs[i], casting='unsafe')
            self.progress(i, len(imgs))
        ips.range = 0, maxvalue