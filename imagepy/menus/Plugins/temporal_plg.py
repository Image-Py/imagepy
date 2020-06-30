"""
Created on Sun Jan 22 12:56:00 2020
@author: weisong
"""
from sciapp.action import Simple
from imagepy.app import ColorManager
import numpy as np

def color_code(img, lut):
    idx = np.linspace(0,255,len(img)).astype(int)
    cs = lut[idx].astype(np.uint32)
    buf = np.zeros(img[0].shape+(3,), dtype=np.uint32)
    for im, c in zip(img, cs):
        buf += im.reshape(im.shape+(-1,)) * c
    k = 255/buf.max(axis=(0,1)).reshape((1,1,3))
    return (buf * k).astype(np.uint8)

class Plugin(Simple):
    title = 'Temporal color-code'
    note = ['all', 'stack']
    para = {'LUT':'Jet',
            'Start image':1,
            'End image': 2,
            'Creatbar':True}

    def load(self, ips): 
        self.slength = len(ips.imgs)
        self.para['End image'] = self.slength
        self.view = [(list, 'LUT', ColorManager.names(), str, 'LUT',''),
            (int, 'Start image', (1,self.slength),0,'Start image','1~%d'%self.slength),
            (int, 'End image', (2,self.slength),0,'End image','start~%d'%self.slength),
            (bool, 'Creatbar', 'Creat time color scale bar')]
        return True

    def run(self, ips, imgs, para = None):
        cmap = ColorManager.get(para['LUT'])
        imglut = color_code(imgs[para['Start image']-1: para['End image']], cmap)
        self.app.show_img([imglut],'Color-coded %s'%ips.title)
        if para['Creatbar']:
            cmapshow = np.ones([32,256,3])*cmap
            self.app.show_img([cmapshow.astype('uint8')],'Color bar')

