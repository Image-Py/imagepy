import wx,os,sys
import numpy as np
import io# urllib2 urllib.request, urllib.error, urllib.parse
from scipy.misc import imread
from imagepy import IPy
from imagepy.core.engine import Free

class Plugin(Free):
    title = 'Open Raw'
    para = {'path':'', 'type':'uint8', 'w':512, 'h':512, 'c':1}
    tps = ['uint8', 'int16', 'float32']

    view = [(list, tps, str, 'type', 'type', ''),
            (int, (0,2048), 0, 'width', 'w', 'pix'),
            (int, (0,2048), 0, 'height', 'h', 'pix'),
            (list, [1,3], int, 'channel', 'c', '')]
    
    def load(self):
        filt = 'RAW files (*.raw)|*.raw'
        rst = IPy.getpath('Open..', filt, 'open', self.para)
        if rst!=None:return True

    #process
    def run(self, para = None):
        path = para['path']
        fp, fn = os.path.split(path)
        fn, fe = os.path.splitext(fn) 
        img = np.fromfile(para['path'], dtype=para['type'])
        sp = (para['h'], para['w'], para['c'])[:2 if para['c']==1 else 3]
        if img.size != para['h']*para['w']*para['c']:
            IPy.alert('raw data error!')
            return
        img.shape = sp
        IPy.show_img([img], fn)

if __name__ == '__main__':
    print(Plugin.title)
    app = wx.App(False)
    Plugin().run()