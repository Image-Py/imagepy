# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 11:30:24 2016
@author: yxl
"""
import wx
from imagepy import IPy, root_dir
from imagepy.core.engine import Free
from imagepy.core.manager import TableLogManager

class Csv(Free):
    title = 'Save Table As CSV'
    #para = {'tab': None, 'path':root_dir}
    para = {'tab': None, 'path':'./'}
    
    def load(self):
        n = len(TableLogManager.get_titles())
        if n>0:return True
        IPy.alert('No table opened!')
        return False
        
    def show(self):
        self.view = [('tab', 'Table', 'tab', '')]
        rst = IPy.getpara('Import sequence', self.view, self.para)
        if rst!=wx.ID_OK:return rst
        filt = 'CSV files (*.csv)|*.csv'
        return IPy.getpath('Import sequence', filt, self.para)
        
    def run(self, para = None):
        table = TableLogManager.get(para['tab'])
        table.save_tab(para['path'], ',')
        
class Tab(Free):
    title = 'Save Table As Tab'
    #para = {'tab': None, 'path':root_dir}
    para = {'tab': None, 'path':'./'}

    def load(self):
        n = len(TableLogManager.get_titles())
        if n>0:return True
        IPy.alert('No table opened!')
        return False
        
    def show(self):
        self.view = [('tab', 'Table', 'tab', '')]
        rst = IPy.getpara('Import sequence', self.view, self.para)
        if rst!=wx.ID_OK:return rst
        filt = 'TXT files (*.txt)|*.txt'
        return IPy.getpath('Import sequence', filt, self.para)
        
    def run(self, para = None):
        table = TableLogManager.get(para['tab'])
        table.save_tab(para['path'], '\t')
        
plgs = [Csv, Tab]