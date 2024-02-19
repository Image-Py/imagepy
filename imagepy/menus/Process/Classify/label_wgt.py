from sciwx.widgets import CMapSelCtrl
from imagepy.app import ColorManager
from sciapp.action import Macros
import numpy as np
import wx, os.path as osp

def make_bitmap(bmp):
    img = bmp.ConvertToImage()
    img.Resize((20, 20), (2, 2))
    return img.ConvertToBitmap()

# apply, paint, fill, width, slic
class Plugin ( wx.Panel ):
	title = 'Label Tool'
	def __init__( self, parent, app=None):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size(-1,-1), style = wx.TAB_TRAVERSAL )
		outsizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer = wx.BoxSizer( wx.VERTICAL )
		sizer_color = wx.BoxSizer( wx.HORIZONTAL )
		self.app = app
		self.btns = []
		self.btn_make =  wx.Button( self, wx.ID_ANY, 'New Mark', wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_color.Add(self.btn_make, 0, wx.ALL, 2)
		for i in range(11):
			btn = wx.Button( self, wx.ID_ANY, str(i), wx.DefaultPosition, wx.DefaultSize, 0 )
			btn.SetMaxSize( wx.Size( 30,-1 ) )
			self.btns.append(btn)
			sizer_color.Add( btn, 0, wx.ALL, 2 )
		self.spn_num = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 2, 15, 0 )
		self.spn_num.SetMaxSize(wx.Size(45, -1))
		sizer_color.Add( self.spn_num, 0, wx.ALL|wx.EXPAND, 2 )

		sizer.Add(sizer_color, 0, wx.ALL|wx.EXPAND, 0)

		sizer_other = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_update =  wx.Button( self, wx.ID_ANY, 'Update', wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_other.Add( self.btn_update, 0, wx.ALL, 2)

		self.cmapsel = CMapSelCtrl(self)
		self.cmapsel.SetItems(ColorManager.gets(tag='base'))
		sizer_other.Add(self.cmapsel, 0, wx.ALL|wx.EXPAND, 2 )

		com_backChoices = [ u"No Background" ]
		self.com_back = wx.ComboBox( self, wx.ID_ANY, u"No Background", wx.DefaultPosition, wx.DefaultSize, com_backChoices, wx.CB_READONLY)
		self.com_back.SetSelection( 0 )
		sizer_other.Add( self.com_back, 1, wx.ALL|wx.EXPAND, 2 )
		
		com_modeChoices = [ u"None", u"Max", u"Min", u"Mask", u"2-8mix", u"4-6mix", u"5-5mix", u"6-4mix", u"8-2mix" ]
		self.com_mode = wx.ComboBox( self, wx.ID_ANY, u"Min", wx.DefaultPosition, wx.DefaultSize, com_modeChoices, wx.CB_READONLY )
		self.com_mode.SetSelection( 0 )
		sizer_other.Add( self.com_mode, 0, wx.ALL|wx.EXPAND, 2 )

		self.chk_hide = wx.CheckBox( self, wx.ID_ANY, u"Hide", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_other.Add( self.chk_hide, 0, wx.ALIGN_CENTER|wx.ALL, 0 )

		sizer.Add(sizer_other, 0, wx.ALL|wx.EXPAND, 0)

		#sizer_tol = wx.GridSizer( 0, 3, 0, 0 )
		self.pens = []
		name = ['01.gif','03.gif','05.gif','10.gif','fill.gif']
		path = osp.abspath(osp.dirname(__file__))
		for i in (0,1,2,3,4):
			pen = wx.BitmapButton(self, wx.ID_ANY, make_bitmap(wx.Bitmap(osp.join(path, 'imgs', name[i]))),#make_bitmap(wx.Bitmap(data[1])), 
            wx.DefaultPosition, (30, 30), wx.BU_AUTODRAW|wx.RAISED_BORDER ) 
            #wx.Button( self, wx.ID_ANY, str(i), wx.DefaultPosition, wx.DefaultSize, 0 )
			pen.SetMaxSize( wx.Size( 30,-1 ) )
			self.pens.append( pen )
			sizer_color.Add( pen, 0, wx.ALL, 2 )

		outsizer.AddStretchSpacer(prop=1)
		#outsizer.Add(sizer_tol, 0, wx.ALL, 0)
		outsizer.Add(sizer, 0, wx.ALL, 0)
		outsizer.AddStretchSpacer(prop=1)

		self.SetSizer( outsizer )
		self.Layout()
		
		# Connect Events
		self.spn_num.Bind( wx.EVT_SPINCTRL, self.on_cmapsel )
		self.com_back.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.on_items )
		self.cmapsel.Bind(wx.EVT_COMBOBOX,  self.on_cmapsel)
		self.com_back.Bind( wx.EVT_COMBOBOX, self.on_setback)
		self.com_mode.Bind( wx.EVT_COMBOBOX, self.on_mode)
		self.chk_hide.Bind( wx.EVT_CHECKBOX, self.on_mode)
		self.pens[-1].Bind( wx.EVT_BUTTON, self.on_fill)
		for i in self.btns: i.Bind(wx.EVT_BUTTON, self.on_color)
		for i in range(4): self.pens[i].Bind(wx.EVT_BUTTON, \
			lambda e, x=(1,3,5,10)[i]: self.on_pen(x))
		self.btn_make.Bind( wx.EVT_BUTTON, self.on_make)

	def on_make(self, event):
		Macros(None, ['Build Mark Image>None']).start(self.app)

	def on_fill(self, event):
		tol = self.app.get_plugin('Flood Fill')()
		tol.para['tor'] = 0
		tol.start(self.app)

	def on_pen(self, width):
		tol = self.app.get_plugin('Pencil')()
		tol.para['width'] = width
		tol.start(self.app)

	def on_color(self, event):
		self.app.manager('color').add('front', self.btns.index(event.GetEventObject()))

	def on_items(self, event):
		items = ['No Background Image']+self.app.img_names()
		self.com_back.SetItems(items)
		if self.com_back.GetValue() in items:
			self.com_back.Select(items.index(self.com_back.GetValue()))
		else: self.com_back.Select(0)

	def on_cmapsel(self, event):
		key = self.cmapsel.GetValue()
		lut = ColorManager.get(key)
		n = self.spn_num.GetValue()+1
		idx = np.linspace(0, 255, n).astype(int)
		self.cs = list(lut[idx]) + [(128,128,128)]*(16-n)
		for btn, c in zip(self.btns, self.cs):
			btn.SetBackgroundColour(c)

		ips = self.app.get_img()
		if ips is None: return
		newlut = lut*0
		newlut[:n] = lut[idx]
		ips.lut = newlut
		ips.update()

	def on_setback(self, event):
		name = self.com_back.GetValue()
		if name is None: return
		self.app.get_img().back = self.app.get_img(name)
		#curwin = WindowsManager.get()
		#curwin.set_back(ImageManager.get(name))
		self.app.get_img().update()

	def on_mode(self, event):
		ips = self.app.get_img()
		if ips is None: return
		if self.chk_hide.GetValue():  
			ips.mode = 0.0
			return ips.update()
		modes = ['set', 'max', 'min', 'msk', 0.2, 0.4, 0.5, 0.6, 0.8]
		ips.mode = modes[self.com_mode.GetSelection()]
		ips.update()

	def __del__( self ):
		pass
	