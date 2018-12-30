# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 19:41:16 2016

@author: yxl
"""
from imagepy.core.engine import Free
from imagepy.core.manager import ImageManager, TextLogManager, \
    TableManager, WindowsManager, WTableManager

class ImageKiller(Free):
    """ImageKiller: derived from imagepy.core.engine.Free"""
    title = 'Kill Image'
    asyn = False

    def load(self):
        ImageKiller.para = {'name':'All'}
        titles =['All'] + ImageManager.get_titles()
        ImageKiller.view = [(list, 'name', titles, str, 'Name', 'selected')]
        return True
    
    #process
    def run(self, para = None):
        if para['name'] == 'All':
            for i in ImageManager.get_titles():
                WindowsManager.get(i).close()
        else: 
            print(WindowsManager.get(para['name']))
            WindowsManager.get(para['name']).close()
        
class TextKiller(Free):
    """TextKiller: derived from imagepy.core.engine.Free"""
    title = 'Kill TextLog'
    asyn = False

    def load(self):
        TextKiller.para = {'name':'All'}
        titles =['All'] + TextLogManager.get_titles()
        TextKiller.view = [(list, 'name', titles, str, 'Name', 'selected')]
        return True
    
    #process
    def run(self, para = None):
        if para['name'] == 'All':
            for i in TextLogManager.get_titles():
                TextLogManager.close(i)
        else: TextLogManager.close(para['name'])
        
class TableKiller(Free):
    """TableKiller: derived from imagepy.core.engine.Free"""
    title = 'Kill TableLog'
    asyn = False

    def load(self):
        self.para = {'name':'All'}
        titles = ['All'] + TableManager.get_titles()
        self.view = [(list, 'name', titles, str, 'Name', 'selected')]
        return True
    
    #process
    def run(self, para = None):
        if para['name'] == 'All':
            for i in TableManager.get_titles():
                WTableManager.get(i).close()
        else: WTableManager.get(para['name']).close()
        
#!TODO: plugins ?!
plgs = [ImageKiller, TextKiller, TableKiller]