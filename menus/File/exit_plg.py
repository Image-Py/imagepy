# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 05:43:50 2016

@author: yxl
"""
import IPy
from core.engines import Free

class Plugin(Free):
    title = 'Exit'
    
    #process
    def run(self, para = None):
        IPy.curapp.Close()