import wx, os, sys
import pluginloader, toolsloader, IPy

class ImagePy(wx.Frame):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = 'ImagePy', size = wx.Size(560,-1), pos = wx.DefaultPosition, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHintsSz( wx.Size( 560,-1 ), wx.DefaultSize )
        self.Layout()
        IPy.curapp = self
        self.menubar = pluginloader.buildMenuBarByPath(self, 'menus')
        self.SetMenuBar( self.menubar )
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizertool = wx.BoxSizer( wx.HORIZONTAL )
        self.toolbar, self.morebar = toolsloader.build_tools(self, 'tools')
        
        self.toolbar.Realize() 
        sizertool.Add(self.toolbar, 1, 0, 5 )
        sizertool.Add(self.morebar, 0, 0, 5)
        sizer.Add(sizertool, 1, wx.EXPAND, 5 )
        
        self.line_color = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        #self.line_color.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        sizer.Add(self.line_color, 0, wx.EXPAND |wx.ALL, 0 )
        
        sizersta = wx.BoxSizer( wx.HORIZONTAL )
        self.txt_info = wx.StaticText( self, wx.ID_ANY, u"ImagePy  v0.1", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txt_info.Wrap( -1 )
        self.txt_info.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
        sizersta.Add( self.txt_info, 1, wx.ALIGN_BOTTOM|wx.BOTTOM|wx.LEFT|wx.RIGHT, 3 )
        self.pro_bar = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 100,15 ), wx.GA_HORIZONTAL )
        sizersta.Add( self.pro_bar, 0, wx.ALIGN_BOTTOM|wx.BOTTOM|wx.LEFT|wx.RIGHT, 3 )
        sizer.Add(sizersta, 0, wx.EXPAND, 5 )        
        self.SetSizer( sizer )
        
        self.Centre( wx.BOTH )
        self.Fit()
        self.update = False
        
    def set_info(self, value):
        self.txt_info.SetLabel(value)
        
    def set_progress(self, value):
        self.pro_bar.SetValue(value)
        self.pro_bar.Update()
        
    def set_color(self, value):
        self.line_color.SetBackgroundColour(value)
        
    def __del__( self ):
        pass
		
if __name__ == '__main__':
    app = wx.App(False)
    mainFrame = ImagePy(None)
    mainFrame.Show()
    app.MainLoop()
