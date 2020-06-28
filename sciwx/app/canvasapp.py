import wx, wx.lib.agw.aui as aui
from ..canvas.mcanvas import MCanvas
from ..widgets import ToolBar, MenuBar, ParaDialog
from sciapp import App

class CanvasApp(wx.Frame, App):
    def __init__(self, parent=None, autofit=False):
        App.__init__(self)
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
                            title = 'CanvasFrame',
                            pos = wx.DefaultPosition,
                            size = wx.Size( 800, 600 ),
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.canvas = MCanvas(self, autofit=autofit)
        sizer.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 0)
        self.SetSizer(sizer)

        self.set_rg = self.canvas.set_rg
        self.set_lut = self.canvas.set_rg
        self.set_log = self.canvas.set_log
        self.set_mode = self.canvas.set_mode
        self.set_tool = self.canvas.set_tool
        self.set_cn = self.canvas.set_cn

        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Bind(wx.EVT_ACTIVATE, self.on_valid)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.status = self.CreateStatusBar( 1 )

    def set_imgs(self, imgs):
        self.remove_img(self.canvas.image)
        self.canvas.set_imgs(imgs)
        self.add_img(self.canvas.image)

    def set_img(self, img, b=False):
        self.remove_img(self.canvas.image)
        self.canvas.set_img(img, b)
        self.add_img(self.canvas.image)

    def on_idle(self, event):
        if self.GetTitle()!=self.canvas.image.title:
            self.SetTitle(self.canvas.image.title)

    def set_title(self, ips): self.SetTitle(ips.title)

    def info(self, info): self.status.SetStatusText(info)

    def on_valid(self, event): pass

    def on_close(self, event): 
        event.Skip()

    def add_toolbar(self):
        toolbar = ToolBar(self)
        self.GetSizer().Insert(0, toolbar, 0, wx.EXPAND | wx.ALL, 0)
        return toolbar

    def add_menubar(self):
        menubar = MenuBar(self)
        self.SetMenuBar(menubar)
        return menubar

    def show_para(self, title, view, para, on_handle=None, on_ok=None, on_cancel=None, preview=False, modal=True):
        dialog = ParaDialog(self, title)
        dialog.init_view(view, para, preview, modal=modal, app=self)
        dialog.Bind('cancel', on_cancel)
        dialog.Bind('parameter', on_handle)
        dialog.Bind('commit', on_ok)
        return dialog.show()