# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 10:03:00 2016

@author: yxl
"""
import wx, os
from ui.panelconfig import ParaDialog
from core import managers

curapp = None

callafter = wx.CallAfter

def get_window():
    return managers.WindowsManager.get()
    
def get_ips():
    win = managers.WindowsManager.get()
    if win==None:return None
    return win.canvas.ips
    
def showips(ips):
    from ui.canvasframe import CanvasFrame
    frame = CanvasFrame(curapp)
    frame.set_ips(ips)
    frame.Show()
    
def show_img(imgs, title):
    from imageplus import ImagePlus
    ips = ImagePlus(imgs, title)
    callafter(showips, ips)
    wx.Yield()

def show_ips(ips):
    callafter(showips, ips)
    wx.Yield()
    
def alert_(info, title='image-py'):
    dlg=wx.MessageDialog(curapp, info, title, wx.OK)
    dlg.ShowModal()
    dlg.Destroy()

alert = lambda info, title='image-py':callafter(alert_, *(info, title))
    
def yes_no(info, title='image-py'):
    dlg = wx.MessageDialog(curapp, info, title, wx.YES_NO | wx.CANCEL) 
    rst = dlg.ShowModal()  
    dlg.Destroy()
    dic = {wx.ID_YES:'yes', wx.ID_NO:'no', wx.ID_CANCEL:'cancel'}
    return dic[rst]
    
def getpath(title, filt, para=None):
    dpath = managers.ConfigManager.get('defaultpath')
    if dpath ==None: dpath = './'
    dialog = wx.FileDialog(curapp, title, dpath, '', filt, wx.FD_OPEN)
    rst = dialog.ShowModal() 
    path = None
    if rst == wx.ID_OK:
        path = dialog.GetPath()
        dpath = os.path.split(path)[0]
        managers.ConfigManager.set('defaultpath', dpath)
        if para!=None:para['path'] = path
    dialog.Destroy()
    
    return rst if para!=None else path
    
def getdir(title, filt, para=None):
    dialog = wx.DirDialog(curapp, title, './')
    rst = dialog.ShowModal() 
    path = None
    if rst == wx.ID_OK:
        path = dialog.GetPath()
        if para!=None:para['path'] = path
    dialog.Destroy()
    return rst if para!=None else path
    
def get_para(title, view, para):
    pd = ParaDialog(curapp, title)
    pd.init_view(view, para)
    rst = pd.ShowModal()
    pd.Destroy()
    return rst
    
def table(title, data, cols=None, rows=None):
    from ui.tablewindow import TableLog
    callafter(TableLog.table, *(title, data, cols, rows))
    
def write(cont, title='ImagePy'):
    from ui.logwindow import TextLog
    callafter(TextLog.write, *(cont, title))
    
def set_progress(i):
    callafter(curapp.set_progress, i)
    
def set_info(i):
    callafter(curapp.set_info, i)
    
def run_macros(cmds):
    for i in cmds:
        title, para = i.split('>')
        managers.PluginsManager.get(title)().start(eval(para), False)
        wx.Yield()
        
if __name__ == '__main__':
    app = wx.App(False)
    dlg = wx.ColourDialog(None)
    dlg.GetColourData().SetChooseFull(True)
    if dlg.ShowModal() == wx.ID_OK:
        print dlg.GetColourData().GetColour()
    dlg.Destroy()