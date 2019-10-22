# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 23:23:30 2017

@author: yxl
"""
import wx, os, sys
import time, threading
from .. import IPy, root_dir
# TODO: @2017.05.01
#from ui import pluginloader, toolsloader
from . import pluginloader, toolsloader, widgetsloader
from ..core.manager import ConfigManager, PluginsManager, TaskManager, ImageManager
from ..core.loader import loader
from ..core.engine import Macros
from .canvasframe import CanvasNoteBook
from .tableframe import TableNoteBook
#import aui as aui
import wx.lib.agw.aui as aui

class FileDrop(wx.FileDropTarget):
    def OnDropFiles(self, x, y, path):
        print(["Open>{'path':'%s'}"%i for i in path])
        Macros('noname', ["Open>{'path':'%s'}"%i.replace('\\', '/') for i in path]).start()
        return 0

class ImagePy(wx.Frame):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = 'ImagePy', 
                            size = wx.Size(-1,-1), pos = wx.DefaultPosition, 
                            style = wx.RESIZE_BORDER|wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.auimgr = aui.AuiManager()
        self.auimgr.SetManagedWindow( self )
        #self.auimgr.SetFlags(aui.AUI_MGR_DEFAULT)

        logopath = os.path.join(root_dir, 'data/logo.ico')
        #self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
        self.SetIcon(wx.Icon(logopath, wx.BITMAP_TYPE_ICO))
        IPy.curapp = self
        self.SetSizeHints( wx.Size(1024,768) if IPy.uimode() == 'ipy' else wx.Size( 700,-1 ))
        

        self.menubar = pluginloader.buildMenuBarByPath(self, 'menus', 'plugins', None, True)
        self.SetMenuBar( self.menubar )
        self.shortcut = pluginloader.buildShortcut(self)
        self.SetAcceleratorTable(self.shortcut)
        #sizer = wx.BoxSizer(wx.VERTICAL)
        self.toolbar = toolsloader.build_tools(self, 'tools', 'plugins', None, True)

        
        print(IPy.uimode())
        if IPy.uimode()=='ipy': self.load_aui()
        else: self.load_ijui()
        self.load_document()
        self.Fit()


        self.stapanel = stapanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizersta = wx.BoxSizer( wx.HORIZONTAL )
        self.txt_info = wx.StaticText( stapanel, wx.ID_ANY, "ImagePy  v0.2", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txt_info.Wrap( -1 )
        #self.txt_info.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
        sizersta.Add( self.txt_info, 1, wx.ALIGN_BOTTOM|wx.BOTTOM|wx.LEFT|wx.RIGHT, 2 )
        self.pro_bar = wx.Gauge( stapanel, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 100,15 ), wx.GA_HORIZONTAL )
        sizersta.Add( self.pro_bar, 0, wx.ALIGN_BOTTOM|wx.BOTTOM|wx.LEFT|wx.RIGHT, 2 )
        stapanel.SetSizer(sizersta)
        stapanel.SetDropTarget(FileDrop())
        self.auimgr.AddPane( stapanel,  aui.AuiPaneInfo() .Bottom() .CaptionVisible( False ).PinButton( True )
            .PaneBorder( False ).Dock().Resizable().FloatingSize( wx.DefaultSize ).DockFixed( True )
            . MinSize(wx.Size(-1, 20)). MaxSize(wx.Size(-1, 20)).Layer( 10 ) )


        self.Centre( wx.BOTH )
        self.Layout()
        self.auimgr.Update()
        self.Fit()
        self.Centre( wx.BOTH )
        if(IPy.uimode()=='ij'):
            self.SetMaxSize((-1, self.GetSize()[1]))
            self.SetMinSize(self.GetSize())
        self.update = False

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(aui.EVT_AUI_PANE_CLOSE, self.on_pan_close)
        thread = threading.Thread(None, self.hold, ())
        thread.setDaemon(True)
        thread.start()

    def load_aui(self):
        self.toolbar.GetSizer().SetOrientation(wx.VERTICAL)
        self.toolbar.GetSizer().Layout()
        self.toolbar.Fit()
        self.auimgr.AddPane(self.toolbar, aui.AuiPaneInfo() .Left()  .PinButton( True )
            .CaptionVisible( True ).Dock().Resizable().FloatingSize( wx.DefaultSize ).MaxSize(wx.Size( 32,-1 ))
            . BottomDockable( True ).TopDockable( False ).Layer( 10 ) )
        self.widgets = widgetsloader.build_widgets(self, 'widgets', 'plugins')
        self.auimgr.AddPane( self.widgets, aui.AuiPaneInfo() .Right().Caption('Widgets') .PinButton( True )
            .Dock().Resizable().FloatingSize( wx.DefaultSize ).MinSize( wx.Size( 266,-1 ) ) .Layer( 10 ) )
        
        self.canvasnbwrap = wx.Panel(self)
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.canvasnb = CanvasNoteBook( self.canvasnbwrap)
        sizer.Add( self.canvasnb, 1, wx.EXPAND |wx.ALL, 0 )
        self.canvasnbwrap.SetSizer( sizer )
        self.canvasnbwrap.Layout()
        self.auimgr.AddPane( self.canvasnbwrap, aui.AuiPaneInfo() .Center() .CaptionVisible( False ).PinButton( True ).Dock()
            .PaneBorder( False ).Resizable().FloatingSize( wx.DefaultSize ). BottomDockable( True ).TopDockable( False )
            .LeftDockable( True ).RightDockable( True ) )

        self.tablenbwrap = wx.Panel(self)
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.tablenb = TableNoteBook( self.tablenbwrap)
        sizer.Add( self.tablenb, 1, wx.EXPAND |wx.ALL, 0 )
        self.tablenbwrap.SetSizer( sizer )
        self.tablenbwrap.Layout()

        self.auimgr.AddPane( self.tablenbwrap, aui.AuiPaneInfo() .Bottom() .CaptionVisible( True ).PinButton( True ).Dock().Hide()
            .MaximizeButton( True ).Resizable().FloatingSize((800, 600)).BestSize(( 120,120 )). Caption('Tables') . 
            BottomDockable( True ).TopDockable( False ).LeftDockable( True ).RightDockable( True ) )
        img = ConfigManager.get('watermark') or ''
        if not os.path.exists(img): img = 'data/watermark.png'
        self.set_background(img)
        #self.auimgr.SetArtProvider(MyArtProvider())
        #self.canvasnb.Bind( aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_pagevalid)        

    def load_ijui(self):
        self.auimgr.AddPane(self.toolbar, aui.AuiPaneInfo() .Top() .CaptionVisible( False ).PinButton( True )
            .PaneBorder( False ).Dock().Resizable().FloatingSize( wx.DefaultSize ).DockFixed( True ) 
            .BottomDockable( False ).TopDockable( False ).LeftDockable( False ).RightDockable( False )
            .MinSize(wx.Size(-1, 32)). Layer( 10 ) )
        self.widgets = widgetsloader.build_widgets(self, 'widgets', 'plugins')
        self.auimgr.AddPane( self.widgets, aui.AuiPaneInfo() .Right().Caption('Widgets') .PinButton( True )
            .Float().Resizable().FloatingSize( wx.DefaultSize ).MinSize( wx.Size( 266,-1 ) ).Hide() .Layer( 10 ) )
        
    def load_dev(self):
        return
        self.devpan = aui.AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE )
        self.auimgr.AddPane( self.devpan, waui.AuiPaneInfo() .Bottom() .CaptionVisible( False ).PinButton( True ).Dock()
            .PaneBorder( False ).Resizable().FloatingSize( wx.DefaultSize ) )

    def on_pan_close(self, event):
        if event.GetPane().window in [self.toolbar, self.widgets]:
            event.Veto()
        if hasattr(event.GetPane().window, 'close'):
            event.GetPane().window.close()

    def load_document(self):
        from glob import glob
        extends = glob('plugins/*/doc')
        for i in extends: loader.build_document(i)
        loader.build_document('doc')

    def reload_plugins(self, report=False, menus=True, tools=False, widgets=False):
        if menus: pluginloader.buildMenuBarByPath(self, 'menus', 'plugins', self.menubar, report)
        if tools: toolsloader.build_tools(self, 'tools', 'plugins', self.toolbar, report)
        if widgets: widgetsloader.build_widgets(self, 'widgets', 'plugins', self.widgets)
        self.load_document()
        if IPy.uimode()!='ipy': self.Fit()

    def hold(self):
        dire = 1
        while True:
            try:
                if time == None: break
                time.sleep(0.05)
                tasks = TaskManager.get()
                if(len(tasks)==0):
                    if self.pro_bar.IsShown():
                        wx.CallAfter(self.set_progress, -1)
                    continue
                arr = [i.prgs for i in tasks]
                if (None, 1) in arr:
                    if self.pro_bar.GetValue()<=0:
                        dire = 1
                    if self.pro_bar.GetValue()>=100:
                        dire = -1
                    v = self.pro_bar.GetValue()+dire*5
                    wx.CallAfter(self.set_progress, v)
                else:
                    v = max([(i[0]+1)*100.0/i[1] for i in arr])
                    wx.CallAfter(self.set_progress, v)
            except: 
                pass
    def set_info(self, value):
        self.txt_info.SetLabel(value)

    def set_progress(self, value):
        v = max(min(value, 100), 0)
        self.pro_bar.SetValue(v)
        if value==-1:
            self.pro_bar.Hide()
        elif not self.pro_bar.IsShown():
            self.pro_bar.Show()
            self.stapanel.GetSizer().Layout()
        self.pro_bar.Update()

    def set_color(self, value):
        self.line_color.SetBackgroundColour(value)

    def set_background(self, img):
        if IPy.uimode()!='ipy': return
        self.canvasnb.set_background(img)

    def on_close(self, event):
        print('close')
        ConfigManager.write()
        self.auimgr.UnInit()
        del self.auimgr
        self.Destroy()
        sys.exit()

    def __del__( self ):
        pass

if __name__ == '__main__':
    app = wx.App(False)
    mainFrame = ImagePy(None)
    mainFrame.Show()
    app.MainLoop()
