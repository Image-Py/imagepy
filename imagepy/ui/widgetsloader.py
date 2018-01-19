# -*- coding: utf-8 -*
# load and build the toolbar 
import wx
import numpy as np
from ..core.loader import loader

def build_widget(parent, datas):
    for i in datas[1]:
        parent.AddPage(i(parent), i.title, False )


def build_widgets_panel(parent, datas):
    wpanel = wx.ScrolledWindow( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
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

def build_widgets(parent, toolspath):
    datas = loader.build_widgets(toolspath)
    return build_widgets_panel(parent, datas)