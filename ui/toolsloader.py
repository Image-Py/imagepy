# -*- coding: utf-8 -*
import wx  
import os
import IPy
from core.engines import Tool, Macros
from core.loader import loader

def build_tools(parent, path):
    global host
    host = parent
    data = loader.build_tools(path)
    menuBar = buildToolsBar(parent, data)
    btn = wx.BitmapButton(parent, wx.ID_ANY, wx.Bitmap('tools/drop.gif'), wx.DefaultPosition, (30,30), wx.BU_AUTODRAW)
    btn.Bind(wx.EVT_LEFT_DOWN, lambda x:menu_drop(parent, menuBar, data, btn, x))   
    return menuBar, btn   

def buildToolsBar(parent, data):
    toolbar =  wx.ToolBar( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
    add_tools(toolbar, data[1][0][1], None)
    add_tools(toolbar, data[1][1][1])
    return toolbar

def menu_drop(parent, toolbar, data, btn, e):
    menu = wx.Menu()
    for i in data[1][1:]:
        item = wx.MenuItem(menu, wx.ID_ANY, i[0].title, wx.EmptyString, wx.ITEM_NORMAL )
        menu.AppendItem(item)
        parent.Bind(wx.EVT_MENU, lambda x,p=i[1]:add_tools(toolbar, p), item)
    parent.PopupMenu( menu )
    menu.Destroy()
           
def f(plg, e):
    plg.start()
    if isinstance(plg, Tool): e.Skip()
        
def set_info(value):
    IPy.curapp.set_info(value)
        
def setting(tol, btn):
    if not hasattr(tol, 'view'):return
    if isinstance(tol.view, list):    
        para = dict(tol.para)
        rst = IPy.getpara(tol.title, tol.view, para)
        if rst!=None: tol.para = rst
    else:
        tol().view(btn)
        
def add_tools(bar, data, curids=[]):
    if curids!=None:
        for i in curids:bar.DeleteTool(i)
    if curids!=None:del curids[:]
    for i in data:
        btn = wx.BitmapButton(bar, wx.ID_ANY, wx.Bitmap(i[1]), wx.DefaultPosition, (30, 30), wx.BU_AUTODRAW|wx.RAISED_BORDER )        
        if curids!=None:curids.append(btn.GetId())        
        bar.AddControl(btn)          
        btn.Bind(wx.EVT_LEFT_DOWN, lambda x, p=i[0]:f(p(), x))
        btn.Bind( wx.EVT_ENTER_WINDOW, lambda x, p='"%s" Tool'%i[0].title: set_info(p))        
        if not isinstance(i[0], Macros) and issubclass(i[0], Tool):
            btn.Bind(wx.EVT_LEFT_DCLICK, lambda x, p=i[0]:p().config())
        btn.SetDefault() 
    if curids==None:bar.AddSeparator()