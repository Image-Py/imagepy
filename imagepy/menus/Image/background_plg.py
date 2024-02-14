import numpy as np
from sciapp.object import Image
from sciapp.action import Simple

class SetBackground(Simple):
    title = 'Set Background'
    note = ['all']
    para = {'img':None,'mode':'msk', 'k':0.5, 'kill':False}
    view = [('img','img', 'background', '8-bit'),
            (list, 'mode', ['set', 'min', 'max', 'msk', 'ratial'], str, 'mode', ''),
            (float, 'k', (0, 1), 1, 'ratial', ''),
            (bool, 'kill', 'kill')]
    
    def run(self, ips, imgs, para = None):
        if para['kill']: ips.mode, ips.back = 'set', None
        else:
            ips.back = self.app.get_img(para['img'])
            ips.mode = para['k'] if para['mode']=='ratial' else para['mode']
        
class BackgroundSelf(Simple):
    title = 'Background Self'
    note = ['all']
    para = {'mode':'msk', 'k':0.5}
    view = [(list, 'mode', ['set', 'min', 'max', 'msk', 'ratial'], str, 'mode', ''),
            (float, 'k', (0, 1), 1, 'ratial', '')]
    
    def run(self, ips, imgs, para = None):
        print(para)
        if ips.isarray: imgs = imgs.copy()
        else: imgs = [i.copy() for i in imgs]
        back = Image(imgs)
        back.cn, back.rg = ips.cn, ips.rg
        ips.back = back
        ips.mode = para['k'] if para['mode']=='ratial' else para['mode']

plgs = [SetBackground, BackgroundSelf]