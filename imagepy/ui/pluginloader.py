# -*- coding: utf-8 -*
import wx  
from ..core.loader import loader
from ..core.manager import ShotcutManager, PluginsManager, LanguageManager
from glob import glob

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
    if menuBar==None:
        menuBar = wx.MenuBar()
    for data in datas[1]:
        if len(data[1]) == 0:
            continue
        LanguageManager.add(data[0].title)
        menuBar.Append(buildMenu(parent, data, data[0].title), LanguageManager.get(data[0].title))
    return menuBar

#!ToDO: tongguo lujing goujian menu 
def buildMenuBarByPath(parent, path, extends, menuBar=None, report=False):
    datas = loader.build_plugins(path, report)
    keydata = {}
    for i in datas[1]:
        if isinstance(i, tuple): keydata[i[0].__name__.split('.')[-1]] = i[1]
    #print(keydata)
    extends = glob(extends+'/*/menus')
    for i in extends:
        plgs = loader.build_plugins(i, report)
        for j in plgs[1]:
            if not isinstance(j, tuple): continue
            name = j[0].__name__.split('.')[-1]
            if name in keydata: 
                keydata[name].extend(j[1])
            else: datas[1].append(j)
        #if len(wgts)!=0: datas[1].extend(wgts[1])
    # print(datas)
    if not menuBar is None:menuBar.SetMenus([])
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
