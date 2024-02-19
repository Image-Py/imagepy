# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 04:34:09 2016

@author: yxl
"""
from skimage.io import imsave
from sciapp.action import Simple
from sciapp.action import dataio

class Plugin(Simple):
    title = 'Save Sequence'
    note = ['all']
    para = {'path':'','name':'','format':'png'}
    #para = {'path':'./','name':'','format':'png'}
    view = [('path', 'path', '', 'folder', 'path'),
            (str, 'name', 'name', 'number'),
            (None)]

    def load(self, ips):
        names = [i[0] for i in dataio.WriterManager.gets(tag='img')]
        self.view[2] = (list, 'format',list(sorted(names)), str, 'format', '')
        return True

    #process
    def run(self, ips, imgs, para = None):
        path = para['path']+'/'+para['name']
        write = dataio.WriterManager.get(para['format'])

        for i in range(len(imgs)):
            self.progress(i, len(imgs))
            name = '%s-%.4d.%s'%(path,i,para['format'])
            write(name, imgs[i])