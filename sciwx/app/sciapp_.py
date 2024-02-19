import wx, os, sys
import time, threading
sys.path.append('../../')
import wx.lib.agw.aui as aui
from sciwx.widgets import MenuBar, ToolBar, RibbonBar, ParaDialog
from sciwx.canvas import CanvasNoteBook
from sciwx.grid import GridNoteBook
from sciwx.widgets import ProgressBar
from sciwx.mesh import Canvas3DFrame
from sciwx.text import MDFrame, TextFrame
from sciwx.plot import PlotFrame
from sciapp.object import Image, Table
from sciapp import App, Source

from sciapp.action.plugin.filters import Gaussian
from sciapp.action.plugin.generalio import OpenFile, SaveImage

class SciApp(wx.Frame, App):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = 'ImagePy', 
                            size = wx.Size(800,600), pos = wx.DefaultPosition, 
                            style = wx.RESIZE_BORDER|wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        App.__init__(self)
        self.auimgr = aui.AuiManager()
        self.auimgr.SetManagedWindow( self )
        self.SetSizeHints( wx.Size(800, 600) )

        self.init_menu()
        self.init_canvas()
        self.init_table()
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
        #self.pro_bar = wx.Gauge( stapanel, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 100,15 ), wx.GA_HORIZONTAL )
        self.pro_bar = ProgressBar(stapanel)
        sizersta.Add( self.pro_bar, 0, wx.ALL, 2 )
        stapanel.SetSizer(sizersta)
        class OpenDrop(wx.FileDropTarget):
            def __init__(self, app): 
                wx.FileDropTarget.__init__(self)
                self.app = app
            def OnDropFiles(self, x, y, path):
                self.app.run_macros(["Open>{'path':'%s'}"%i.replace('\\', '/') for i in path])
        stapanel.SetDropTarget(OpenDrop(self))
        self.auimgr.AddPane( stapanel,  aui.AuiPaneInfo() .Bottom() .CaptionVisible( False ).PinButton( True )
            .PaneBorder( False ).Dock().Resizable().FloatingSize( wx.DefaultSize ).DockFixed( True )
            . MinSize(wx.Size(-1, 20)). MaxSize(wx.Size(-1, 20)).Layer( 10 ) )
        
    def init_menu(self):
        self.menubar = MenuBar(self)

    def init_menu(self):
        self.menubar = RibbonBar(self)
        self.auimgr.AddPane( self.menubar, aui.AuiPaneInfo() .CaptionVisible(False) .Top() .PinButton( True ).Dock().Resizable().FloatingSize( wx.DefaultSize ).Layer(5) )
        

    def load_menu(self, data):
        self.menubar.load(data, {})
        
    def init_canvas(self):
        self.canvasnbwrap = wx.Panel(self)
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.canvasnb = CanvasNoteBook(self.canvasnbwrap)

        sizer.Add( self.canvasnb, 1, wx.EXPAND |wx.ALL, 0 )
        self.canvasnbwrap.SetSizer( sizer )
        self.canvasnbwrap.Layout()
        self.auimgr.AddPane( self.canvasnbwrap, aui.AuiPaneInfo() .Center() .CaptionVisible( False ).PinButton( True ).Dock()
            .PaneBorder( False ).Resizable().FloatingSize( wx.DefaultSize ). BottomDockable( True ).TopDockable( False )
            .LeftDockable( True ).RightDockable( True ) )
        self.canvasnb.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_active_img)
        self.canvasnb.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close_img)

    def init_table(self):
        self.tablenbwrap = wx.Panel(self)
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.tablenb = GridNoteBook( self.tablenbwrap)
        sizer.Add( self.tablenb, 1, wx.EXPAND |wx.ALL, 0 )
        self.tablenbwrap.SetSizer( sizer )
        self.tablenbwrap.Layout()
        
        self.auimgr.AddPane( self.tablenbwrap, aui.AuiPaneInfo() .Bottom() .CaptionVisible( True ).PinButton( True ).Dock().Hide()
            .MaximizeButton( True ).Resizable().FloatingSize((800, 600)).BestSize(( 120,120 )). Caption('Table') . 
            BottomDockable( True ).TopDockable( False ).LeftDockable( True ).RightDockable( True ) )
        self.tablenb.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_active_table)
        self.tablenb.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close_table)

    def init_tool(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.toolbar = ToolBar(self, False)
        self.toolbar.Fit()

        self.auimgr.AddPane(self.toolbar, aui.AuiPaneInfo() .Top()  .PinButton( True ).PaneBorder( False )
            .CaptionVisible( False ).Dock().FloatingSize( wx.DefaultSize ).MinSize(wx.Size( -1,34 )).DockFixed( True )
            . BottomDockable( False ).TopDockable( False ).Layer( 10 ) )

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

    def init_text(self): return
        #self.mdframe = MDNoteFrame(self, 'Sci Document')
        #self.txtframe = TextNoteFrame(self, 'Sci Text')

    def on_pan_close(self, event):
        if event.GetPane().window in [self.toolbar, self.widgets]:
            event.Veto()
        if hasattr(event.GetPane().window, 'close'):
            event.GetPane().window.close()

    def on_new_img(self, event):
        self.add_img(self.canvasnb.canvas().image)
        self.add_img_win(self.canvasnb.canvas())

    def on_active_img(self, event):
        self.active_img(self.canvasnb.canvas().image.name)
        #self.add_img_win(self.canvasnb.canvas())

    def on_close_img(self, event):
        canvas = event.GetEventObject().GetPage(event.GetSelection())
        self.remove_img_win(canvas)
        self.remove_img(canvas.image)

    def on_new_tab(self, event):
        self.add_tab(event.GetEventObject().grid.table)
        self.add_tab_win(event.GetEventObject().grid)

    def on_active_table(self, event):
        self.active_table(self.tablenb.grid().table.title)

    def on_close_table(self, event):
        grid = event.GetEventObject().GetPage(event.GetSelection())
        App.close_table(self, grid.table.title)
        
    def on_new_mesh(self, event):
        self.add_mesh(event.GetEventObject().canvas.mesh)
        self.add_mesh_win(event.GetEventObject().canvas)

    def on_close_mesh(self, event):
        self.remove_mesh(event.GetEventObject().canvas.mesh)
        self.remove_mesh_win(event.GetEventObject().canvas)
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
        print(img)
        canvas = self.canvasnb.add_canvas()
        if not isinstance(img, Image): 
            img = Image(img, title)
        App.show_img(self, img, img.title)
        canvas.set_img(img)

    def show_img(self, img, title=None):
        wx.CallAfter(self._show_img, img, title)

    def _show_table(self, tab, title):
        grid = self.tablenb.add_grid()
        if not isinstance(tab, Table): 
            tab = Table(tab, title)
        App.show_table(self, tab, tab.title)
        grid.set_data(tab)
        info = self.auimgr.GetPane(self.tablenbwrap)
        info.Show(True)
        self.auimgr.Update()

    def show_table(self, tab, title=None):
        wx.CallAfter(self._show_table, tab, title)

    def show_plot(self, title):
        fig = PlotFrame(self)
        fig.figure.title = title
        return fig

    def _show_md(self, cont, title='ImagePy'):
        mdframe = MDFrame(self)
        mdframe.set_cont(cont)
        mdframe.mdpad.title = title
        mdframe.Show(True)

    def show_md(self, cont, title='ImagePy'):
        wx.CallAfter(self._show_md, cont, title)
        
    def _show_workflow(self, cont, title='ImagePy'):
        pan = WorkFlowPanel(self)
        pan.SetValue(cont)
        info = aui.AuiPaneInfo(). DestroyOnClose(True). Left(). Caption(title)  .PinButton( True ) \
            .Resizable().FloatingSize( wx.DefaultSize ).Dockable(False).Float().Top().Layer( 5 ) 
        pan.Bind(None, lambda x:self.run_macros(['%s>None'%x]))
        self.auimgr.AddPane(pan, info)
        self.auimgr.Update()

    def show_workflow(self, cont, title='ImagePy'):
        wx.CallAfter(self._show_workflow, cont, title)

    def _show_txt(self, cont, title='ImagePy'):
        TextFrame(self, title, cont).Show()

    def show_txt(self, cont, title='ImagePy'):
        wx.CallAfter(self._show_txt, cont, title)

    def _show_mesh(self, mesh=None, title=None):
        if mesh is None:
            cframe = Canvas3DFrame(self)
            canvas = cframe.canvas
            canvas.mesh.name = 'Surface'

        elif hasattr(mesh, 'vts'):
            canvas = self.get_mesh_win()
            if canvas is None:
                cframe = Canvas3DFrame(self)
                canvas = cframe.canvas
                canvas.mesh.name = 'Surface'
            canvas.add_surf(title, mesh)
        else:
            cframe = Canvas3DFrame(self)
            canvas = cframe.canvas
            canvas.set_mesh(mesh)
        canvas.GetParent().Show()
        canvas.GetParent().Bind(wx.EVT_ACTIVATE, self.on_new_mesh)
        canvas.GetParent().Bind(wx.EVT_CLOSE, self.on_close_mesh)
        self.add_mesh(canvas.mesh)
        self.add_mesh_win(canvas)

    def show_mesh(self, mesh=None, title=None):
        wx.CallAfter(self._show_mesh, mesh, title)

    def show_widget(self, panel, title='Widgets'):
        obj = self.manager('widget').get(panel.title)
        if obj is None:
            pan = panel(self)
            self.manager('widget').add(obj=pan, name=panel.title)
            self.auimgr.AddPane(pan, aui.AuiPaneInfo().Caption(panel.title).Left().Layer( 15 ).PinButton( True )
                .Float().Resizable().FloatingSize( wx.DefaultSize ).Dockable(True)) #.DestroyOnClose())
        else: 
            info = self.auimgr.GetPane(obj)
            info.Show(True)
        self.Layout()
        self.auimgr.Update()

    def close_img(self, name=None):
        names = self.img_names() if name is None else [name]
        for name in names:
            idx = self.canvasnb.GetPageIndex(self.get_img_win(name))
            self.remove_img(self.get_img_win(name).image)
            self.remove_img_win(self.get_img_win(name))
            self.canvasnb.DeletePage(idx)

    def close_table(self, name=None):
        names = self.get_tab_name() if name is None else [name]
        for name in names:
            idx = self.tablenb.GetPageIndex(self.get_tab_win(name))
            self.remove_tab(self.get_tab_win(name).table)
            self.remove_tab_win(self.get_tab_win(name))
            self.tablenb.DeletePage(idx)

    def run_macros(self, cmd, callafter=None):
        cmds = [i for i in cmd]
        def one(cmds, after): 
            cmd = cmds.pop(0)
            title, para = cmd.split('>')
            plg = self.app.plugin_manager.get(name=title)()
            after = lambda cmds=cmds: one(cmds, one)
            if len(cmds)==0: after = callafter
            wx.CallAfter(plg.start, self, eval(para), after)
        one(cmds, None)

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

    def show_para(self, title, para, view, on_handle=None, on_ok=None, 
        on_cancel=None, on_help=None, preview=False, modal=True):
        on_help = lambda x=None:self.show_md(x or 'No Document!', title)
        dialog = ParaDialog(self, title)
        dialog.init_view(view, para, preview, modal=modal, app=self)
        dialog.Bind('cancel', on_cancel)
        dialog.Bind('parameter', on_handle)
        dialog.Bind('commit', on_ok)
        dialog.Bind('help', on_help)
        return dialog.show()

if __name__ == '__main__':
    import numpy as np
    import pandas as pd

    app = wx.App(False)
    frame = SciApp(None)
    frame.Show()
    frame.show_img([np.zeros((512, 512), dtype=np.uint8)], 'zeros')
    frame.show_table(pd.DataFrame(np.arange(100).reshape((10,10))), 'title')

    plgs = ('root', [('file', [('IO', [('Open', OpenFile), ('Save', SaveImage)]), ('Gaussian', Gaussian)])])

    frame.load_menu(plgs)

    '''
    frame.show_md('abcdefg', 'md')
    frame.show_md('ddddddd', 'md')
    frame.show_txt('abcdefg', 'txt')
    frame.show_txt('ddddddd', 'txt')
    '''

    app.MainLoop()