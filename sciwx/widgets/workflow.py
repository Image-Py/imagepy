import wx

def parse(cont):
	ls = cont.split('\n')
	workflow = {'title':ls[0], 'chapter':[]}
	for line in ls[2:]:
		line = line.strip()
		if line == '':continue
		if line.startswith('## '):
			chapter = {'title':line[3:], 'section':[]}
			workflow['chapter'].append(chapter)
		elif line[1:3] == '. ':
			section = {'title':line[3:]}
		else:
			section['hint'] = line
			chapter['section'].append(section)
	return workflow

class WorkFlowPanel ( wx.Panel ):
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.TAB_TRAVERSAL )
		self.app, self.f = parent, print

	def SetValue(self, cont):
		self.workflow, self.cont = parse(cont), cont
		sizer_scroll = wx.BoxSizer( wx.HORIZONTAL )
		
		self.scr_workflow = wx.ScrolledCanvas( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
		self.scr_workflow.SetScrollRate( 30, 0 )
		self.scr_workflow.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_NEVER)
		self.scr_workflow.SetMinSize((600,-1))

		sizer_chapter = wx.BoxSizer( wx.HORIZONTAL )
		self.spn_scroll = wx.SpinButton( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_HORIZONTAL )
		sizer_scroll.Add( self.spn_scroll, 0, wx.ALL|wx.EXPAND, 3 )

		for chapter in self.workflow['chapter']:
			self.pan_chapter = wx.Panel( self.scr_workflow, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL )
			sizer_frame = wx.BoxSizer( wx.VERTICAL )
			
			self.lab_chapter = wx.StaticText( self.pan_chapter, wx.ID_ANY, chapter['title'], wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
			self.lab_chapter.Wrap( -1 )
			self.lab_chapter.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
			
			sizer_frame.Add( self.lab_chapter, 0, wx.ALL|wx.EXPAND, 0 )
			
			sizer_section = wx.BoxSizer( wx.HORIZONTAL )
			for section in chapter['section']:
				btn = wx.Button( self.pan_chapter, wx.ID_ANY, section['title'], wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
				sizer_section.Add( btn, 0, wx.ALL, 3 )
				btn.Bind(wx.EVT_BUTTON, lambda e, x=section['title']: self.f(x))
				btn.Bind( wx.EVT_ENTER_WINDOW, lambda e, info=section['hint']: self.info(info))
				#self.m_button1.Bind( wx.EVT_LEAVE_WINDOW, self.on_out )

			sizer_frame.Add( sizer_section, 0, wx.EXPAND, 3 )
			sizer_btn = wx.BoxSizer( wx.HORIZONTAL )
			sizer_btn.AddStretchSpacer(1)
			
			self.btn_snap = wx.StaticText( self.pan_chapter, wx.ID_ANY, u" Snap ", wx.DefaultPosition, wx.DefaultSize, 0|wx.SIMPLE_BORDER )
			self.btn_snap.Wrap( -1 )
			sizer_btn.Add( self.btn_snap, 0, wx.ALL, 3 )
			
			self.btn_load = wx.StaticText( self.pan_chapter, wx.ID_ANY, u" Load ", wx.DefaultPosition, wx.DefaultSize, 0|wx.SIMPLE_BORDER )
			self.btn_load.Wrap( -1 )
			sizer_btn.Add( self.btn_load, 0, wx.ALL, 3 )
			
			self.btn_step = wx.StaticText( self.pan_chapter, wx.ID_ANY, u" >> ", wx.DefaultPosition, wx.DefaultSize, 0|wx.SIMPLE_BORDER )
			self.btn_step.Wrap( -1 )
			sizer_btn.Add( self.btn_step, 0, wx.ALL, 3 )
			sizer_frame.Add( sizer_btn, 0, wx.EXPAND, 3 )
		
		
			self.pan_chapter.SetSizer( sizer_frame )
			self.pan_chapter.Layout()
			sizer_frame.Fit( self.pan_chapter )
			sizer_chapter.Add( self.pan_chapter, 0, wx.EXPAND |wx.ALL, 3 )
		
		sizer_scroll.Add( self.scr_workflow, 1, wx.EXPAND |wx.ALL, 0)
		sizer_info = wx.BoxSizer( wx.VERTICAL )
		sizer_info.SetMinSize( wx.Size( 260,-1 ) ) 
		self.btn_help = wx.StaticText( self, wx.ID_ANY, u" Click For Detail Document ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.btn_help.Wrap( -1 )
		self.btn_help.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		sizer_info.Add( self.btn_help, 0, wx.ALL|wx.EXPAND, 0 )
		
		self.txt_info = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_AUTO_URL|wx.TE_MULTILINE|wx.TE_READONLY )
		sizer_info.Add( self.txt_info, 1, wx.TOP|wx.EXPAND, 3 )
		
		sizer_scroll.Add( sizer_info, 0, wx.EXPAND |wx.ALL, 3)

		self.scr_workflow.SetSizer( sizer_chapter )
		self.scr_workflow.Layout()	
		
		self.SetSizer( sizer_scroll )
		
		#self.Fit()
		self.Layout()

		self.spn_scroll.Bind( wx.EVT_SPIN, self.on_spn )
		self.btn_help.Bind( wx.EVT_LEFT_DOWN, self.on_help )

	def info(self, info):
		self.txt_info.SetValue(info)

	def on_spn(self, event):
		v = self.spn_scroll.GetValue()
		self.scr_workflow.Scroll(v, 0)
		self.spn_scroll.SetValue(self.scr_workflow.GetViewStart()[0])

	def Bind(self, event, f=print): self.f = f

	def on_help(self, event):
		self.app.show_md(self.cont, self.workflow['title'])

if __name__ == '__main__':

	cont = '''Title
=====
## Chapter1
1. Section1
some coment for section1 ...
2. Section2
some coment for section2 ...
## Chapter2
1. Section1
some coment for section1 ...
2. Section2
some coment for section2 ...
'''

	app = wx.App()
	frame = wx.Frame(None)
	sizer = wx.BoxSizer(wx.VERTICAL)
	wf = WorkFlowPanel(frame)
	wf.SetValue(cont)
	sizer.Add(wf, 0, wx.EXPAND, 0 )
	frame.SetSizer(sizer)
	frame.Show()
	app.MainLoop()