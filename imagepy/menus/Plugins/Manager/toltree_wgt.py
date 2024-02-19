# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 21:13:16 2017

@author: yxl
"""

from sciapp.action import Free
import wx,os
from imagepy import root_dir
from imagepy.app import loader, ConfigManager, DocumentManager
from wx.py.editor import EditorFrame
#from imagepy.ui.mkdownwindow import HtmlPanel, md2html
from sciwx.text import MDPad
from glob import glob

class Plugin ( wx.Panel ):
    title = 'Tool Tree View'
    single = None
    def __init__( self, parent, app=None):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, 
                            pos = wx.DefaultPosition, size = wx.Size( 500,300 ), 
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.app = app
        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.tre_plugins = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, 
                                        wx.DefaultSize, wx.TR_DEFAULT_STYLE )
        self.tre_plugins.SetMinSize( wx.Size( 200,-1 ) )
        
        bSizer1.Add( self.tre_plugins, 0, wx.ALL|wx.EXPAND, 5 )
        bSizer3 = wx.BoxSizer( wx.VERTICAL )
        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, "Tool Information", 
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
        
        self.txt_info = MDPad( self )
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
                item = self.tre_plugins.AppendItem(parent, i[0].title)
                self.tre_plugins.SetItemData(item, i[0])
                
    def load(self):
        datas = loader.build_tools('tools')
        extends = glob('plugins/*/tools')
        for i in extends:
            tols = loader.build_tools(i)
            if len(tols)!=0: datas[1].extend(tols[1])

        root = self.tre_plugins.AddRoot('Tools')
        for i in datas[1]:
            item = self.tre_plugins.AppendItem(root, i[0].title)
            self.tre_plugins.SetItemData(item, i[0])
            for j in i[1]:
                it = self.tre_plugins.AppendItem(item, j[0].title)
                self.tre_plugins.SetItemData(it, j[0])
    
    # Virtual event handlers, overide them in your derived class
    def on_run( self, event ):
        plg = self.tre_plugins.GetItemData(event.GetItem())
        if hasattr(plg, 'start'):plg().start(self.app)
    
    def on_select( self, event ):
        plg = self.tre_plugins.GetItemData(event.GetItem())
        if plg!=None:
            self.plg = plg
            name = self.tre_plugins.GetItemText(event.GetItem())
            lang = ConfigManager.get('language')
            doc = DocumentManager.get(name, tag=lang)
            doc = doc or DocumentManager.get(name, tag='English')
            self.txt_info.set_cont(doc or 'No Document!')
    
    def on_source(self, event):
        ## TODO: should it be absolute path ?
        filename = self.plg.__module__.replace('.','/')+'.py'
        root = os.path.split(root_dir)[0]
        filename=os.path.join(root,filename)
        EditorFrame(filename=filename).Show()        