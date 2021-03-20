# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 19:41:16 2016

@author: yxl
"""
from sciapp.action import Free
#from imagepy.core.manager import ImageManager, TextLogManager, \
#    TableManager, WindowsManager, WTableManager

class ImageKiller(Free):
    title = 'Kill Image'
    asyn = False
    para = {'img':None, 'all':False}
    view = [('img', 'img', 'name', ''),
            (bool, 'all', 'close all images')]
    
    def run(self, para = None):
        self.app.close_img(None if para['all'] else para['img'])
        
class TableKiller(Free):
    title = 'Kill Table'
    asyn = False
    para = {'tab':None, 'all':False}
    view = [('tab', 'tab', 'name', ''),
            (bool, 'all', 'close all tables')]
    
    def run(self, para = None):
        self.app.close_table(None if para['all'] else para['tab'])
        
#!TODO: plugins ?!
plgs = [ImageKiller, TableKiller]