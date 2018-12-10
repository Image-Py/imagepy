# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 04:34:09 2016

@author: yxl
"""
import wx
from skimage.io import imsave
from imagepy.core.engine import Simple
from imagepy.core.manager import WriterManager, ViewerManager
from imagepy import IPy, root_dir

class Plugin(Simple):
    title = 'Save Sequence'
    note = ['all']
    para = {'path':'','name':'','format':'png'}
    #para = {'path':'./','name':'','format':'png'}

    def load(self, ips):
        self.view = [(str, 'name', 'Name', ''),
            (list, 'format',list(sorted(WriterManager.get())), str, 'Format', '')]
        return True

    def show(self):
        self.para['name'] = self.ips.title
        rst = IPy.get_para('Save sequence', self.view, self.para)
        if not rst :return rst
        return IPy.getdir('Save sequence', '', self.para)

    #process
    def run(self, ips, imgs, para = None):
        path = para['path']+'/'+para['name']
        write = WriterManager.get(para['format'])
        print(path)
        for i in range(len(imgs)):
            self.progress(i, len(imgs))
            name = '%s-%.4d.%s'%(path,i,para['format'])
            write(name, imgs[i])