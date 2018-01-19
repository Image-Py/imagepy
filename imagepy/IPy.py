# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 10:03:00 2016

@author: yxl
"""
from __future__ import absolute_import
from __future__ import print_function

import wx, os
from wx.lib.pubsub import pub

from .core import manager
from .imageplus import ImagePlus
from . import root_dir

aui = manager.ConfigManager.get('uistyle') != 'ij'
curapp = None

def get_window():
    return manager.WindowsManager.get()

def get_ips():
    win = manager.WindowsManager.get()
    return None if win==None else win.canvas.ips

def showips(ips):
    if aui:
        from .ui.canvasframe import CanvasPanel
        canvasp = CanvasPanel(curapp.canvasnb)
        curapp.canvasnb.add_page( canvasp, ips)
        #canvasp.canvas.initBuffer()
        canvasp.set_ips(ips)
        curapp.auimgr.Update()
    else:
        from .ui.canvasframe import CanvasFrame
        frame = CanvasFrame(curapp)
        frame.set_ips(ips)
        frame.Show()   

pub.subscribe(showips, 'showips')
def show_ips(ips):
    wx.CallAfter(pub.sendMessage, 'showips', ips=ips) 

def showimg(imgs, title):
    print('show img')
    ips = ImagePlus(imgs, title)
    showips(ips)

pub.subscribe(showimg, 'showimg')
def show_img(imgs, title):
    wx.CallAfter(pub.sendMessage, 'showimg', imgs=imgs, title=title) 

def showmd(title, cont, url=''):
    from .ui.mkdownwindow import MkDownWindow
    MkDownWindow(curapp, title, cont, url).Show()

pub.subscribe(showmd, 'showmd')
def show_md(title, cont, url=''):
    wx.CallAfter(pub.sendMessage, 'showmd', title=title, cont=cont, url=url)
'''
def stepmacros(macros):
    macros.next()

pub.subscribe(stepmacros, 'stepmacros')
def step_macros(macros):
    wx.CallAfter(pub.sendMessage, "stepmacros", macros=macros)
'''
def alert(info, title="ImagePy Alert!"):
    dlg=wx.MessageDialog(curapp, info, title, wx.OK)
    dlg.ShowModal()
    dlg.Destroy()

# MT alert = lambda info, title='image-py':callafter(alert_, *(info, title))

def yes_no(info, title="ImagePy Yes-No ?!"):
    dlg = wx.MessageDialog(curapp, info, title, wx.YES_NO | wx.CANCEL)
    rst = dlg.ShowModal()
    dlg.Destroy()
    dic = {wx.ID_YES:'yes', wx.ID_NO:'no', wx.ID_CANCEL:'cancel'}
    return dic[rst]

def getpath(title, filt, k, para=None):
    """Get the defaultpath of the ImagePy"""
    dpath = manager.ConfigManager.get('defaultpath')
    if dpath ==None:
        dpath = root_dir # './'
    dic = {'open':wx.FD_OPEN, 'save':wx.FD_SAVE}
    dialog = wx.FileDialog(curapp, title, dpath, '', filt, dic[k])
    rst = dialog.ShowModal()
    path = None
    if rst == wx.ID_OK:
        path = dialog.GetPath()
        dpath = os.path.split(path)[0]
        manager.ConfigManager.set('defaultpath', dpath)
        if para!=None:para['path'] = path
    dialog.Destroy()

    return rst if para!=None else path

def getdir(title, filt, para=None):
    dpath = manager.ConfigManager.get('defaultpath')
    if dpath ==None:
        dpath = root_dir
    dialog = wx.DirDialog(curapp, title, dpath )
    rst = dialog.ShowModal()
    path = None
    if rst == wx.ID_OK:
        path = dialog.GetPath()
        if para!=None:para['path'] = path
    dialog.Destroy()
    return rst if para!=None else path

def get_para(title, view, para):
    from .ui.panelconfig import ParaDialog
    pd = ParaDialog(curapp, title)
    pd.init_view(view, para)
    rst = pd.ShowModal()
    pd.Destroy()
    return rst

def showtable(title, data, cols=None, rows=None):
    from .ui.tablewindow import TableLog
    TableLog.table(title, data, cols, rows)
    # MT callafter(TableLog.table, *(title, data, cols, rows))
    
pub.subscribe(showtable, 'showtable')
def table(title, data, cols=None, rows=None):
    wx.CallAfter(pub.sendMessage, "showtable", title=title, data=data, cols=cols, rows=rows) 

def showlog(title, cont):
    from .ui.logwindow import TextLog
    TextLog.write(cont, title)
pub.subscribe(showlog, 'showlog')

def write(cont, title='ImagePy'):
    from .ui.logwindow import TextLog
    wx.CallAfter(pub.sendMessage, 'showlog', title=title, cont=cont)

def plot(title, gtitle='Graph', labelx='X-Unit', labely='Y-Unit'):
    from .ui.plotwindow import PlotFrame
    return PlotFrame.get_frame(title, gtitle, labelx, labely)

#def set_progress(i):
#    curapp.set_progress(i)
    # MT callafter(curapp.set_progress, i)

def set_info(i):
    curapp.set_info(i)
    # MT callafter(curapp.set_info, i)

def run(cmd):
    title, para = cmd.split('>')
    manager.PluginsManager.get(title)().start(eval(para), False)