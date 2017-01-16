# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 20:25:52 2016

@author: yxl
"""

from core.engines import Simple
from core.managers import RoiManager
import IPy

class Union(Simple):
    title = 'Union'
    note = ['all']
    para = {'name':''}
    
    def load(self, ips):
        titles = RoiManager.rois.keys()
        if len(titles)==0: 
            IPy.alert('No roi in manager!')
            return False
        self.para['name'] = titles[0]
        self.view = [(list, titles, str, 'Name', 'name', '')]
        return True

    def run(self, ips, imgs, para = None):
        ips.roi = ips.roi.union(RoiManager.get(para['name']))
        
class Diff(Simple):
    title = 'Difference'
    note = ['all']
    para = {'name':''}
    
    def load(self, ips):
        titles = RoiManager.rois.keys()
        if len(titles)==0: 
            IPy.alert('No roi in manager!')
            return False
        self.para['name'] = titles[0]
        self.view = [(list, titles, str, 'Name', 'name', '')]
        return True

    def run(self, ips, imgs, para = None):
        ips.roi = ips.roi.diff(RoiManager.get(para['name']))
        
plgs = [Union, Diff]