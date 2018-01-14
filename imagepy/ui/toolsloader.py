# -*- coding: utf-8 -*
# load and build the toolbar 
import wx  
import os
from .. import IPy
from .. import root_dir 
from ..core.engine import Tool, Macros
from ..core.loader import loader


def make_bitmap(bmp):
    img = bmp.ConvertToImage()
    img.Resize((20, 20), (2, 2))
    return img.ConvertToBitmap()

def build_tools(parent, toolspath):
    global host
    host = parent
    ## get tool datas from the loader.build_tools(toolspath)
    ## then generate toolsbar
    datas = loader.build_tools(toolspath)
    toolsbar = buildToolsBar(parent, datas)
    gifpath = os.path.join(root_dir, "tools/drop.gif")
    #btn = wx.BitmapButton(parent, wx.ID_ANY, wx.Bitmap(gifpath), wx.DefaultPosition, (30,30), wx.BU_AUTODRAW)
    #btn.Bind(wx.EVT_LEFT_DOWN, lambda x:menu_drop(parent, toolsbar, datas, btn, x))   
    return toolsbar#, btn   

def buildToolsBar(parent, datas):    
    box = wx.BoxSizer( wx.HORIZONTAL )
    #toolsbar =  wx.ToolBar( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
    toolsbar = wx.Panel( parent, wx.ID_ANY, 
                         wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
    
    toolsbar.SetSizer( box )
    add_tools(toolsbar, datas[1][0][1], None)
    
    gifpath = os.path.join(root_dir, "tools/drop.gif")
    btn = wx.BitmapButton(toolsbar, wx.ID_ANY, make_bitmap(wx.Bitmap(gifpath)),
                          wx.DefaultPosition, (32, 32), wx.BU_AUTODRAW|wx.RAISED_BORDER)

    box.Add(btn)
    btn.Bind(wx.EVT_LEFT_DOWN, lambda x:menu_drop(parent, toolsbar, datas, btn, x))
    add_tools(toolsbar, datas[1][1][1])
    toolsbar.Fit()
    return toolsbar

def menu_drop(parent, toolbar, datas, btn, e):
    menu = wx.Menu()
    for data in datas[1][1:]:
        item = wx.MenuItem(menu, wx.ID_ANY, data[0].title, wx.EmptyString, wx.ITEM_NORMAL )
        menu.Append(item)
        parent.Bind(wx.EVT_MENU, lambda x,p=data[1]:add_tools(toolbar, p), item)
    parent.PopupMenu( menu )
    menu.Destroy()
           
def f(plg, e):
    ##! TODO: What's this? for wx.EVT_LEFT_DOWN
    plg.start()
    #print e.GetEventObject().SetBackgroundColour( 
    #    wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
    if isinstance(plg, Tool): 
        e.Skip()
        
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
        
def add_tools(bar, datas, curids=[]):
    ##! TODO: 
    ## datas? dirpath tree to generate menus/toolsbar?
    ## curids? ??
    box = bar.GetSizer() 
    if curids!=None:
        for curid in curids:
            bar.RemoveChild(curid)
            box.Hide(curid)
            box.Detach(curid)
    if curids!=None:
        del curids[:]
    for data in datas:
        btn = wx.BitmapButton(bar, wx.ID_ANY, 
                              make_bitmap(wx.Bitmap(data[1])), 
                              wx.DefaultPosition, (32,32), 
                              wx.BU_AUTODRAW|wx.RAISED_BORDER )        
        if curids!=None:
            curids.append(btn)        
        if curids==None:
            box.Add(btn)
        else: 
            box.Insert(len(box.GetChildren())-2, btn)
            
        btn.Bind( wx.EVT_LEFT_DOWN, lambda x, p=data[0]:f(p(), x))
        btn.Bind( wx.EVT_ENTER_WINDOW, 
                  lambda x, p='"{}" Tool'.format(data[0].title): set_info(p))        
        if not isinstance(data[0], Macros) and issubclass(data[0], Tool):
            btn.Bind(wx.EVT_LEFT_DCLICK, lambda x, p=data[0]:p().show())
        btn.SetDefault()
    box.Layout()
    bar.Refresh()
    if curids==None:
        sp = wx.StaticLine( bar, wx.ID_ANY, 
                            wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        box.Add( sp, 0, wx.ALL|wx.EXPAND, 2 )
        box.AddStretchSpacer(1)