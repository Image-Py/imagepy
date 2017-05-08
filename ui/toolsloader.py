# -*- coding: utf-8 -*
import wx, os
import IPy
from core.engine import Tool, Macros
from core.loader import loader

def make_bitmap(bmp):
    img = bmp.ConvertToImage()
    img.Resize((20, 20), (2, 2))
    return img.ConvertToBitmap()

def build_tools(parent, path):
    global host
    host = parent
    data = loader.build_tools(path)
    menuBar = buildToolsBar(parent, data)
    #btn = wx.BitmapButton(parent, wx.ID_ANY, wx.Bitmap('tools/drop.gif'), wx.DefaultPosition, (30,30), wx.BU_AUTODRAW)
    #btn.Bind(wx.EVT_LEFT_DOWN, lambda x:menu_drop(parent, menuBar, data, btn, x))   
    return menuBar#, btn   

def buildToolsBar(parent, data):
    toolbar = wx.Panel( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
    box = wx.BoxSizer( wx.HORIZONTAL )
    toolbar.SetSizer( box )
    #toolbar =  wx.ToolBar( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
    add_tools(toolbar, data[1][0][1], None)
    path = os.path.join(IPy.root_dir, 'tools/drop.gif')
    btn = wx.BitmapButton(toolbar, wx.ID_ANY, make_bitmap(wx.Bitmap(path)), wx.DefaultPosition, (32, 32), wx.BU_AUTODRAW|wx.RAISED_BORDER)
    box.Add(btn)
    btn.Bind(wx.EVT_LEFT_DOWN, lambda x:menu_drop(parent, toolbar, data, btn, x))
    add_tools(toolbar, data[1][1][1])
    return toolbar

def menu_drop(parent, toolbar, data, btn, e):
    menu = wx.Menu()
    for i in data[1][1:]:
        item = wx.MenuItem(menu, wx.ID_ANY, i[0].title, wx.EmptyString, wx.ITEM_NORMAL )
        menu.Append(item)
        parent.Bind(wx.EVT_MENU, lambda x,p=i[1]:add_tools(toolbar, p), item)
    parent.PopupMenu( menu )
    menu.Destroy()
           
def f(plg, e):
    plg.start()
    #print e.GetEventObject().SetBackgroundColour( 
    #    wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
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
    box = bar.GetSizer() 
    if curids!=None:
        for i in curids:
            bar.RemoveChild(i)
            box.Hide(i)
            box.Detach(i)
    if curids!=None:del curids[:]
    for i in data:
        btn = wx.BitmapButton(bar, wx.ID_ANY, make_bitmap(wx.Bitmap(i[1])), wx.DefaultPosition, (32,32), wx.BU_AUTODRAW|wx.RAISED_BORDER )        
        if curids!=None:curids.append(btn)        
        if curids==None:box.Add(btn)
        else: box.Insert(len(box.GetChildren())-2, btn)
        btn.Bind(wx.EVT_LEFT_DOWN, lambda x, p=i[0]:f(p(), x))
        btn.Bind( wx.EVT_ENTER_WINDOW, lambda x, p='"%s" Tool'%i[0].title: set_info(p))        
        if not isinstance(i[0], Macros) and issubclass(i[0], Tool):
            btn.Bind(wx.EVT_LEFT_DCLICK, lambda x, p=i[0]:p().show())
        btn.SetDefault()
    box.Layout()
    bar.Refresh()
    if curids==None:
        sp = wx.StaticLine( bar, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        box.Add( sp, 0, wx.ALL|wx.EXPAND, 2 )
        box.AddStretchSpacer(1)
        
