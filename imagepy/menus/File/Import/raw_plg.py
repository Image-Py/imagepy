import os,sys
import numpy as np
import io# urllib2 urllib.request, urllib.error, urllib.parse
from skimage.io import imread
from sciapp.action import Free

class Plugin(Free):
    title = 'Open Raw'
    para = {'path':'', 'type':'uint8', 'w':512, 'h':512, 'c':1}
    tps = ['uint8', 'int16', 'float32']

    view = [(list, 'type', tps, str, 'type', ''),
            (int, 'w', (0,2048), 0, 'width', 'pix'),
            (int, 'h', (0,2048), 0, 'height', 'pix'),
            (list, 'c', [1,3], int, 'channel', '')]
    
    def load(self):
        filt = 'raw'
        self.para['path'] = self.app.get_path('Open..', filt, 'open', '')
        return not self.para['path'] is None

    #process
    def run(self, para = None):
        path = para['path']
        fp, fn = os.path.split(path)
        fn, fe = os.path.splitext(fn) 
        img = np.fromfile(para['path'], dtype=para['type'])
        sp = (para['h'], para['w'], para['c'])[:2 if para['c']==1 else 3]
        if img.size != para['h']*para['w']*para['c']:
            self.app.alert('raw data error!')
            return
        img.shape = sp
        self.app.show_img([img], fn)