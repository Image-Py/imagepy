# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 03:57:53 2016
@author: yxl
"""
import threading, wx
from imagepy import IPy

class Widget():
    title = 'widget'
        
    def start(self):
        frame = wx.Frame(IPy.curapp)
        self.__init__(frame)
        frame.Fit()
        frame.Show()