# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 09:58:55 2016
@author: yxl
"""
import IPy
from core.engines import Simple
from core.managers import WindowsManager
from imageplus import ImagePlus
from ui.canvasframe import CanvasFrame

class Plugin(Simple):
    title = 'Split Channels'
    note = ['rgb']
    
    para = {'copy':False, 'destory':True}
    view = {(bool, 'Copy data from view', 'copy'),
            (bool, 'Destory current image', 'destory')}
    #process
    def run(self, ips, imgs, para = None):
        r,g,b = [],[],[]
        for i,n in zip(imgs,list(range(ips.get_nslices()))):
            IPy.curapp.set_progress(round((n+1)*100.0/len(imgs)))
            for c,ci in zip((r,g,b),(0,1,2)):
                if self.para['copy']:c.append(i[:,:,ci].copy())
                else: c.append(i[:,:,ci])
        IPy.curapp.set_progress(0)
        for im, tl in zip([r,g,b],['red','green','blue']):
            ip = ImagePlus(im, ips.title+'-'+tl)
            frame = CanvasFrame(IPy.curapp)
            frame.set_ips(ip)
            frame.Show()
        if self.para['destory']:
            WindowsManager.close(ips.title)