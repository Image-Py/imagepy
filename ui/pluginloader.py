# -*- coding: utf-8 -*
import wx  
from core.loader import loader
from core.manager import ShotcutManager, PluginsManager

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
            menu.Append(-1,i[0].title,buildMenu(parent, i,nextpath))
        else: 
            buildItem(parent, menu, i)
    return menu
	
def buildItem(parent, root, plg):
    if plg=='-':
        root.AppendSeparator()
        return
    sc = ShotcutManager.get(plg.title)
    title = plg.title if sc==None else plg.title+'\t'+sc
    mi = wx.MenuItem(root, -1, title)
    parent.Bind(wx.EVT_MENU, lambda x, p=plg:p().start(), mi)
    root.Append(mi)

def codeSplit(txt):
    sep = txt.split('-')
    acc, code = wx.ACCEL_NORMAL, -1
    if 'Ctrl' in sep: acc|= wx.ACCEL_CTRL
    if 'Alt' in sep: acc|= wx.ACCEL_ALT
    if 'Shift' in sep: acc|= wx.ACCEL_SHIFT
    fs = ['F%s'%i for i in range(1,13)]
    if sep[-1] in fs:
        code = 340+fs.index(sep[-1])
    elif len(sep[-1])==1: code = ord(sep[-1])
    return acc, code

def buildShortcut(parent):
    shortcuts = []
    for plg in list(PluginsManager.plgs.values()):
        cut = ShotcutManager.get(plg.title)
        if cut!=None:
            acc, code = codeSplit(cut)
            if code==-1: continue;
            nid = wx.NewId()
            parent.Bind(wx.EVT_MENU, lambda x, p=plg:p().start(), id=nid)
            shortcuts.append((acc, code, nid))
    return wx.AcceleratorTable(shortcuts)