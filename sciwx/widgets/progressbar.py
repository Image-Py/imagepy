import threading, time, wx

class ProgressBar ( wx.Panel ):
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )
		
		sizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.lab_name = wx.StaticText( self, wx.ID_ANY, u"Process", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lab_name.Wrap( -1 )
		sizer.Add( self.lab_name, 0, wx.RIGHT, 5 )
		
		self.gau_bar = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.gau_bar.SetValue( 0 ) 
		sizer.Add( self.gau_bar, 0, wx.ALL, 0 )
		
		self.progress = []
		self.cur = 0
		self.SetSizer( sizer )
		self.Layout()
		self.Fit()

		thread = threading.Thread(None, self.hold, ())
		thread.setDaemon(True)
		thread.start()

	def SetValue(self, values=[]):
		self.progress = values

	def hold(self):
		span, c, t = 30, 0, 0
		while True:
			time.sleep(0.1)
			try:
				if len(self.progress)==0 and self.IsShown(): self.Hide()
				if len(self.progress)>0 and not self.IsShown(): self.Show()
				if len(self.progress)==0: continue
				t = (t + 1)%span
				if t==0: self.cur = (self.cur + 1)%len(self.progress)
				name, f = self.progress[self.cur]
				wx.CallAfter(self.lab_name.SetLabel, name)
				if f() is None:
					c = (c + 5)%200
					wx.CallAfter(self.gau_bar.SetValue, 100-abs(c-100))
				else: wx.CallAfter(self.gau_bar.SetValue, f())
				self.Layout()
				self.GetParent().Layout()
			except: pass

if __name__ == '__main__':
	app = wx.App()
	frame = wx.Frame(None)
	pb = ProgressBar(frame)
	pb.SetValue([('third', lambda : -1)])
	frame.Show()
	app.MainLoop()
