import wx, weakref
from sciapp.action import Macros
import os.path as osp

class Plugin ( wx.Panel ):
	title = 'Macros Recorder'

	def __init__( self, parent, app=None):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size(300, 200), style = wx.TAB_TRAVERSAL )
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		root = osp.abspath(osp.dirname(__file__))
		self.toolbar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.tol_open = self.toolbar.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( osp.join(root, "icons/open.png"), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_save = self.toolbar.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( osp.join(root, "icons/save.png"), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.toolbar.AddSeparator()
		
		self.tol_cut = self.toolbar.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( osp.join(root, "icons/cut.png"), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_copy = self.toolbar.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( osp.join(root, "icons/copy.png"), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_paste = self.toolbar.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( osp.join(root, "icons/paste.png"), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_delete = self.toolbar.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( osp.join(root, "icons/delete.png"), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.toolbar.AddSeparator()
		
		self.m_run = self.toolbar.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( osp.join(root, "icons/play.png"), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.tol_runlines = self.toolbar.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( osp.join(root, "icons/runlines.png"), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_record = self.toolbar.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( osp.join(root, "icons/record.png"), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_RADIO, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_pause = self.toolbar.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( osp.join(root, "icons/pause.png"), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_RADIO, wx.EmptyString, wx.EmptyString, None ) 
		
		
		self.toolbar.Realize() 
		
		bSizer1.Add( self.toolbar, 0, wx.EXPAND, 0 )
		
		self.txt_cont = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer1.Add( self.txt_cont, 1, wx.ALL|wx.EXPAND, 5 )
		self.file = ''
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.Fit()
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.on_open, id = self.tol_open.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_save, id = self.m_save.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_cut, id = self.tol_cut.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_copy, id = self.m_copy.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_paste, id = self.m_paste.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_delete, id = self.m_delete.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_run, id = self.m_run.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_record, id = self.m_record.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_pause, id = self.m_pause.GetId() )
		self.Bind( wx.EVT_TOOL, self.on_runlines, id = self.tol_runlines.GetId() )


		self.recording = True	
	
	# Virtual event handlers, overide them in your derived class
	def on_open( self, event ):
		filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in ['mc']])
		dialog=wx.FileDialog(None, 'Open  Macros', '', '', filt, style=wx.FD_OPEN)
		if dialog.ShowModal()==wx.ID_OK:
			self.file=dialog.GetPath()
			file=open(self.file)
			self.txt_cont.WriteText(file.read())
			file.close()
		dialog.Destroy()
	
	def on_save( self, event ):
		if self.file=='':
			filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in ['mc']])
			dialog=wx.FileDialog(None,'Save Macros', '', '', filt, style=wx.FD_SAVE)
			if dialog.ShowModal()==wx.ID_OK:
				self.file=dialog.GetPath()
				self.txt_cont.SaveFile(self.file)
			dialog.Destroy()
		else:
			self.txt_cont.SaveFile(self.file)
	
	def on_cut( self, event ):
		self.txt_cont.Cut()
	
	def on_copy( self, event ):
		self.txt_cont.Copy()
	
	def on_paste( self, event ):
		self.txt_cont.Paste()
	
	def on_delete( self, event ):
		self.txt_cont.Clear()
	
	def on_run( self, event ):
		cmds = self.txt_cont.GetValue().split('\n')
		Macros(None, cmds).start(self.GetParent().GetParent())
	
	def on_record( self, event ):
		self.recording = True
	
	def on_pause( self, event ):
		self.recording = False
	
	def on_runlines( self, event ):
		cmds = self.txt_cont.GetStringSelection().split('\n')
		Macros(None, cmds).start(self.GetParent().GetParent())

	def write(self, cont):
		if not self.recording: return
		self.txt_cont.AppendText((cont+'\n'))