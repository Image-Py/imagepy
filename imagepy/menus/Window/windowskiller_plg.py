# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 19:41:16 2016

@author: yxl
"""
from imagepy.core.engine import Free
from imagepy.core.manager import WindowsManager, TextLogManager, TableLogManager

class ImageKiller(Free):
    """ImageKiller: derived from imagepy.core.engine.Free"""
    title = 'Kill Image'

    def load(self):
        ImageKiller.para = {'name':'All'}
        titles =['All'] + WindowsManager.get_titles()
        ##!TODO: waht is the view ?
        ImageKiller.view = [(list, titles, str, 'Name', 'name', 'selected')]
        return True
    
    #process
    def run(self, para = None):
        if para['name'] == 'All':
            for i in WindowsManager.get_titles():
                WindowsManager.close(i)
        else: WindowsManager.close(para['name'])
        
class TextKiller(Free):
    """TextKiller: derived from imagepy.core.engine.Free"""
    title = 'Kill TextLog'

    def load(self):
        TextKiller.para = {'name':'All'}
        titles =['All'] + TextLogManager.get_titles()
        TextKiller.view = [(list, titles, str, 'Name', 'name', 'selected')]
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

    def load(self):
        TableKiller.para = {'name':'All'}
        titles =['All'] + TableLogManager.get_titles()
        TableKiller.view = [(list, titles, str, 'Name', 'name', 'selected')]
        return True
    
    #process
    def run(self, para = None):
        if para['name'] == 'All':
            for i in TableLogManager.get_titles():
                TableLogManager.close(i)
        else: TableLogManager.close(para['name'])
        
#!TODO: plugins ?!
plgs = [ImageKiller, TextKiller, TableKiller]