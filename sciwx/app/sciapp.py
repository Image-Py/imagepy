import wx, os, sys
import time, threading

import wx.lib.agw.aui as aui
from sciwx.widgets import MenuBar, ToolBar, ChoiceBook, ParaDialog
from sciwx.canvas import CanvasNoteBook
from sciwx.grid import GridNoteBook
from sciwx.text import MDNoteFrame, TextNoteFrame
from skimage.data import camera
from sciapp import App

class SciApp(wx.Frame, App):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = 'SciApp', 
                            size = wx.Size(-1,-1), pos = wx.DefaultPosition, 
                            style = wx.RESIZE_BORDER|wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        App.__init__(self)
        self.auimgr = aui.AuiManager()
        self.auimgr.SetManagedWindow( self )
        self.SetSizeHints( wx.Size(1024,768) )
        
        self.init_menu()
        self.init_tool()
        self.init_canvas()
        self.init_table()
        self.init_widgets()
        self.init_text()
        self.init_status()

        self.Layout()
        self.auimgr.Update()
        self.Fit()
        self.Centre( wx.BOTH )

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(aui.EVT_AUI_PANE_CLOSE, self.on_pan_close)

    def init_status(self):
        self.stapanel = stapanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizersta = wx.BoxSizer( wx.HORIZONTAL )
        self.txt_info = wx.StaticText( stapanel, wx.ID_ANY, "ImagePy  v0.2", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txt_info.Wrap( -1 )
        sizersta.Add( self.txt_info, 1, wx.ALIGN_BOTTOM|wx.BOTTOM|wx.LEFT|wx.RIGHT, 2 )
        self.pro_bar = wx.Gauge( stapanel, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 100,15 ), wx.GA_HORIZONTAL )
        sizersta.Add( self.pro_bar, 0, wx.ALIGN_BOTTOM|wx.BOTTOM|wx.LEFT|wx.RIGHT, 2 )
        stapanel.SetSizer(sizersta)
        self.auimgr.AddPane( stapanel,  aui.AuiPaneInfo() .Bottom() .CaptionVisible( False ).PinButton( True )
            .PaneBorder( False ).Dock().Resizable().FloatingSize( wx.DefaultSize ).DockFixed( True )
            . MinSize(wx.Size(-1, 20)). MaxSize(wx.Size(-1, 20)).Layer( 10 ) )
        
    def load_menu(self, data):
        self.menubar.load(data)

    def load_tool(self, data, default=None):
        for i, (name, tols) in enumerate(data[1]):
            self.toolbar.add_tools(name, tols, i==0)
        if not default is None: self.toolbar.add_pop('P', default)
        self.toolbar.Layout()

    def load_widget(self, data):
        self.widgets.load(data)
        
    def init_menu(self):
        self.menubar = MenuBar(self)
        
    def init_tool(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.toolbar = ToolBar(self, True)
        self.toolbar.Fit()

        self.auimgr.AddPane(self.toolbar, aui.AuiPaneInfo() .Left()  .PinButton( True )
            .CaptionVisible( True ).Dock().Resizable().FloatingSize( wx.DefaultSize ).MaxSize(wx.Size( 32,-1 ))
            . BottomDockable( True ).TopDockable( False ).Layer( 10 ) )
        
    def init_canvas(self):
        self.canvasnbwrap = wx.Panel(self)
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.canvasnb = CanvasNoteBook( self.canvasnbwrap)
        sizer.Add( self.canvasnb, 1, wx.EXPAND |wx.ALL, 0 )
        self.canvasnbwrap.SetSizer( sizer )
        self.canvasnbwrap.Layout()
        self.auimgr.AddPane( self.canvasnbwrap, aui.AuiPaneInfo() .Center() .CaptionVisible( False ).PinButton( True ).Dock()
            .PaneBorder( False ).Resizable().FloatingSize( wx.DefaultSize ). BottomDockable( True ).TopDockable( False )
            .LeftDockable( True ).RightDockable( True ) )
        self.canvasnb.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_new_img)
        self.canvasnb.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close_img)

    def init_table(self):
        self.tablenbwrap = wx.Panel(self)
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.tablenb = GridNoteBook( self.tablenbwrap)
        sizer.Add( self.tablenb, 1, wx.EXPAND |wx.ALL, 0 )
        self.tablenbwrap.SetSizer( sizer )
        self.tablenbwrap.Layout()

        self.auimgr.AddPane( self.tablenbwrap, aui.AuiPaneInfo() .Bottom() .CaptionVisible( True ).PinButton( True ).Dock().Hide()
            .MaximizeButton( True ).Resizable().FloatingSize((800, 600)).BestSize(( 120,120 )). Caption('Tables') . 
            BottomDockable( True ).TopDockable( False ).LeftDockable( True ).RightDockable( True ) )

    def init_widgets(self):
        self.widgets = ChoiceBook(self)
        self.auimgr.AddPane( self.widgets, aui.AuiPaneInfo() .Right().Caption('Widgets') .PinButton( True )
            .Dock().Resizable().FloatingSize( wx.DefaultSize ).MinSize( wx.Size( 266,-1 ) ).Layer( 10 ) )

    def init_text(self):
        self.mdframe = MDNoteFrame(self, 'Sci Document')
        self.txtframe = TextNoteFrame(self, 'Sci Text')

    def on_pan_close(self, event):
        if event.GetPane().window in [self.toolbar, self.widgets]:
            event.Veto()
        if hasattr(event.GetPane().window, 'close'):
            event.GetPane().window.close()

    def on_new_img(self, event):
        self.add_img_win(self.canvasnb.canvas())
        self.add_img(self.canvasnb.canvas().image)

    def on_close_img(self, event):
        canvas = event.GetEventObject().GetPage(event.GetSelection())
        self.remove_img_win(canvas)
        self.remove_img(canvas.image)
        
    def info(self, value):
        wx.CallAfter(self.txt_info.SetLabel, value)

    def set_progress(self, value):
        v = max(min(value, 100), 0)
        self.pro_bar.SetValue(v)
        if value==-1:
            self.pro_bar.Hide()
        elif not self.pro_bar.IsShown():
            self.pro_bar.Show()
            self.stapanel.GetSizer().Layout()
        self.pro_bar.Update()

    def on_close(self, event):
        print('close')
        #ConfigManager.write()
        self.auimgr.UnInit()
        del self.auimgr
        self.Destroy()
        sys.exit()

    def show_img(self, img):
        canvas = self.canvasnb.add_canvas()
        canvas.set_img(img)
        self.add_img_win(canvas)
        self.add_img(canvas.image)

    def show_tab(self, tab):
        import pandas as pd
        grid = self.tablenb.add_grid()
        grid.set_data(pd.DataFrame([[1,1],[2,2]]))
        info = self.auimgr.GetPane(self.tablenbwrap)
        info.Show(True)
        self.auimgr.Update()

    def show_md(self, cont, title='Document'):
        page = self.mdframe.add_page()
        page.set_cont(cont)
        self.mdframe.Show()
        
    def show_txt(self, cont, title='Text'):
        page = self.txtframe.add_notepad()
        page.append(cont)
        self.txtframe.Show()

    def alert(self, info, title='SciWx'):
        dialog=wx.MessageDialog(self, info, title, wx.OK)
        dialog.ShowModal() == wx.ID_OK
        dialog.Destroy()

    def getpath(self, title, filt, io, name=''):
        filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in filt])
        dic = {'open':wx.FD_OPEN, 'save':wx.FD_SAVE}
        dialog = wx.FileDialog(self, title, '', name, filt, dic[io])
        rst = dialog.ShowModal()
        path = dialog.GetPath() if rst == wx.ID_OK else None
        dialog.Destroy()
        return path

    def show_para(self, title, view, para, on_handle, on_ok=None, on_cancel=None, preview=False, modal=True):
        dialog = ParaDialog(self, title)
        dialog.init_view(view, para, preview, modal=True)
        dialog.Bind('cancel', on_cancel)
        dialog.Bind('parameter', on_handle)
        return dialog.show()

class P:
    def __init__(self, name):
        self.name = name

    def start(self):
        print(self.name)

    def __call__(self):
        return self
        
data = ('menu', [
        ('File', [('Open', P('O')),
                  '-',
                  ('Close', P('C'))]),
        ('Edit', [('Copy', P('C')),
                  ('A', [('B', P('B')),
                         ('C', P('C'))]),
                  ('Paste', P('P'))])])

if __name__ == '__main__':
    app = wx.App(False)
    frame = SciApp(None)
    frame.Show()
    frame.show_img(None)
    frame.show_img(None)
    frame.show_tab(None)
    '''
    frame.show_md('abcdefg', 'md')
    frame.show_md('ddddddd', 'md')
    frame.show_txt('abcdefg', 'txt')
    frame.show_txt('ddddddd', 'txt')
    '''
    app.MainLoop()
