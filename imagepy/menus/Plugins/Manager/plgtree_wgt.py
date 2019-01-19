# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 01:00:02 2017

@author: yxl
"""

from imagepy.core.engine import Free
import wx,os
from imagepy import IPy, root_dir
from imagepy.core.loader import loader
from wx.py.editor import EditorFrame
from imagepy.ui.mkdownwindow import HtmlPanel, md2html
from imagepy.core.manager import DocumentManager
from glob import glob

class Plugin ( wx.Panel ):
    title = 'Plugin Tree View'
    single = None
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, 
                            pos = wx.DefaultPosition, size = wx.Size( 500,300 ), 
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.tre_plugins = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, 
                                        wx.DefaultSize, wx.TR_DEFAULT_STYLE )
        self.tre_plugins.SetMinSize( wx.Size( 300,-1 ) )
        
        bSizer1.Add( self.tre_plugins, 0, wx.ALL|wx.EXPAND, 5 )
        bSizer3 = wx.BoxSizer( wx.VERTICAL )
        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, "Plugin Infomation:",
                                            wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        bSizer4.Add( self.m_staticText2, 0, wx.ALL, 5 )
        
        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, "[SourceCode]", 
                                            wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        self.m_staticText3.SetForegroundColour(
            wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        
        bSizer4.Add( self.m_staticText3, 0, wx.ALL, 5 )
        bSizer3.Add( bSizer4, 0, wx.EXPAND, 5 )
        
        self.txt_info = HtmlPanel( self )
        bSizer3.Add( self.txt_info, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.tre_plugins.Bind( wx.EVT_TREE_ITEM_ACTIVATED, self.on_run )
        self.tre_plugins.Bind( wx.EVT_TREE_SEL_CHANGED, self.on_select )
        self.m_staticText3.Bind( wx.EVT_LEFT_DOWN, self.on_source )
        self.plg = None
        self.load()
        
    def addnode(self, parent, data):
        for i in data:
            if i=='-':continue
            if isinstance(i, tuple):
                item = self.tre_plugins.AppendItem(parent, i[0].title)
                self.tre_plugins.SetItemData(item, i[0])
                self.addnode(item, i[1])
            else:
                item = self.tre_plugins.AppendItem(parent, i.title)
                self.tre_plugins.SetItemData(item, i)
                
    def load(self):
        datas = loader.build_plugins('menus')
        keydata = {}
        for i in datas[1]:
            if isinstance(i, tuple): keydata[i[0].__name__.split('.')[-1]] = i[1]
        #print(keydata)
        extends = glob('plugins/*/menus')
        for i in extends:
            plgs = loader.build_plugins(i)
            for j in plgs[1]:
                if not isinstance(j, tuple): continue
                name = j[0].__name__.split('.')[-1]
                if name in keydata: 
                    keydata[name].extend(j[1])
                else: datas[1].append(j)
        root = self.tre_plugins.AddRoot('Plugins')
        self.addnode(root, datas[1])
    
    # Virtual event handlers, overide them in your derived class
    def on_run( self, event ):
        plg = self.tre_plugins.GetItemPyData(event.GetItem())
        if hasattr(plg, 'start'):plg().start()
    
    def on_select( self, event ):
        plg = self.tre_plugins.GetItemData(event.GetItem())
        if plg!=None:
            self.plg = plg
            name = self.tre_plugins.GetItemText(event.GetItem())
            self.txt_info.SetValue((md2html(DocumentManager.get(name)), ''))
        
    def on_source(self, event):
        ## TODO: should it be absolute path ?
        filename = self.plg.__module__.replace('.','/')+'.py'
        #print('==========', filename)
        root = os.path.split(root_dir)[0]
        filename=os.path.join(root,filename)
        #print(filename)
        EditorFrame(filename=filename).Show()