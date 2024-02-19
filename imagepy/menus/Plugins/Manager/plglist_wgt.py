# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 16:01:14 2017

@author: yxl
"""
import wx, os
#from imagepy import IPy, root_dir

class VirtualListCtrl(wx.ListCtrl):
    def __init__(self, parent, title, data=[]):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VIRTUAL)
        self.title, self.data = title, data
        #self.Bind(wx.EVT_LIST_CACHE_HINT, self.DoCacheItems)
        for col, text in enumerate(title):
            self.InsertColumn(col, text)
        self.set_data(data)
        
    def OnGetItemText(self, row, col):
        return self.data[row][col]
        
    def OnGetItemAttr(self, item):  return None
        
    def OnGetItemImage(self, item): return -1
        
    def set_data(self, data):
        self.data = data
        self.SetItemCount(len(data))
        print(len(data))
        
    def refresh(self):
        self.SetItemCount(len(self.data))
        
class Plugin( wx.Panel ):
    title = 'Plugin List View'
    single = None

    def __init__( self, parent, app=None):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, 
                            pos = wx.DefaultPosition, size = wx.Size( 500,300 ), 
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.app = app
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, "Search", 
                                            wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer2.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.txt_search = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, 
                                       wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.txt_search, 1, wx.ALL, 5 )
        bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
        self.lst_plgs = VirtualListCtrl( self, ['Name', 'Location'])
        self.lst_plgs.SetColumnWidth(0,200)
        self.lst_plgs.SetColumnWidth(1,400)
        bSizer1.Add( self.lst_plgs, 1, wx.ALL|wx.EXPAND, 5 )
        self.SetSizer( bSizer1 )
        self.Layout()
        self.Centre( wx.BOTH )
        # Connect Events
        self.txt_search.Bind( wx.EVT_TEXT, self.on_search )
        self.lst_plgs.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.on_run )
        self.load()
    
    def __del__( self ):
        pass
    
    #def list_plg(self, lst, items
    def load(self):
        lst = [i[1] for i in list(self.app.plugin_manager.gets())]
        self.plgs = [(i.title, i.__module__) for i in lst]
        self.plgs.sort()
        self.buf = self.plgs
        self.lst_plgs.set_data(self.plgs)
    
    # Virtual event handlers, overide them in your derived class
    def on_search( self, event ):
        wd = self.txt_search.GetValue()
        self.buf = [i for i in self.plgs if wd.lower() in i[0].lower()]
        self.lst_plgs.set_data(self.buf)
        self.lst_plgs.Refresh()
        
    def on_run(self, event):
        name=self.buf[event.GetIndex()][0]
        self.app.manager('plugin').get(name)().start(self.app)