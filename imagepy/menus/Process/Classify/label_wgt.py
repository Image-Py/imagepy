from imagepy.ui.widgets import CMapSelCtrl
from imagepy.core.manager import ColorManager, ImageManager, WindowsManager
import numpy as np
import wx

class Plugin ( wx.Panel ):
	title = 'Label Tool'
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size(-1,-1), style = wx.TAB_TRAVERSAL )
		outsizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer = wx.BoxSizer( wx.VERTICAL )
		sizer_color = wx.BoxSizer( wx.HORIZONTAL )
		self.btns = []
		for i in range(16):
			btn = wx.Button( self, wx.ID_ANY, str(i), wx.DefaultPosition, wx.DefaultSize, 0 )
			btn.SetMaxSize( wx.Size( 30,-1 ) )
			self.btns.append(btn)
			sizer_color.Add( btn, 0, wx.ALL, 2 )
		self.spn_num = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 2, 15, 0 )
		self.spn_num.SetMaxSize(wx.Size(45, -1))
		sizer_color.Add( self.spn_num, 0, wx.ALL|wx.EXPAND, 3 )

		sizer.Add(sizer_color, 0, wx.ALL|wx.EXPAND, 0)

		sizer_other = wx.BoxSizer( wx.HORIZONTAL )

		self.cmapsel = CMapSelCtrl(self)
		self.cmapsel.SetItems(ColorManager.luts)
		sizer_other.Add(self.cmapsel, 0, wx.ALL|wx.EXPAND, 3 )

		com_backChoices = [ u"No Background" ]
		self.com_back = wx.ComboBox( self, wx.ID_ANY, u"No Background", wx.DefaultPosition, wx.DefaultSize, com_backChoices, wx.CB_READONLY)
		self.com_back.SetSelection( 0 )
		sizer_other.Add( self.com_back, 1, wx.ALL|wx.EXPAND, 3 )
		
		com_modeChoices = [ u"None", u"Max", u"Min", u"Mask", u"2-8mix", u"4-6mix", u"5-5mix", u"6-4mix", u"8-2mix" ]
		self.com_mode = wx.ComboBox( self, wx.ID_ANY, u"Min", wx.DefaultPosition, wx.DefaultSize, com_modeChoices, wx.CB_READONLY )
		self.com_mode.SetSelection( 0 )
		sizer_other.Add( self.com_mode, 0, wx.ALL|wx.EXPAND, 3 )

		self.chk_hide = wx.CheckBox( self, wx.ID_ANY, u"Hide", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_other.Add( self.chk_hide, 0, wx.ALIGN_CENTER|wx.ALL, 0 )

		sizer.Add(sizer_other, 0, wx.ALL|wx.EXPAND, 0)

		outsizer.AddStretchSpacer(prop=1)
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
		for i in self.btns: i.Bind(wx.EVT_BUTTON, self.on_color)

	def on_color(self, event):
		ColorManager.set_front(self.btns.index(event.GetEventObject()))

	def on_items(self, event):
		items = ['No Background Image']+ImageManager.get_titles()
		self.com_back.SetItems(items)
		if self.com_back.GetValue() in items:
			self.com_back.Select(items.index(self.com_back.GetValue()))
		else: self.com_back.Select(0)

	def on_cmapsel(self, event):
		key = self.cmapsel.GetValue()
		lut = ColorManager.get_lut(key)
		n = self.spn_num.GetValue()+1
		idx = np.linspace(0, 255, n).astype(int)
		cs = list(lut[idx]) + [(128,128,128)]*(16-n)
		for btn, c in zip(self.btns, cs):
			btn.SetBackgroundColour(c)

		ips = ImageManager.get()
		if ips is None: return
		newlut = lut*0
		newlut[:n] = lut[idx]
		ips.lut = newlut
		ips.update()

	def on_setback(self, event):
		name = self.com_back.GetValue()
		if name is None: return
		curwin = WindowsManager.get()
		curwin.set_back(ImageManager.get(name))
		curwin.ips.update()

	def on_mode(self, event):
		ips = ImageManager.get()
		if ips is None: return
		if self.chk_hide.GetValue():  
			ips.chan_mode = 0.0
			return ips.update()
		modes = ['set', 'max', 'min', 'msk', 0.2, 0.4, 0.5, 0.6, 0.8]
		ips.chan_mode = modes[self.com_mode.GetSelection()]
		ips.update()

	def __del__( self ):
		pass
	