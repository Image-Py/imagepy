# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 01:48:23 2016
@author: yxl
"""
from sciapp import Source
#from imagepy.ui.propertygrid import GridDialog
#from imagepy.core.util import xlreport
from time import time
import openpyxl as pyxl
from sciapp import Source

class Report:
    def __init__(self, title, cont):
        self.title = title
        self.cont = cont
        
    def __call__(self): return self

    def runasyn(self,  wb, info, key, para = None, callback = None):
        self.app.add_task(self)
        for i in para: 
            if i in key and key[i][0] == 'img':
                ips = ImageManager.get(para[i])
                para[i] = ips if ips is None else ips.img

            if i in key and key[i][0] == 'tab':
                tps = TableManager.get(para[i])
                para[i] = tps if tps is None else tps.data

        start = time()
        xlreport.fill_value(wb, info, para)
        wb.save(para['path'])
        self.app.info('%s: cost %.3fs'%(self.title, time()-start))
        self.app.remove_task(self)
        if callback!=None:callback()

    def start(self, para=None, callafter=None):
        wb = pyxl.load_workbook(self.cont)
        xlreport.repair(wb)
        info, key = xlreport.parse(wb)
        if para is not None: 
            return self.runasyn(wb, info, para, callafter)
        dialog = GridDialog(IPy.curapp, self.title, info, key)
        rst = dialog.ShowModal()
        para = dialog.GetValue()
        dialog.Destroy()
        if rst != 5100: return
        filt = '|'.join(['%s files (*.%s)|*.%s'%('XLSX', 'xlsx', 'xlsx')])
        if not self.app.getpath('Save..', filt, 'save', para): return
        win = Source.manager('widget').get('obj', name='Macros Recorder')
        if win!=None: win.write('{}>{}'.format(self.title, para))
        self.runasyn(wb, info, key, para, callafter)

def show_rpt(data, title):
    wx.CallAfter(Report(title, data).start)
    
# ViewerManager.add('rpt', show_rpt)
def read_rpt(path): return path

Source.manager('reader').add(name='rpt', obj=read_rpt, tag='rpt')