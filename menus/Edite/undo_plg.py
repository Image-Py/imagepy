# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 15:55:42 2016

@author: yxl
"""
from core.engines import Simple

class Plugin(Simple):
    title = 'Undo'
    note = ['all']
    #process
    def run(self, ips, img, buf, para=None):
        ips.swap()