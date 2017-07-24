# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 05:43:50 2016
@author: yxl
"""
from imagepy import IPy
from imagepy.core.engine import Free

class Plugin(Free):
    title = 'Exit'
    
    def run(self, para = None):
        IPy.curapp.Close()