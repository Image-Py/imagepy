# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 19:41:16 2016

@author: yxl
"""
from core.engines import Free
from core.managers import WindowsManager, TextLogManager, TableLogManager

class ImageKiller(Free):
    title = 'Kill Image'

    def load(self):
        ImageKiller.para = {'name':'All'}
        titles =['All'] + WindowsManager.get_titles()
        ImageKiller.view = [(list, titles, str, 'Name', 'name', 'selected')]
        return True
    
    #process
    def run(self, para = None):
        if para['name'] == 'All':
            for i in WindowsManager.get_titles():
                WindowsManager.close(i)
        else: WindowsManager.close(para['name'])
        
class TextKiller(Free):
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
        
plgs = [ImageKiller, TextKiller, TableKiller]