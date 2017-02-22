# -*- coding: utf-8 -*
import wx  
from core.loader import loader

def buildMenuBarByPath(parent, path, menuBar=None):
    data = loader.build_plugins(path)
    return buildMenuBar(parent, data, menuBar)

def buildMenuBar(parent, data, menuBar=None):
    if menuBar==None:menuBar = wx.MenuBar()
    for i in data[1]:
        if i[1] == []:continue
        menuBar.Append(buildMenu(parent, i,i[0].title),i[0].title)
    return menuBar
		
def buildMenu(parent, item, curpath):
    menu = wx.Menu()
    for i in item[1]:
        if isinstance(i, tuple):
            nextpath = curpath + '.' + i[0].title
            menu.AppendMenu(-1,i[0].title,buildMenu(parent, i,nextpath))
        else: 
            buildItem(parent, menu, i)
    return menu
	
def buildItem(parent, root, plg):
    if plg=='-':
        root.AppendSeparator()
        return
    mi = wx.MenuItem(root, -1, plg.title)
    parent.Bind(wx.EVT_MENU, lambda x, p=plg:p().start(), mi)
    root.AppendItem(mi)