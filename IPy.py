# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 10:03:00 2016

@author: yxl
"""
from __future__ import absolute_import
from __future__ import print_function

import wx, os
from ui.panelconfig import ParaDialog
from ui.canvasframe import CanvasFrame
from core import managers
from imageplus import ImagePlus
import IPyGL

curapp = None
callafter = wx.CallAfter


def get_window():
    return managers.WindowsManager.get()

def get_ips():
    win = managers.WindowsManager.get()
    return None if win==None else win.canvas.ips

def showips(ips):
    frame = CanvasFrame(curapp)
    frame.set_ips(ips)
    frame.Show()

def show_img(imgs, title):
    ips = ImagePlus(imgs, title)
    showips(ips)
    '''MT
    callafter(showips, ips)
    wx.Yield()
    '''

def show_ips(ips):
    showips(ips)
    ''' MT
    callafter(showips, ips)
    wx.Yield()
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
    dpath = managers.ConfigManager.get('defaultpath')
    if dpath ==None:
        dpath = IPyGL.root_dir # './'
    dic = {'open':wx.FD_OPEN, 'save':wx.FD_SAVE}
    dialog = wx.FileDialog(curapp, title, dpath, '', filt, dic[k])
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
    dialog = wx.DirDialog(curapp, title, IPyGL.root_dir )
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
    TableLog.table(title, data, cols, rows)
    # MT callafter(TableLog.table, *(title, data, cols, rows))

def write(cont, title='ImagePy'):
    from ui.logwindow import TextLog
    TextLog.write(cont, title)
    # MT callafter(TextLog.write, *(cont, title))

def plot(title, gtitle='Graph', labelx='X-Unit', labely='Y-Unit'):
    from ui.plotwindow import PlotFrame
    return PlotFrame.get_frame(title, gtitle, labelx, labely)

def set_progress(i):
    curapp.set_progress(i)
    # MT callafter(curapp.set_progress, i)

def set_info(i):
    curapp.set_info(i)
    # MT callafter(curapp.set_info, i)

def run_macros(cmds):
    for cmd in cmds:
        title, para = cmd.split('>')
        managers.PluginsManager.get(title)().start(eval(para), False)
        # MT wx.Yield()

if __name__ == '__main__':
    app = wx.App(False)
    dlg = wx.ColourDialog(None)
    dlg.GetColourData().SetChooseFull(True)
    if dlg.ShowModal() == wx.ID_OK:
        print(dlg.GetColourData().GetColour())
    dlg.Destroy()
