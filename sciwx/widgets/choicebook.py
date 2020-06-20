import wx

class ChoiceBook(wx.ScrolledWindow):
	def __init__(self, parent, app=None):
		wx.ScrolledWindow.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.app = app or parent
		self.SetSizer(wx.BoxSizer( wx.VERTICAL ))

	def add_wgts(self, name, wgts):
		book = wx.Choicebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.CHB_DEFAULT )
		for name, wgt in wgts:
			book.AddPage(wgt(book, self.app), name, False )
		self.GetSizer().Add( book, 0, wx.EXPAND |wx.ALL, 0 )
		self.Layout()
		self.GetSizer().Fit(self)

	def load(self, data):
		for name, wgts in data[1]:
			self.add_wgts(name, wgts)

	def clear(self):
		self.DestroyChildren()

if __name__ == '__main__':
	app = wx.App()
	frame = wx.Frame(None)
	book = ChoiceBook(frame)
	book.load(('widgets', [('panels', [('A', wx.Panel), ('B', wx.Panel)]),
		('panels2', [('A', wx.Panel), ('B', wx.Panel)])]))
	frame.Show()
	app.MainLoop()
