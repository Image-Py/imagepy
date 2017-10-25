# -*- coding: utf-8 -*
import wx  
from ..core.loader import loader
from ..core.manager import ShotcutManager, PluginsManager, LanguageManager

def buildItem(parent, root, item):
    if item=='-':
        root.AppendSeparator()
        return
    sc = ShotcutManager.get(item.title)
    LanguageManager.add(item.title)

    title = LanguageManager.get(item.title) if sc==None else LanguageManager.get(item.title)+'\t'+sc

    mi = wx.MenuItem(root, -1, title)
    parent.Bind(wx.EVT_MENU, lambda x, p=item:p().start(), mi)
    root.Append(mi)
    
def buildMenu(parent, data, curpath):
    menu = wx.Menu()
    for item in data[1]:
        if isinstance(item, tuple):
            ## TODO: fixed by auss 
            nextpath = curpath + '.' + item[0].title
            #print(nextpath)
            LanguageManager.add(item[0].title)
            menu.Append(-1, LanguageManager.get(item[0].title), buildMenu(parent, item,nextpath))
        else: 
            buildItem(parent, menu, item)
    return menu

def buildMenuBar(parent, datas, menuBar=None):
    # datas:tuple 
    # datas[1]: list 
    # datas[1][-1]: tuple 
    # datas[1][-1][-1]: list 
    if menuBar==None:
        menuBar = wx.MenuBar()
    for data in datas[1]:
        if len(data[1]) == 0:
            continue
        LanguageManager.add(data[0].title)
        menuBar.Append(buildMenu(parent, data, data[0].title), LanguageManager.get(data[0].title))
    return menuBar


#!ToDO: tongguo lujing goujian menu 
def buildMenuBarByPath(parent, path, menuBar=None):
    datas = loader.build_plugins(path)
    # print(datas)
    return buildMenuBar(parent, datas, menuBar)

def codeSplit(txt):
    sep = txt.split('-')
    acc, code = wx.ACCEL_NORMAL, -1
    if 'Ctrl' in sep: acc|= wx.ACCEL_CTRL
    if 'Alt' in sep: acc|= wx.ACCEL_ALT
    if 'Shift' in sep: acc|= wx.ACCEL_SHIFT
    fs = ['F{}'.format(i) for i in range(1,13)]
    if sep[-1] in fs:
        code = 340+fs.index(sep[-1])
    elif len(sep[-1])==1: code = ord(sep[-1])
    return acc, code

def buildShortcut(parent):
    shortcuts = []
    for item in list(PluginsManager.plgs.values()):
        cut = ShotcutManager.get(item.title)
        if cut!=None:
            acc, code = codeSplit(cut)
            if code==-1: continue;
            nid = wx.NewId()
            parent.Bind(wx.EVT_MENU, lambda x, p=item:p().start(), id=nid)
            shortcuts.append((acc, code, nid))
    return wx.AcceleratorTable(shortcuts)
