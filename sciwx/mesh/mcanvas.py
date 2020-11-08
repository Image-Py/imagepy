import wx
import os.path as osp
import platform, math
from pubsub import pub
from .canvas import Canvas3D
from sciapp.util import count_ns
import numpy as np
import math

def make_bitmap(bmp):
    img = bmp.ConvertToImage()
    img.Resize((20, 20), (2, 2))
    return img.ConvertToBitmap()

class MCanvas3D(wx.Panel):
    def __init__( self, parent, scene=None):
        wx.Panel.__init__(self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
        #self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.canvas = Canvas3D(self, scene)
        self.toolbar = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        tsizer = wx.BoxSizer( wx.HORIZONTAL )

        root = osp.abspath(osp.dirname(__file__))

        #self.SetIcon(wx.Icon('data/logo.ico', wx.BITMAP_TYPE_ICO))

        self.btn_x = wx.BitmapButton( self.toolbar, wx.ID_ANY, make_bitmap(wx.Bitmap( osp.join(root, 'imgs/x-axis.png'), wx.BITMAP_TYPE_ANY )), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        tsizer.Add( self.btn_x, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
        self.btn_y = wx.BitmapButton( self.toolbar, wx.ID_ANY, make_bitmap(wx.Bitmap( osp.join(root, 'imgs/y-axis.png'), wx.BITMAP_TYPE_ANY )), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        tsizer.Add( self.btn_y, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
        self.btn_z = wx.BitmapButton( self.toolbar, wx.ID_ANY, make_bitmap(wx.Bitmap( osp.join(root, 'imgs/z-axis.png'), wx.BITMAP_TYPE_ANY )), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        tsizer.Add( self.btn_z, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
        tsizer.Add(wx.StaticLine( self.toolbar, wx.ID_ANY,  wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL), 0, wx.ALL|wx.EXPAND, 2 )
        self.btn_pers = wx.BitmapButton( self.toolbar, wx.ID_ANY, make_bitmap(wx.Bitmap( osp.join(root, 'imgs/isometric.png'), wx.BITMAP_TYPE_ANY )), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        tsizer.Add( self.btn_pers, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
        self.btn_orth = wx.BitmapButton( self.toolbar, wx.ID_ANY, make_bitmap(wx.Bitmap( osp.join(root, 'imgs/parallel.png'), wx.BITMAP_TYPE_ANY )), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        tsizer.Add( self.btn_orth, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
        tsizer.Add(wx.StaticLine( self.toolbar, wx.ID_ANY,  wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL), 0, wx.ALL|wx.EXPAND, 2 )
        self.btn_open = wx.BitmapButton( self.toolbar, wx.ID_ANY, make_bitmap(wx.Bitmap(osp.join(root, 'imgs/open.png'), wx.BITMAP_TYPE_ANY )), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        tsizer.Add( self.btn_open, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
        self.btn_stl = wx.BitmapButton( self.toolbar, wx.ID_ANY, make_bitmap(wx.Bitmap(osp.join(root, 'imgs/stl.png'), wx.BITMAP_TYPE_ANY )), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        tsizer.Add( self.btn_stl, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
        #pan = wx.Panel(self.toolbar, size=(50, 50))
        self.btn_color = wx.ColourPickerCtrl( self.toolbar, wx.ID_ANY, wx.Colour( 128, 128, 128 ), wx.DefaultPosition, [(33, 38), (-1, -1)][platform.system() in ['Windows', 'Linux']], wx.CLRP_DEFAULT_STYLE )
        tsizer.Add( self.btn_color, 0, wx.ALL|(0, wx.EXPAND)[platform.system() in ['Windows', 'Linux']], 0 )
        tsizer.Add(wx.StaticLine( self.toolbar, wx.ID_ANY,  wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL), 0, wx.ALL|wx.EXPAND, 2 )
        self.cho_light = wx.Choice( self.toolbar, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ['force light', 'normal light', 'weak light', 'off light'], 0 )
        self.cho_light.SetSelection( 1 )
        tsizer.Add( self.cho_light, 0, wx.ALIGN_CENTER|wx.ALL, 1 )
        self.cho_bg = wx.Choice( self.toolbar, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ['force scatter', 'normal scatter', 'weak scatter', 'off scatter'], 0 )
        self.cho_bg.SetSelection( 1 )
        tsizer.Add( self.cho_bg, 0, wx.ALIGN_CENTER|wx.ALL, 1 )

        self.toolbar.SetSizer( tsizer )
        tsizer.Layout()

        self.settingbar = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        ssizer = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText1 = wx.StaticText( self.settingbar, wx.ID_ANY, u"Object:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        ssizer.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.LEFT, 10 )
        
        cho_objChoices = ['None']
        self.cho_obj = wx.Choice( self.settingbar, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_objChoices, 0 )
        self.cho_obj.SetSelection( 0 )
        ssizer.Add( self.cho_obj, 0, wx.ALIGN_CENTER|wx.ALL, 1 )
        
        self.chk_visible = wx.CheckBox( self.settingbar, wx.ID_ANY, u"visible", wx.DefaultPosition, wx.DefaultSize, 0 )
        ssizer.Add( self.chk_visible, 0, wx.ALIGN_CENTER|wx.LEFT, 10 )
        
        self.col_color = wx.ColourPickerCtrl( self.settingbar, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
        ssizer.Add( self.col_color, 0, wx.ALIGN_CENTER|wx.ALL, 1 )
        
        self.m_staticText2 = wx.StaticText( self.settingbar, wx.ID_ANY, u"Alpha:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        ssizer.Add( self.m_staticText2, 0, wx.ALIGN_CENTER|wx.LEFT, 10 )
        
        self.sli_alpha = wx.Slider( self.settingbar, wx.ID_ANY, 10, 0, 10, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        ssizer.Add( self.sli_alpha, 0, wx.ALIGN_CENTER|wx.ALL, 1 )
        self.settingbar.SetSizer(ssizer)

        self.m_staticText2 = wx.StaticText( self.settingbar, wx.ID_ANY, u"Mode:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        ssizer.Add( self.m_staticText2, 0, wx.ALIGN_CENTER|wx.LEFT, 10 )

        cho_objChoices = ['mesh', 'grid']
        self.cho_mode = wx.Choice( self.settingbar, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_objChoices, 0 )
        self.cho_mode.SetSelection( 0 )
        ssizer.Add( self.cho_mode, 0, wx.ALIGN_CENTER|wx.ALL, 1 )

        sizer.Add( self.toolbar, 0, wx.EXPAND |wx.ALL, 0 )
        sizer.Add( self.canvas, 1, wx.EXPAND |wx.ALL, 0)
        sizer.Add( self.settingbar, 0, wx.EXPAND |wx.ALL, 0 )
        
        self.SetSizer( sizer )
        self.Layout()
        self.Centre( wx.BOTH )
        
        self.view_x = self.canvas.view_x
        self.view_y = self.canvas.view_y
        self.view_z = self.canvas.view_z
        self.set_pers = self.canvas.set_pers
        self.set_background = self.canvas.set_background
        self.set_scatter = self.canvas.set_scatter
        self.set_bright = self.canvas.set_bright

        self.on_bgcolor = lambda e: self.canvas.set_background(np.array(e.GetColour()[:3])/255)
        self.on_bg = lambda e: self.canvas.set_scatter((3-e.GetSelection())/3)
        self.on_light = lambda e: self.canvas.set_bright((3-e.GetSelection())/3)

        self.btn_x.Bind( wx.EVT_BUTTON, self.view_x)
        self.btn_y.Bind( wx.EVT_BUTTON, self.view_y)
        self.btn_z.Bind( wx.EVT_BUTTON, self.view_z)
        self.btn_open.Bind( wx.EVT_BUTTON, self.on_open)
        self.btn_stl.Bind( wx.EVT_BUTTON, self.on_stl)
        self.btn_pers.Bind( wx.EVT_BUTTON, lambda evt, f=self.set_pers:f(True))
        self.btn_orth.Bind( wx.EVT_BUTTON, lambda evt, f=self.set_pers:f(False))
        self.btn_color.Bind( wx.EVT_COLOURPICKER_CHANGED, self.on_bgcolor )

        self.cho_obj.Bind( wx.EVT_CHOICE, self.on_select )
        self.cho_mode.Bind( wx.EVT_CHOICE, self.on_mode )
        self.cho_light.Bind( wx.EVT_CHOICE, self.on_light )
        self.cho_bg.Bind( wx.EVT_CHOICE, self.on_bg )
        self.chk_visible.Bind( wx.EVT_CHECKBOX, self.on_visible)
        self.sli_alpha.Bind( wx.EVT_SCROLL, self.on_alpha )
        self.col_color.Bind( wx.EVT_COLOURPICKER_CHANGED, self.on_color )

        if scene!=None: self.cho_obj.Set(list(scene.objs.keys()))
    
    @property
    def name(self): return self.canvas.scene.meshset.name

    def set_mesh(self, mesh):
        self.canvas.set_mesh(mesh)
        self.cho_obj.Set(list(mesh.objs.keys()))

    @property
    def mesh(self): return self.canvas.scene.meshset

    def on_save(self, evt):
        dic = {'open':wx.FD_OPEN, 'save':wx.FD_SAVE}
        filt = 'PNG files (*.png)|*.png'
        dialog = wx.FileDialog(self, 'Save Picture', '', '', filt, wx.FD_SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            self.canvas.save_bitmap(path)
        dialog.Destroy()

    def on_stl(self, evt):
        filt = 'STL files (*.stl)|*.stl'
        dialog = wx.FileDialog(self, 'Save STL', '', '', filt, wx.FD_SAVE)
        rst = dialog.ShowModal()
        if rst == wx.ID_OK:
            path = dialog.GetPath()
            self.canvas.save_stl(path)
        dialog.Destroy()

    def on_open(self, evt):
        from stl import mesh
        filt = 'STL files (*.stl)|*.stl'
        dialog = wx.FileDialog(self, 'Open STL', '', '', filt, wx.FD_OPEN)
        rst = dialog.ShowModal()
        if rst == wx.ID_OK:
            path = dialog.GetPath()
            cube = mesh.Mesh.from_file(path)
            verts = cube.vectors.reshape((-1,3)).astype(np.float32)
            ids = np.arange(len(verts), dtype=np.uint32).reshape((-1,3))
            norms = count_ns(verts, ids)
            fp, fn = osp.split(path)
            fn, fe = osp.splitext(fn)
            self.add_surf_asyn(fn, verts, ids, norms, (1,1,1))
        dialog.Destroy()

    def get_obj(self, name):
        return self.canvas.scene.meshset.get_obj(name)

    def set_style(self, name, **key):
        self.get_obj(name).set_style(**key)
        self.canvas.Refresh()

    def on_visible(self, evt):
        self.curobj.set_style(visible=evt.IsChecked())
        self.canvas.Refresh(False)

    def on_alpha(self, evt):
        self.curobj.set_style(alpha=evt.GetInt()/10.0)
        self.canvas.Refresh(False)

    def on_mode(self, evt):
        self.curobj.set_style(mode=evt.GetString())
        self.canvas.Refresh(False)

    def on_color(self, evt):
        c = tuple(np.array(evt.GetColour()[:3])/255)
        self.curobj.set_style(color = c)
        self.canvas.Refresh(False)

    def on_select(self, evt):
        n = self.cho_obj.GetSelection()
        self.curobj = self.get_obj(self.cho_obj.GetString(n))
        self.chk_visible.SetValue(self.curobj.visible)
        color = (np.array(self.curobj.color)*255).astype(np.uint8)
        self.col_color.SetColour((tuple(color)))
        self.sli_alpha.SetValue(int(self.curobj.alpha*10))
        self.cho_mode.SetSelection(['mesh', 'grid'].index(self.curobj.mode))

    def add_surf_asyn(self, name, obj):
        self.canvas.add_surf_asyn(name, obj)
        self.cho_obj.Append(name)

    def add_surf(self, name, obj):
        self.canvas.add_surf(name, obj)
        self.cho_obj.Append(name)