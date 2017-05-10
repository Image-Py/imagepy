# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 04:34:09 2016

@author: yxl
"""
from scipy.misc import imsave
from core.engines import Simple
import wx
import IPy,IPyGL

class Plugin(Simple):
    title = 'Save Sequence'
    note = ['all']
    para = {'path':IPyGL.root_dir,'name':'','format':'png'}
    #para = {'path':'./','name':'','format':'png'}
    
    view = [(str, 'Name', 'name', ''),
            (list, ['bmp','jpg','png','tif'], str, 'Format', 'format','')]

    def show(self):
        self.para['name'] = self.ips.title
        rst = IPy.get_para('Save sequence', self.view, self.para)    
        if rst!=wx.ID_OK:return rst
        return IPy.getdir('Save sequence', '', self.para)

    #process
    def run(self, ips, imgs, para = None):
        path = para['path']+'/'+para['name']
        print(path)
        for i in range(len(imgs)):
            IPy.curapp.set_progress(int(round((i+1.0)/len(imgs)*100)))
            #name = '%s-%.4d.%s'%(path,i,para['format'])
            name = "{0}-{1:04}.{2}".format(path,i,para['format'])
            print(name)
            imsave(name, imgs[i])
        IPy.curapp.set_progress(0)