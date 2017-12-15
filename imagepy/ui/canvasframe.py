# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 01:24:41 2016

@author: yxl
"""
import wx, os
from .canvas import Canvas
from ..core.manager import WindowsManager
from ..core.manager import ShotcutManager,PluginsManager
from .. import IPy, root_dir

class CanvasPanel(wx.Panel):
    """CanvasFrame: derived from the wx.core.Frame"""
    ## TODO: Main frame ???
    def __init__(self, parent=None):
        wx.Frame.__init__ ( self, parent)

        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
        
        self.SetSizeHints( wx.Size( 560,-1 ), wx.DefaultSize )
        WindowsManager.add(self)
        print('frame added')
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

        sizer = wx.BoxSizer( wx.VERTICAL )
        self.txt_info = wx.StaticText( self, wx.ID_ANY,
                                       '500*500 pixels 173k',
                                       wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txt_info.Wrap( -1 )
        sizer.Add( self.txt_info, 0, wx.ALL, 0 )

        self.canvas = Canvas(self)
        self.canvas.fit = self

        sizer.Add( self.canvas, 1, wx.EXPAND |wx.ALL, 0 )

        self.page = wx.ScrollBar( self, wx.ID_ANY,
                                  wx.DefaultPosition, wx.DefaultSize, wx.SB_HORIZONTAL)

        self.page.SetScrollbar(0,0,0,0, refresh=True)
        sizer.Add( self.page, 0, wx.ALL|wx.EXPAND, 0 )
        #self.page.Hide()
        self.SetSizer(sizer)
        self.Layout()

        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Bind(wx.EVT_SCROLL, self.on_scroll)
        self.Bind(wx.EVT_ACTIVATE, self.on_valid)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.canvas.Bind(wx.EVT_CHAR, self.on_key)
        self.canvas.SetFocus()
        # panel.Bind(wx.EVT_CHAR, self.OnKeyDown)
        self.opage = 0
        self.Fit()

        self.SetAcceleratorTable(IPy.curapp.shortcut)

    def on_idle(self, event):
        if self.ips.update:
            self.set_info(self.ips)
        if False and self.canvas.resized:
            print(self.GetParent())
            self.Fit()
            #self.GetParent().Fit()
            #print 'fit'
            self.canvas.resized = False

    def on_key(self, event):
        if event.GetKeyCode()==27:
            self.ips.tool=None
            self.SetTitle(self.ips.title)

    def on_valid(self, event):
        if event.GetActive():
            WindowsManager.add(self)

    def on_close(self, event):
        WindowsManager.remove(self)
        self.Destroy()

    def set_info(self, ips):
        #self.GetParent().SetTitle(ips.title)
        if ips.tool != None: self.SetTitle(ips.title + ' [CustomTool]')
        stk = 'stack' if ips.is3d else 'list'
        label="{}/{}; {}  {}x{} pixels; {}; {} M".format(ips.cur+1, ips.get_nslices(),
            stk if ips.get_nslices()>1 else '',ips.size[0], ips.size[1],
            ips.imgtype, round(ips.get_nbytes()/1024.0/1024.0, 2))
        self.txt_info.SetLabel(label)

        if ips.get_nslices() == self.opage:
            return
        self.opage = ips.get_nslices()
        if ips.get_nslices()==1 and self.page.Shown:
            self.page.Hide()
            self.Fit()
        elif not self.page.Shown:
            self.page.Show()
            self.Fit()
        self.page.SetScrollbar(0, 0, ips.get_nslices()-1, 0, refresh=True)
        print('CanvasFrame:set_info')
        #self.page.Show()

    def set_ips(self, ips):
        self.ips = ips
        self.set_info(ips)
        self.canvas.set_ips(ips)
        print('CanvasFrame:set_ips')

    def on_scroll(self, event):
        self.ips.cur = self.page.GetThumbPosition()
        self.ips.update = 'pix'
        self.on_idle(None)
        self.canvas.on_idle(None)


class CanvasFrame(wx.Frame):
    """CanvasFrame: derived from the wx.core.Frame"""
    ## TODO: Main frame ???
    def __init__(self, parent=None):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
                            title = wx.EmptyString,
                            pos = wx.DefaultPosition,
                            size = wx.Size( -1,-1 ),
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.canvaspanel = CanvasPanel(self)
        logopath = os.path.join(root_dir, 'data/logo.ico')
        self.SetIcon(wx.Icon(logopath, wx.BITMAP_TYPE_ICO))
        self.set_ips = self.canvaspanel.set_ips

if __name__=='__main__':
    app = wx.PySimpleApp()
    CanvasFrame().Show(True)
    app.MainLoop()
