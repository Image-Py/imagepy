import wx
from imagepy.core.manager import RoiManager
from imagepy.core.engine import Macros
from imagepy import IPy

class VirtualListCtrl(wx.ListCtrl):
	def __init__(self, parent, title, data=[]):
		wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VIRTUAL)
		self.title, self.data = title, data
		#self.Bind(wx.EVT_LIST_CACHE_HINT, self.DoCacheItems)
		for col, text in enumerate(title):
		    self.InsertColumn(col, text)
		self.SetValue(data)

	def OnGetItemText(self, row, col):
		return self.data[row][col]

	def OnGetItemAttr(self, item):  return None
	    
	def OnGetItemImage(self, item): return -1
	    
	def SetValue(self, data):
		self.data = data
		self.SetItemCount(len(data))

	def Refresh(self):
		self.SetItemCount(len(self.data))
		wx.ListCtrl.Refresh(self)

class Plugin(wx.Panel):
	title = 'ROI Ctrl Panel'
	single = None
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size(-1,-1), style = wx.TAB_TRAVERSAL )
		
		sizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.note_book = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_LEFT|wx.NB_TOP )
		#self.note_book = wx.Choicebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.CHB_DEFAULT )
		self.pan_manage = wx.Panel( self.note_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizer_manage = wx.BoxSizer( wx.VERTICAL )
		
		self.btn_add = wx.Button( self.pan_manage, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_manage.Add( self.btn_add, 0, wx.ALL, 5 )
		
		self.btn_load = wx.Button( self.pan_manage, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_manage.Add( self.btn_load, 0, wx.ALL, 5 )
		
		self.btn_update = wx.Button( self.pan_manage, wx.ID_ANY, u"Update", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_manage.Add( self.btn_update, 0, wx.ALL, 5 )
		
		self.btn_remove = wx.Button( self.pan_manage, wx.ID_ANY, u"Remove", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_manage.Add( self.btn_remove, 0, wx.ALL, 5 )
		
		self.btn_open = wx.Button( self.pan_manage, wx.ID_ANY, u"Open", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_manage.Add( self.btn_open, 0, wx.ALL, 5 )
		
		self.btn_save = wx.Button( self.pan_manage, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_manage.Add( self.btn_save, 0, wx.ALL, 5 )
		
		
		self.pan_manage.SetSizer( sizer_manage )
		self.pan_manage.Layout()
		sizer_manage.Fit( self.pan_manage )
		self.note_book.AddPage( self.pan_manage, u"Manage", True )
		self.pan_operate = wx.Panel( self.note_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizer_operate = wx.BoxSizer( wx.VERTICAL )
		
		self.btn_inflate = wx.Button( self.pan_operate, wx.ID_ANY, u"Inflate", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_operate.Add( self.btn_inflate, 0, wx.ALL, 5 )
		
		self.btn_shrink = wx.Button( self.pan_operate, wx.ID_ANY, u"Shrink", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_operate.Add( self.btn_shrink, 0, wx.ALL, 5 )
		
		self.btn_convex = wx.Button( self.pan_operate, wx.ID_ANY, u"Convex", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_operate.Add( self.btn_convex, 0, wx.ALL, 5 )
		
		self.btn_bound = wx.Button( self.pan_operate, wx.ID_ANY, u"Bound", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_operate.Add( self.btn_bound, 0, wx.ALL, 5 )
		
		self.btn_clip = wx.Button( self.pan_operate, wx.ID_ANY, u"Clip", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_operate.Add( self.btn_clip, 0, wx.ALL, 5 )
		
		self.btn_invert = wx.Button( self.pan_operate, wx.ID_ANY, u"Invert", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_operate.Add( self.btn_invert, 0, wx.ALL, 5 )
		
		
		self.pan_operate.SetSizer( sizer_operate )
		self.pan_operate.Layout()
		sizer_operate.Fit( self.pan_operate )
		self.note_book.AddPage( self.pan_operate, u"Operate", False )
		self.pan_relation = wx.Panel( self.note_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizer_relation = wx.BoxSizer( wx.VERTICAL )
		
		self.btn_intersect = wx.Button( self.pan_relation, wx.ID_ANY, u"Intersect", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_relation.Add( self.btn_intersect, 0, wx.ALL, 5 )

		self.btn_union = wx.Button( self.pan_relation, wx.ID_ANY, u"Union", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_relation.Add( self.btn_union, 0, wx.ALL, 5 )
		
		self.btn_difference = wx.Button( self.pan_relation, wx.ID_ANY, u"Difference", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_relation.Add( self.btn_difference, 0, wx.ALL, 5 )

		self.btn_symdiff = wx.Button( self.pan_relation, wx.ID_ANY, u"Sym Diff", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_relation.Add( self.btn_symdiff, 0, wx.ALL, 5 )
		
		
		self.pan_relation.SetSizer( sizer_relation )
		self.pan_relation.Layout()
		sizer_relation.Fit( self.pan_relation )
		self.note_book.AddPage( self.pan_relation, u"Relationship", False )
		self.pan_draw = wx.Panel( self.note_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sizer_draw = wx.BoxSizer( wx.VERTICAL )
		
		self.btn_sketch = wx.Button( self.pan_draw, wx.ID_ANY, u"Sketch", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_draw.Add( self.btn_sketch, 0, wx.ALL, 5 )
		
		self.btn_clear = wx.Button( self.pan_draw, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_draw.Add( self.btn_clear, 0, wx.ALL, 5 )
		
		self.btn_clearout = wx.Button( self.pan_draw, wx.ID_ANY, u"Clear Out", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_draw.Add( self.btn_clearout, 0, wx.ALL, 5 )
		
		sizer_draw.AddStretchSpacer(1)
		self.btn_setting = wx.Button( self.pan_draw, wx.ID_ANY, u"Setting", wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer_draw.Add( self.btn_setting, 0, wx.ALL, 5 )

		self.pan_draw.SetSizer( sizer_draw )
		self.pan_draw.Layout()
		sizer_draw.Fit( self.pan_draw )
		self.note_book.AddPage( self.pan_draw, u"Draw", False )
		
		sizer.Add( self.note_book, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.lst_rois = VirtualListCtrl(self, ['name', 'type'], [])
		self.UpdateData()

		sizer.Add( self.lst_rois, 1, wx.ALL|wx.EXPAND, 5 )
		self.SetSizer( sizer )
		self.Fit()
		self.Layout()
		self.AddEvent()
		
	def AddEvent(self):
		self.btn_add.Bind(wx.EVT_BUTTON, self.on_add)
		self.btn_load.Bind(wx.EVT_BUTTON, self.on_load)
		self.btn_update.Bind(wx.EVT_BUTTON, self.on_update)
		self.btn_remove.Bind(wx.EVT_BUTTON, self.on_remove)
		self.btn_open.Bind(wx.EVT_BUTTON, self.on_open)
		self.btn_save.Bind(wx.EVT_BUTTON, self.on_save)
		self.btn_inflate.Bind(wx.EVT_BUTTON, self.on_inflate)
		self.btn_shrink.Bind(wx.EVT_BUTTON, self.on_shrink)
		self.btn_convex.Bind(wx.EVT_BUTTON, self.on_convex)
		self.btn_bound.Bind(wx.EVT_BUTTON, self.on_box)
		self.btn_clip.Bind(wx.EVT_BUTTON, self.on_clip)
		self.btn_invert.Bind(wx.EVT_BUTTON, self.on_invert)
		self.btn_intersect.Bind(wx.EVT_BUTTON, self.on_intersect)
		self.btn_union.Bind(wx.EVT_BUTTON, self.on_union)
		self.btn_difference.Bind(wx.EVT_BUTTON, self.on_difference)
		self.btn_symdiff.Bind(wx.EVT_BUTTON, self.on_symdiff)
		self.btn_sketch.Bind(wx.EVT_BUTTON, self.on_sketch)
		self.btn_clear.Bind(wx.EVT_BUTTON, self.on_clear)
		self.btn_clearout.Bind(wx.EVT_BUTTON, self.on_clearout)
		self.btn_setting.Bind(wx.EVT_BUTTON, self.on_setting)
		self.lst_rois.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.on_load)

	def on_add(self, event):
		Macros('', ['ROI Add>None']).start(callafter=self.UpdateData)

	def on_load(self, event):
		idx = self.lst_rois.GetFirstSelected()
		if idx==-1: return IPy.alert('No ROI Selected!')
		name = self.lst_rois.OnGetItemText(idx, 0)
		Macros('', ['ROI Load>{"name":"%s"}'%name]).start()

	def on_remove(self, event):
		idx = self.lst_rois.GetFirstSelected()
		if idx==-1: return IPy.alert('No ROI Selected!')
		name = self.lst_rois.OnGetItemText(idx, 0)
		Macros('', ['ROI Remove>{"name":"%s"}'%name]).start(callafter=self.UpdateData)

	def on_open(self, event):
		Macros('', ['ROI Open>None']).start()

	def on_save(self, event):
		Macros('', ['ROI Save>None']).start()

	def on_inflate(self, event):
		Macros('', ['ROI Inflate>None']).start()

	def on_shrink(self, event):
		Macros('', ['ROI Shrink>None']).start()

	def on_convex(self, event):
		Macros('', ['ROI Convex Hull>None']).start()
		
	def on_box(self, event):
		Macros('', ['ROI Bound Box>None']).start()

	def on_clip(self, event):
		Macros('', ['ROI Clip>None']).start()

	def on_invert(self, event):
		Macros('', ['ROI Invert>None']).start()

	def on_intersect(self, event):
		idx = self.lst_rois.GetFirstSelected()
		if idx==-1: return IPy.alert('No ROI Selected!')
		name = self.lst_rois.OnGetItemText(idx, 0)
		Macros('', ['ROI Intersect>{"name":"%s"}'%name]).start()

	def on_union(self, event):
		idx = self.lst_rois.GetFirstSelected()
		if idx==-1: return IPy.alert('No ROI Selected!')
		name = self.lst_rois.OnGetItemText(idx, 0)
		Macros('', ['ROI Union>{"name":"%s"}'%name]).start()

	def on_difference(self, event):
		idx = self.lst_rois.GetFirstSelected()
		if idx==-1: return IPy.alert('No ROI Selected!')
		name = self.lst_rois.OnGetItemText(idx, 0)
		Macros('', ['ROI Difference>{"name":"%s"}'%name]).start()

	def on_symdiff(self, event):
		idx = self.lst_rois.GetFirstSelected()
		if idx==-1: return IPy.alert('No ROI Selected!')
		name = self.lst_rois.OnGetItemText(idx, 0)
		Macros('', ['ROI Symmetric Diff>{"name":"%s"}'%name]).start()

	def on_clear(self, event):
		Macros('', ['Clear>None']).start()

	def on_clearout(self, event):
		Macros('', ['Clear Out>None']).start()

	def on_sketch(self, event):
		Macros('', ['Sketch>None']).start()

	def on_update(self, event):
		self.UpdateData()

	def on_setting(self, event):
		Macros('', ['ROI Setting>None']).start()

	def UpdateData(self):
		names = RoiManager.get_titles()
		types = [RoiManager.get(i).dtype for i in names]
		self.lst_rois.SetValue(list(zip(names, types)))

	def __del__( self ):
		pass