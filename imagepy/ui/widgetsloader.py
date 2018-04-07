# -*- coding: utf-8 -*
# load and build the toolbar 
import wx
import numpy as np
from ..core.loader import loader
from glob import glob

def build_widget(parent, datas):
    for i in datas[1]:
        parent.AddPage(i(parent), i.title, False )


def build_widgets_panel(parent, datas, wpanel):
    if wpanel is None:
        wpanel = wx.ScrolledWindow( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
    else: wpanel.DestroyChildren()
    wpanel.SetScrollRate( 5, 5 ) 
    sizer = wx.BoxSizer( wx.VERTICAL )
    for i in datas[1]:
        choicebook = wx.Choicebook( wpanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.CHB_DEFAULT )
        build_widget(choicebook, i)
        sizer.Add( choicebook, 0, wx.EXPAND |wx.ALL, 0 )
    wpanel.SetSizer( sizer )
    wpanel.Layout()
    sizer.Fit( wpanel )
    return wpanel

def build_widgets(parent, toolspath, extends, panel=None):
    datas = loader.build_widgets(toolspath)
    extends = glob(extends+'/*/widgets')
    for i in extends:
        wgts = loader.build_widgets(i)
        if len(wgts)!=0: datas[1].extend(wgts[1])
    return build_widgets_panel(parent, datas, panel)