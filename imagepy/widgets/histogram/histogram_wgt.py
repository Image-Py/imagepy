from ...ui.widgets import HistCanvas, CMapPanel, CMapSelPanel
from  imagepy.core.manager import ColorManager
from imagepy import IPy
import numpy as np
import wx

class Plugin( wx.Panel ):
	title = 'Histogram'
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 255,0 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.histpan = HistCanvas(self)
		bSizer1.Add(self.histpan, 0, wx.ALL|wx.EXPAND, 5 )

		self.sli_high = wx.Slider( self, wx.ID_ANY, 255, 0, 255, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_LABELS )
		bSizer1.Add( self.sli_high, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.sli_low = wx.Slider( self, wx.ID_ANY, 0, 0, 255, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_LABELS )
		bSizer1.Add( self.sli_low, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		self.btn_8bit = wx.Button( self, wx.ID_ANY, u"0-255", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_8bit.SetMaxSize( wx.Size( -1,40 ) )
		
		bSizer2.Add( self.btn_8bit, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		
		bSizer2.AddStretchSpacer(prop=1)
		
		self.btn_minmax = wx.Button( self, wx.ID_ANY, u"min-max", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_minmax.SetMaxSize( wx.Size( -1,40 ) )
		bSizer2.Add( self.btn_minmax, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		
		bSizer2.AddStretchSpacer(prop=1)
		
		self.btn_slice = wx.Button( self, wx.ID_ANY, u"slice", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_slice.SetMaxSize( wx.Size( -1,40 ) )
		bSizer2.Add( self.btn_slice, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		
		bSizer2.AddStretchSpacer(prop=1)
		
		self.btn_stack = wx.Button( self, wx.ID_ANY, u"stack", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_stack.SetMaxSize( wx.Size( -1,40 ) )
		bSizer2.Add( self.btn_stack, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		
		bSizer1.Add( bSizer2, 0, wx.EXPAND |wx.ALL, 5 )

		line = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( line, 0, wx.EXPAND |wx.ALL, 5 )

		self.cmapsel = CMapSelPanel(self)
		luts = ColorManager.luts
		self.cmapsel.SetItems(list(luts.keys()), list(luts.values()))
		bSizer1.Add(self.cmapsel, 0, wx.ALL|wx.EXPAND, 5 )

		self.cmap = CMapPanel(self)
		bSizer1.Add(self.cmap, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.sli_high.Bind( wx.EVT_SCROLL, self.on_low )
		self.sli_low.Bind( wx.EVT_SCROLL, self.on_high )
		self.btn_8bit.Bind( wx.EVT_BUTTON, self.on_8bit )
		self.btn_minmax.Bind( wx.EVT_BUTTON, self.on_minmax )
		self.btn_slice.Bind( wx.EVT_BUTTON, self.on_slice )
		self.btn_stack.Bind( wx.EVT_BUTTON, self.on_stack )
		self.cmap.set_handle(self.on_cmap)
		self.cmapsel.set_handle(self.on_cmapsel)

		self.range = (0, 255)
	
	def on_cmap(self):
		ips = IPy.get_ips()
		if ips is None: return
		cmap = CMapPanel.linear_color(self.cmap.GetValue())
		ips.lut = cmap
		ips.update = 'pix'

	def on_cmapsel(self):
		ips = IPy.get_ips()
		if ips is None: return
		key = self.cmapsel.GetValue()
		ips.lut = ColorManager.get_lut(key)
		ips.update = 'pix'
	
	# Virtual event handlers, overide them in your derived class
	def on_low( self, event ):
		ips = IPy.get_ips()
		if ips is None: return
		if self.sli_high.GetValue()<self.sli_low.GetValue():
			self.sli_high.SetValue(self.sli_low.GetValue())
		ips.range = (self.sli_low.GetValue(), self.sli_high.GetValue())
		lim1 = 1.0 * (self.sli_low.GetValue() - self.range[0])/(self.range[1]-self.range[0])
		lim2 = 1.0 * (self.sli_high.GetValue() - self.range[0])/(self.range[1]-self.range[0])
		self.histpan.set_lim(lim1*255, lim2*255)
		ips.update = 'pix'
	
	def on_high( self, event ):
		ips = IPy.get_ips()
		if ips is None: return
		if self.sli_low.GetValue()>self.sli_high.GetValue():
			self.sli_low.SetValue(self.sli_high.GetValue())
		ips.range = (self.sli_low.GetValue(), self.sli_high.GetValue())
		lim1 = 1.0 * (self.sli_low.GetValue() - self.range[0])/(self.range[1]-self.range[0])
		lim2 = 1.0 * (self.sli_high.GetValue() - self.range[0])/(self.range[1]-self.range[0])
		self.histpan.set_lim(lim1*255, lim2*255)
		ips.update = 'pix'
	
	def on_8bit( self, event ):
		ips = IPy.get_ips()
		if ips is None: return
		self.range = ips.range = (0,255)
		hist = ips.histogram()
		self.histpan.set_hist(hist)
		self.sli_low.SetMax(255)
		self.sli_low.SetMin(0)
		self.sli_high.SetMax(255)
		self.sli_high.SetMin(0)
		self.sli_low.SetValue(0)
		self.sli_high.SetValue(255)
		self.histpan.set_lim(0,255)
		ips.update = 'pix'
	
	def on_minmax( self, event ):
		ips = IPy.get_ips()
		if ips is None: return
		minv, maxv = ips.get_updown()
		self.range = ips.range = (minv, maxv)
		hist = ips.histogram()
		self.histpan.set_hist(hist)
		self.sli_low.SetMax(maxv)
		self.sli_low.SetMin(minv)
		self.sli_high.SetMax(maxv)
		self.sli_high.SetMin(minv)
		self.sli_low.SetValue(minv)
		self.sli_high.SetValue(maxv)
		self.histpan.set_lim(0,255)
		ips.update = 'pix'
	
	def on_slice( self, event ):
		ips = IPy.get_ips()
		if ips is None: return
		hist = ips.histogram()
		self.histpan.set_hist(hist)
	
	def on_stack( self, event ):
		ips = IPy.get_ips()
		if ips is None: return
		hists = ips.histogram(stack=True)
		self.histpan.set_hist(hists)