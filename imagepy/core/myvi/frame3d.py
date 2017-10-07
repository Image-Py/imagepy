import wx, os
from .canvas3d import Canvas3D
from wx.lib.pubsub import pub
from . import util
import numpy as np
import os.path as osp

class GLFrame(wx.Frame):
	frm = None

	@classmethod
	def get_frame(cls, parent, title):
		if cls.frm == None:
			cls.frm = GLFrame(parent, title)
			cls.frm.Show()
		wx.Yield()
		return cls.frm

	def __init__( self, parent, title=''):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = title, pos = wx.DefaultPosition, size = wx.Size( 800, 600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		sizer = wx.BoxSizer( wx.VERTICAL )
		self.canvas = Canvas3D(self)
		self.toolbar = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
		tsizer = wx.BoxSizer( wx.HORIZONTAL )

		root = osp.abspath(osp.dirname(__file__))

		self.SetIcon(wx.Icon('data/logo.ico', wx.BITMAP_TYPE_ICO))

		self.btn_x = wx.BitmapButton( self.toolbar, wx.ID_ANY, wx.Bitmap( os.path.join(root, 'imgs/x-axis.png'), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		tsizer.Add( self.btn_x, 0, wx.ALL, 1 )
		self.btn_y = wx.BitmapButton( self.toolbar, wx.ID_ANY, wx.Bitmap( os.path.join(root, 'imgs/y-axis.png'), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		tsizer.Add( self.btn_y, 0, wx.ALL, 1 )
		self.btn_z = wx.BitmapButton( self.toolbar, wx.ID_ANY, wx.Bitmap( os.path.join(root, 'imgs/z-axis.png'), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		tsizer.Add( self.btn_z, 0, wx.ALL, 1 )
		tsizer.Add(wx.StaticLine( self.toolbar, wx.ID_ANY,  wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL), 0, wx.ALL|wx.EXPAND, 2 )
		self.btn_pers = wx.BitmapButton( self.toolbar, wx.ID_ANY, wx.Bitmap( os.path.join(root, 'imgs/isometric.png'), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		tsizer.Add( self.btn_pers, 0, wx.ALL, 1 )
		self.btn_orth = wx.BitmapButton( self.toolbar, wx.ID_ANY, wx.Bitmap( os.path.join(root, 'imgs/parallel.png'), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		tsizer.Add( self.btn_orth, 0, wx.ALL, 1 )
		tsizer.Add(wx.StaticLine( self.toolbar, wx.ID_ANY,  wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL), 0, wx.ALL|wx.EXPAND, 2 )
		self.btn_save = wx.BitmapButton( self.toolbar, wx.ID_ANY, wx.Bitmap(os.path.join(root, 'imgs/save.png'), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		tsizer.Add( self.btn_save, 0, wx.ALL, 1 )
		
		self.btn_color = wx.ColourPickerCtrl( self.toolbar, wx.ID_ANY, wx.Colour( 128, 128, 128 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		tsizer.Add( self.btn_color, 0, wx.ALIGN_CENTER|wx.ALL, 1 )
		self.toolbar.SetSizer( tsizer )

		self.settingbar = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		ssizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self.settingbar, wx.ID_ANY, u"Object:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		ssizer.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.LEFT, 10 )
		
		cho_objChoices = []
		self.cho_obj = wx.Choice( self.settingbar, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_objChoices, 0 )
		self.cho_obj.SetSelection( 0 )
		ssizer.Add( self.cho_obj, 0, wx.ALL, 1 )
		
		self.chk_visible = wx.CheckBox( self.settingbar, wx.ID_ANY, u"visible", wx.DefaultPosition, wx.DefaultSize, 0 )
		ssizer.Add( self.chk_visible, 0, wx.ALIGN_CENTER|wx.LEFT, 10 )
		
		self.col_color = wx.ColourPickerCtrl( self.settingbar, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		ssizer.Add( self.col_color, 0, wx.ALIGN_CENTER|wx.ALL, 1 )
		
		self.m_staticText2 = wx.StaticText( self.settingbar, wx.ID_ANY, u"Blend:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		ssizer.Add( self.m_staticText2, 0, wx.ALIGN_CENTER|wx.LEFT, 10 )
		
		self.sli_blend = wx.Slider( self.settingbar, wx.ID_ANY, 10, 0, 10, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		ssizer.Add( self.sli_blend, 0, wx.ALIGN_CENTER|wx.ALL, 1 )
		self.settingbar.SetSizer(ssizer)

		self.m_staticText2 = wx.StaticText( self.settingbar, wx.ID_ANY, u"Mode:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		ssizer.Add( self.m_staticText2, 0, wx.ALIGN_CENTER|wx.LEFT, 10 )

		cho_objChoices = ['mesh', 'grid']
		self.cho_mode = wx.Choice( self.settingbar, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cho_objChoices, 0 )
		self.cho_mode.SetSelection( 0 )
		ssizer.Add( self.cho_mode, 0, wx.ALL, 1 )

		sizer.Add( self.toolbar, 0, wx.EXPAND |wx.ALL, 0 )
		sizer.Add( self.canvas, 1, wx.EXPAND |wx.ALL, 0)
		sizer.Add( self.settingbar, 0, wx.EXPAND |wx.ALL, 0 )
		
		self.SetSizer( sizer )
		self.Layout()
		self.Centre( wx.BOTH )
		
		self.btn_x.Bind( wx.EVT_BUTTON, self.view_x)
		self.btn_y.Bind( wx.EVT_BUTTON, self.view_y)
		self.btn_z.Bind( wx.EVT_BUTTON, self.view_z)
		self.btn_save.Bind( wx.EVT_BUTTON, self.on_save)
		self.btn_pers.Bind( wx.EVT_BUTTON, lambda evt, f=self.on_pers:f(True))
		self.btn_orth.Bind( wx.EVT_BUTTON, lambda evt, f=self.on_pers:f(False))
		self.btn_color.Bind( wx.EVT_COLOURPICKER_CHANGED, self.on_bgcolor )

		self.cho_obj.Bind( wx.EVT_CHOICE, self.on_select )
		self.cho_mode.Bind( wx.EVT_CHOICE, self.on_mode )
		self.chk_visible.Bind( wx.EVT_CHECKBOX, self.on_visible)
		self.sli_blend.Bind( wx.EVT_SCROLL, self.on_blend )
		self.col_color.Bind( wx.EVT_COLOURPICKER_CHANGED, self.on_color )

		self.Bind(wx.EVT_CLOSE, self.on_closing)
		
		pub.subscribe(self.add_obj, 'add_obj')

	def on_closing(self, event):
		print('closed', '-------------------')
		GLFrame.frm = None
		event.Skip()

	def view_x(self, evt): 
		self.canvas.view_x()

	def view_y(self, evt): 
		self.canvas.view_y()

	def view_z(self, evt): 
		self.canvas.view_z()

	def on_pers(self, b):
		self.canvas.view_pers(b)

	def on_bgcolor(self, event):
		c = tuple(np.array(event.GetColour()[:3])/255)
		self.canvas.set_background(c)
		self.canvas.Refresh(False)

	def on_save(self, evt):
	    dic = {'open':wx.FD_OPEN, 'save':wx.FD_SAVE}
	    filt = 'PNG files (*.png)|*.png'
	    dialog = wx.FileDialog(self, 'Save Picture', '', '', filt, wx.FD_SAVE)
	    rst = dialog.ShowModal()
	    if rst == wx.ID_OK:
	        path = dialog.GetPath()
	        self.canvas.save_bitmap(path)
	        print(path)
	    dialog.Destroy()

	def get_obj(self, name):
		return self.canvas.manager.get_obj(name)

	def on_visible(self, evt):
		self.curobj.set_style(visible=evt.IsChecked())
		self.canvas.Refresh(False)

	def on_blend(self, evt):
		self.curobj.set_style(blend=evt.GetInt()/10.0)
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
		print(color)
		self.col_color.SetColour((tuple(color)))
		self.sli_blend.SetValue(int(self.curobj.blend*10))
		self.cho_mode.SetSelection(['mesh', 'grid'].index(self.curobj.mode))

	def add_obj_ansy(self, name, vts, fs, ns, cs):
		wx.CallAfter(pub.sendMessage, 'add_obj', name=name, vts=vts, fs=fs, ns=ns, cs=cs)

	def add_obj(self, name, vts, fs, ns, cs, **key):
		manager = self.canvas.manager
		manager.add_obj(name, vts, fs, ns, cs)


		self.cho_obj.Append(name)
		self.cho_obj.SetSelection(self.cho_obj.GetCount()-1)
		self.on_select(None)
		self.canvas.manager.count_box()
		self.canvas.manager.reset()
		self.canvas.Refresh(False)

if __name__ == '__main__':
    app = wx.App(False)
    frm = GLFrame(None, title='GLCanvas Sample')
    frm.Show()
    app.MainLoop()