# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 01:48:23 2016
@author: yxl
"""
from ... import IPy
from ...core.manager import TextLogManager
import threading

class Macros:
    def __init__(self, title, cmds):
        self.title = title
        self.cmds = cmds
        
    def run(self):
        IPy.run_macros(self.cmds)

    def __call__(self):
        return self
        
    def start(self, thd=False):
        win = TextLogManager.get('Recorder')
        if win!=None and self.title!=None:
            win.append('{}>None'.format(self.title))
        self.run()
        '''
        if thd:
            print thd, '--------------------new thread'
            thread = threading.Thread(None, self.run, ())
            thread.start()
        else: self.run()
        '''
        