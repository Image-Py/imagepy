import wx, wx.lib.agw.aui as aui
from .mcanvas import MCanvas3D

class Canvas3DFrame(wx.Frame):
	def __init__(self, parent=None):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
							title = 'Canvas3DFrame',
							pos = wx.DefaultPosition,
							size = wx.Size( 800, 600 ),
							style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.canvas = MCanvas3D(self)
		sizer.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 0)
		self.SetSizer(sizer)
		self.Bind(wx.EVT_IDLE, self.on_idle)

		self.view_x = self.canvas.view_x
		self.view_y = self.canvas.view_y
		self.view_z = self.canvas.view_z
		self.on_pers = self.canvas.set_pers
		self.set_background = self.canvas.set_background
		self.set_scatter = self.canvas.set_scatter
		self.set_bright = self.canvas.set_bright
		self.add_surf_asyn = self.canvas.add_surf_asyn
		self.add_surf = self.canvas.add_surf
		self.add_mark_asyn = self.canvas.add_mark_asyn
		self.add_mark = self.canvas.add_mark
		self.set_mesh = self.canvas.set_mesh

	def on_idle(self, event):
		if self.GetTitle()!=self.canvas.meshset.title:
			self.SetTitle(self.canvas.meshset.title)

	def set_title(self, tab): self.SetTitle(tab.title)

	def on_valid(self, event): event.Skip()

	def on_close(self, event): event.Skip()
    
class Canvas3DNoteBook(wx.lib.agw.aui.AuiNotebook):
	def __init__(self, parent):
		wx.lib.agw.aui.AuiNotebook.__init__( self, parent, wx.ID_ANY, 
		    wx.DefaultPosition, wx.DefaultSize, wx.lib.agw.aui.AUI_NB_DEFAULT_STYLE )
		self.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_valid) 
		self.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)
		self.Bind( wx.EVT_IDLE, self.on_idle)
		self.SetArtProvider(aui.AuiSimpleTabArt())

	def on_idle(self, event):
		for i in range(self.GetPageCount()):
			title = self.GetPage(i).mesh.name
			if self.GetPageText(i) != title:
				self.SetPageText(i, title)

	def canvas(self, i=None):
		if not i is None: return self.GetPage(i)
		else: return self.GetCurrentPage()

	def set_background(self, img):
		self.GetAuiManager().SetArtProvider(ImgArtabtProvider(img))

	def add_canvas(self, canvas=None):
		if canvas is None: canvas = MCanvas3D(self)
		self.AddPage(canvas, 'Image', True, wx.NullBitmap )
		return canvas

	def set_title(self, panel, title):
		self.SetPageText(self.GetPageIndex(panel), title)

	def on_valid(self, event): pass

	def on_close(self, event): pass

class Canvas3DNoteFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
							title = 'CanvasNoteFrame',
							pos = wx.DefaultPosition,
							size = wx.Size( 800, 600 ),
							style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.notebook = Canvas3DNoteBook(self)
		self.canvas = self.notebook.canvas
		sizer.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 0 )
		self.SetSizer(sizer)
		self.add_canvas = self.notebook.add_canvas
		self.Layout()


if __name__=='__main__':
	from skimage.data import camera, astronaut
	from skimage.io import imread

	df = pd.DataFrame(np.arange(100).reshape((20,5)))
	app = wx.App()
	cf = GridFrame(None)
	cf.set_data(df)
	cf.Show()
	app.MainLoop()

	'''
	app = wx.App()
	cnf = CanvasNoteFrame(None)
	canvas = cnf.add_img()
	canvas.set_img(camera())

	canvas = cnf.add_img()
	canvas.set_img(camera())
	canvas.set_cn(0)

	cnf.Show()
	app.MainLoop()
	'''
