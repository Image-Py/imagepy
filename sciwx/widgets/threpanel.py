import wx, math
from .histpanel import HistPanel
from .normal import FloatSlider

class ThresholdPanel( wx.Panel ):
	def __init__( self, parent, mode, hist, rang, accury, app=None):
		wx.Panel.__init__ ( self, parent)
		(self.lim1, self.lim2), self.mode = rang, mode
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.histpan = HistPanel(self)
		self.histpan.SetValue(hist)
		bSizer1.Add(self.histpan, 0, wx.ALL|wx.EXPAND, 5 )

		self.sli_high = FloatSlider(self, rang, accury, '', '')
		self.sli_high.SetValue(rang[0])
		bSizer1.Add( self.sli_high, 0, wx.ALL|wx.EXPAND, 0 )
		if mode == 'bc': rang, accury = (1, 89), 0
		self.sli_low = FloatSlider(self, rang, accury, '', '')
		self.sli_low.SetValue(rang[1])
		bSizer1.Add( self.sli_low, 0, wx.ALL|wx.EXPAND, 0 )
		self.SetSizer(bSizer1)

	def on_threshold(self, dir, event):
		if self.f is None: return
		a, b = self.GetValue()
		if self.mode == 'lh':
			if dir: b = max(a, b)
			else: a = min(a, b)
			self.SetValue((a,b))
			a = int((a-self.lim1)/(self.lim2-self.lim1)*255)
			b = int((b-self.lim1)/(self.lim2-self.lim1)*255)
			self.histpan.set_lim(a, b)
		if self.mode == 'bc':
			mid = 128-a/(self.lim2-self.lim1)*255
			length = 255/math.tan(b/180.0*math.pi)
			self.histpan.set_lim(mid-length/2, mid+length/2)
		self.f(self)

	def Bind(self, z, f):
		self.f = f
		self.sli_high.Bind(z, lambda e: self.on_threshold(True, e))
		self.sli_low.Bind(z, lambda e: self.on_threshold(False, e))

	def SetValue(self, n):
		self.sli_high.SetValue(n[0])
		self.sli_low.SetValue(n[1])
	    
	def GetValue(self):
		b = self.sli_low.GetValue()
		a = self.sli_high.GetValue()
		return None if None in (a,b) else (a,b)