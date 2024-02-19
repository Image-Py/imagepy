import wx, os, sys
import time, threading
sys.path.append('../../')
import wx.lib.agw.aui as aui
from sciwx.widgets import MenuBar, ToolBar, ParaDialog
from sciwx.canvas import CanvasNoteBook
from sciwx.widgets import ProgressBar
from sciwx.grid import GridFrame
from sciwx.mesh import Canvas3DFrame
from sciwx.text import MDFrame, TextFrame
from sciwx.plot import PlotFrame
from sciapp import App, Source
from sciapp.object import Image, Table

class ImageApp(wx.Frame, App):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = 'ImageApp', 
                            size = wx.Size(800,600), pos = wx.DefaultPosition, 
                            style = wx.RESIZE_BORDER|wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        App.__init__(self)
        self.SetSizeHints( wx.Size(600,-1) )

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.toolbar = ToolBar(self)
        self.toolbar.Fit()
        sizer.Add(self.toolbar, 0, wx.EXPAND |wx.ALL, 0)

        self.canvasnb = CanvasNoteBook(self)
        self.canvasnb.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_active_img)
        self.canvasnb.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close_img)
        sizer.Add(self.canvasnb, 1, wx.EXPAND |wx.ALL, 0)

        self.stapanel = stapanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizersta = wx.BoxSizer( wx.HORIZONTAL )
        self.txt_info = wx.StaticText( stapanel, wx.ID_ANY, "ImageApp", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizersta.Add( self.txt_info, 1, wx.ALIGN_BOTTOM|wx.BOTTOM|wx.LEFT|wx.RIGHT, 2 )
        self.pro_bar = ProgressBar(stapanel)
        sizersta.Add( self.pro_bar, 0, wx.ALL, 2 )
        stapanel.SetSizer(sizersta)
        sizer.Add(self.stapanel, 0, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(sizer)
        self.Layout()
        self.Centre( wx.BOTH )
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
    def record_macros(self, x): print(x)
    
    def add_task(self, task):
        self.task_manager.add(task.title, task)
        tasks = self.task_manager.gets()
        tasks = [(p.title, lambda t=p:p.prgs) for n,p,t in tasks]
        self.pro_bar.SetValue(tasks)

    def remove_task(self, task):
        self.task_manager.remove(obj=task)
        tasks = self.task_manager.gets()
        tasks = [(p.title, lambda t=p:p.prgs) for n,p,t in tasks]
        self.pro_bar.SetValue(tasks)

    def on_active_img(self, event):
        self.active_img(self.canvasnb.canvas().image.name)
        # self.add_img_win(self.canvasnb.canvas())

    def on_close_img(self, event):
        canvas = event.GetEventObject().GetPage(event.GetSelection())
        App.close_img(self, canvas.image.title)

    def on_new_tab(self, event):
        self.add_tab(event.GetEventObject().grid.table)
        self.add_tab_win(event.GetEventObject().grid)

    def on_close_tab(self, event):
        self.remove_tab_win(event.GetEventObject().grid)
        self.remove_tab(event.GetEventObject().grid.table)
        event.Skip()
        
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
        self.Destroy()
        sys.exit()

    def _show_img(self, img, title=None):
        canvas = self.canvasnb.add_canvas()
        if not isinstance(img, Image): 
            img = Image(img, title)
        App.show_img(self, img, img.title)
        canvas.set_img(img)

    def show_img(self, img, title=None):
        wx.CallAfter(self._show_img, img, title)

    def _show_table(self, tab, title):
        cframe = GridFrame(self)
        grid = cframe.grid
        grid.set_data(tab)
        if not title is None:
            grid.table.name = title
        cframe.Bind(wx.EVT_ACTIVATE, self.on_new_tab)
        cframe.Bind(wx.EVT_CLOSE, self.on_close_tab)
        cframe.Show()

    def show_table(self, tab, title=None):
        wx.CallAfter(self._show_table, tab, title)

    def show(self, tag, cont, title):
        tag = tag or 'img'
        if tag=='img':
            self.show_img([cont], title)
        elif tag=='imgs':
            self.show_img(cont, title)
        elif tag=='tab':
            self.show_table(cont, title)
        elif tag=='mc':
            self.run_macros(cont)
        elif tag=='md':
            self.show_md(cont, title)
        elif tag=='wf':
            self.show_workflow(cont, title)
        else: self.alert('no view for %s!'%tag)

    def info(self, cont): 
        wx.CallAfter(self.txt_info.SetLabel, cont)

    def _alert(self, info, title='ImagePy'):
        dialog=wx.MessageDialog(self, info, title, wx.OK)
        dialog.ShowModal() == wx.ID_OK
        dialog.Destroy()

    def alert(self, info, title='ImagePy'):
        wx.CallAfter(self._alert, info, title)

    def yes_no(self, info, title='ImagePy'):
        dialog = wx.MessageDialog(self, info, title, wx.YES_NO | wx.CANCEL)
        rst = dialog.ShowModal()
        dialog.Destroy()
        dic = {wx.ID_YES:'yes', wx.ID_NO:'no', wx.ID_CANCEL:'cancel'}
        return dic[rst]

    def get_path(self, title, filt, io, name=''):
        filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in filt])
        dic = {'open':wx.FD_OPEN, 'save':wx.FD_SAVE}
        dialog = wx.FileDialog(self, title, '', name, filt, dic[io])
        rst = dialog.ShowModal()
        path = dialog.GetPath() if rst == wx.ID_OK else None
        dialog.Destroy()
        return path

    def show_para(self, title, para, view, on_handle=None, on_ok=None, on_cancel=None, preview=False, modal=True):
        dialog = ParaDialog(self, title)
        dialog.init_view(view, para, preview, modal=modal, app=self)
        dialog.Bind('cancel', on_cancel)
        dialog.Bind('parameter', on_handle)
        dialog.Bind('commit', on_ok)
        return dialog.show()

    def start(imgs=[], plgs=[]):
        app = wx.App(False)
        frame = ImageApp(None)
        for name, i in imgs: frame.show_img([i], name)
        for name, i in plgs: frame.toolbar.add_tool(name, i)
        frame.Show()
        app.MainLoop()

if __name__ == '__main__':
    from skimage.data import camera
    from sciwx.plugins.filters import Gaussian

    ImageApp.start(
        imgs = [('camera', camera())], 
        plgs=[('G', Gaussian), ('T', Gaussian)])