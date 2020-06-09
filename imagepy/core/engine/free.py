# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 03:57:53 2016
@author: yxl
"""
import threading
from time import time

class Free:
    title = 'Free'
    view = None
    para = None
    prgs = None
    asyn = True

    def progress(self, i, n): self.prgs = int(i*100/n)

    def run(self, para=None):
        print('this is a plugin')
        
    def runasyn(self, para, callback=None):
        self.app.add_task(self)
        start = time()
        self.run(para)
        self.app.info('%s: cost %.3fs'%(self.title, time()-start))
        self.app.remove_task(self)
        if callback!=None:callback()

    def load(self):return True
        
    def show(self):
        if self.view==None:return True
        return self.app.show_para(self.title, self.view, self.para, None)
        
    def start(self, app, para=None, callback=None):
        self.app = app
        if not self.load():return
        if para!=None or self.show():
            if para==None:para = self.para
            self.app.record_macros('{}>{}'.format(self.title, para))
            if self.asyn:
                threading.Thread(target = self.runasyn, 
                    args = (para, callback)).start()
            else: self.runasyn(para, callback)
