# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 01:48:23 2016
@author: yxl
"""
import wx
from imagepy import IPy
from imagepy.core.manager import WidgetsManager, TaskManager, ImageManager
from imagepy.core.manager import ReaderManager, ViewerManager, TableManager
from imagepy.ui.propertygrid import GridDialog
from imagepy.core.util import xlreport
from time import time
import openpyxl as pyxl

class Report:
    def __init__(self, title, cont):
        self.title = title
        self.cont = cont
        
    def __call__(self): return self

    def runasyn(self,  wb, info, key, para = None, callback = None):
        TaskManager.add(self)
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
        IPy.set_info('%s: cost %.3fs'%(self.title, time()-start))
        TaskManager.remove(self)
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
        if not IPy.getpath('Save..', filt, 'save', para): return
        win = WidgetsManager.getref('Macros Recorder')
        if win!=None: win.write('{}>{}'.format(self.title, para))
        self.runasyn(wb, info, key, para, callafter)

def show_rpt(data, title):
    wx.CallAfter(Report(title, data).start)
    
ViewerManager.add('rpt', show_rpt)
def read_rpt(path): return path
ReaderManager.add('rpt', read_rpt, tag='rpt')