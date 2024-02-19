from ..widgets import HistPanel, CMapPanel, FloatSlider
import numpy as np
import wx

class Channels( wx.Panel ):
	title = 'Channels RGB'
	def __init__( self, parent , app):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 255,0 ), style = wx.TAB_TRAVERSAL )
		self.app = app

		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		sizer_chans = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_r = wx.Button( self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		self.btn_r.SetBackgroundColour( wx.Colour( 255, 0, 0 ) )
		self.btn_r.SetMaxSize( wx.Size( -1,40 ) )
		sizer_chans.Add( self.btn_r, 0, wx.ALL|wx.CENTER, 0)
		
		com_rChoices = [ u"C:0" ]
		self.com_r = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, com_rChoices, wx.CB_READONLY )
		self.com_r.SetSelection( 0 )
		self.com_r.SetInitialSize((50,-1))
		sizer_chans.Add( self.com_r, 1, wx.ALL|wx.EXPAND, 1)
		
		self.btn_g = wx.Button( self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		self.btn_g.SetBackgroundColour( wx.Colour( 0, 255, 0 ) )
		self.btn_g.SetMaxSize( wx.Size( -1,40 ) )
		
		sizer_chans.Add( self.btn_g, 0, wx.ALL|wx.CENTER, 0)
		
		com_gChoices = [ u"C:1" ]
		self.com_g = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, com_gChoices, wx.CB_READONLY )
		self.com_g.SetSelection( 0 )
		self.com_g.SetInitialSize((50,-1))
		sizer_chans.Add( self.com_g, 1, wx.ALL|wx.EXPAND, 1)
		
		self.btn_b = wx.Button( self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		self.btn_b.SetBackgroundColour( wx.Colour( 0, 0, 255 ) )
		self.btn_b.SetMaxSize( wx.Size( -1,40 ) )
		sizer_chans.Add( self.btn_b, 0, wx.ALL|wx.CENTER, 0)
		
		com_bChoices = [ u"C:2" ]
		self.com_b = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, (-1,-1), com_bChoices, wx.CB_READONLY )
		self.com_b.SetSelection( 0 )
		self.com_b.SetInitialSize((50,-1))
		sizer_chans.Add( self.com_b, 1, wx.ALL|wx.EXPAND, 1 )

		self.btn_gray = wx.Button( self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		self.btn_gray.SetBackgroundColour( wx.Colour( 128, 128, 128 ) )
		self.btn_gray.SetMaxSize( wx.Size( -1,40 ) )
		sizer_chans.Add( self.btn_gray, 0, wx.ALL|wx.CENTER, 0)

		bSizer1.Add(sizer_chans, 0, wx.ALL|wx.EXPAND, 2)

		self.histpan = HistPanel(self)
		bSizer1.Add(self.histpan, 0, wx.ALL|wx.EXPAND, 5 )

		self.sli_high = FloatSlider(self, (0,255), 0, '')
		self.sli_high.SetValue(255)
		bSizer1.Add( self.sli_high, 0, wx.ALL|wx.EXPAND, 0 )
		
		self.sli_low = FloatSlider(self, (0,255), 0, '')
		self.sli_low.SetValue(0)
		bSizer1.Add( self.sli_low, 0, wx.ALL|wx.EXPAND, 0 )
		

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		self.btn_8bit = wx.Button( self, wx.ID_ANY, u"255", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_8bit.SetMaxSize( wx.Size( -1,40 ) )
		
		bSizer2.Add( self.btn_8bit, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		
		bSizer2.AddStretchSpacer(prop=1)
		
		self.btn_minmax = wx.Button( self, wx.ID_ANY, u"100", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_minmax.SetMaxSize( wx.Size( -1,40 ) )
		bSizer2.Add( self.btn_minmax, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		
		bSizer2.AddStretchSpacer(prop=1)
		
		self.btn_90 = wx.Button( self, wx.ID_ANY, "90", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_90.SetMaxSize( wx.Size( -1,40 ) )
		bSizer2.Add( self.btn_90, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		
		bSizer2.AddStretchSpacer(prop=1)
		
		self.btn_95 = wx.Button( self, wx.ID_ANY, "95", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_95.SetMaxSize( wx.Size( -1,40 ) )
		bSizer2.Add( self.btn_95, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		
		bSizer2.AddStretchSpacer(prop=1)

		self.btn_99 = wx.Button( self, wx.ID_ANY, "99", wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_EXACTFIT )
		self.btn_99.SetMaxSize( wx.Size( -1,40 ) )
		bSizer2.Add( self.btn_99, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		
		bSizer2.AddStretchSpacer(prop=1)

		self.chk_stack = wx.CheckBox( self, wx.ID_ANY, u"stack", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.chk_stack, 0, wx.ALIGN_CENTER|wx.ALL, 0 )

		
		bSizer1.Add( bSizer2, 0, wx.EXPAND |wx.ALL, 5 )

		sizer_mode = wx.BoxSizer( wx.HORIZONTAL )
		
		#self.btn_back = wx.Button( self, wx.ID_ANY, 'Bg', wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		#self.btn_back.SetMaxSize( wx.Size( -1,40 ) )
		#self.btn_back = wx.StaticText( self, wx.ID_ANY, u" BG ", wx.DefaultPosition, wx.DefaultSize, 0|wx.SIMPLE_BORDER )
		#self.btn_back.Wrap( -1 )
		#sizer_mode.Add( self.btn_back, 0, wx.ALL|wx.EXPAND, 3)

		com_backChoices = [ u"No Background" ]
		self.com_back = wx.ComboBox( self, wx.ID_ANY, u"No Background", wx.DefaultPosition, wx.DefaultSize, com_backChoices, wx.CB_READONLY)
		self.com_back.SetSelection( 0 )
		sizer_mode.Add( self.com_back, 1, wx.ALL, 3 )
		
		com_modeChoices = [ u"None", u"Max", u"Min", u"Mask", u"2-8mix", u"4-6mix", u"5-5mix", u"6-4mix", u"8-2mix" ]
		self.com_mode = wx.ComboBox( self, wx.ID_ANY, u"Min", wx.DefaultPosition, wx.DefaultSize, com_modeChoices, wx.CB_READONLY )
		self.com_mode.SetSelection( 0 )
		sizer_mode.Add( self.com_mode, 0, wx.ALL, 3 )
		
		bSizer1.Add( sizer_mode, 0, wx.EXPAND, 2 )
		#line = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		#txtlut = wx.StaticText( self, wx.ID_ANY, 'Look Up Table', wx.DefaultPosition, wx.DefaultSize)
		#bSizer1.Add( line, 0, wx.EXPAND |wx.ALL, 5 )
		#bSizer1.Add( txtlut, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.sli_high.Bind( wx.EVT_SCROLL, self.on_low )
		self.sli_low.Bind( wx.EVT_SCROLL, self.on_high )
		self.btn_r.Bind( wx.EVT_BUTTON, lambda e: self.on_rgb(e, 'r') )
		self.btn_g.Bind( wx.EVT_BUTTON, lambda e: self.on_rgb(e, 'g') )
		self.btn_b.Bind( wx.EVT_BUTTON, lambda e: self.on_rgb(e, 'b') )
		self.btn_gray.Bind( wx.EVT_BUTTON, self.on_gray)
		# self.btn_back.Bind( wx.EVT_LEFT_DOWN, self.on_back)
		self.com_r.Bind( wx.EVT_COMBOBOX, lambda e: self.on_chan(e, 'r'))
		self.com_g.Bind( wx.EVT_COMBOBOX, lambda e: self.on_chan(e, 'g'))
		self.com_b.Bind( wx.EVT_COMBOBOX, lambda e: self.on_chan(e, 'b'))
		self.com_back.Bind( wx.EVT_COMBOBOX, self.on_setback)
		self.com_mode.Bind( wx.EVT_COMBOBOX, self.on_mode)
		self.btn_8bit.Bind( wx.EVT_BUTTON, self.on_8bit )
		self.btn_minmax.Bind( wx.EVT_BUTTON, lambda e: self.on_p(e, 1))
		self.btn_90.Bind( wx.EVT_BUTTON, lambda e: self.on_p(e, 0.9))
		self.btn_95.Bind( wx.EVT_BUTTON, lambda e: self.on_p(e, 0.95))
		self.btn_99.Bind( wx.EVT_BUTTON, lambda e: self.on_p(e, 0.99))
		self.com_back.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.on_back)
		self.active = 0
	
	def on_back(self, event):
		self.com_back.SetItems(['None']+self.app.img_names())
		cur = self.app.get_img_win()
		if not cur is None: cur = cur.back
		if not cur is None: cur = cur.title
		self.com_back.SetValue(str(cur))
		modes = ['set', 'max', 'min', 'msk', 0.2, 0.4, 0.5, 0.6, 0.8]
		ips = self.app.get_img()
		if ips is None: self.com_mode.Select(0)
		else: self.com_mode.Select(modes.index(ips.mode))

	def on_setback(self, event):
		name = self.com_back.GetValue()
		if name is None: return
		self.app.get_img().back = self.app.get_img(name)
		self.app.get_img().update()

	def on_mode(self, event):
		ips = self.app.get_img()
		if ips is None: return
		modes = ['set', 'max', 'min', 'msk', 0.2, 0.4, 0.5, 0.6, 0.8]
		ips.mode = modes[self.com_mode.GetSelection()]
		ips.update()

	# Virtual event handlers, overide them in your derived class
	def on_low( self, event ):
		ips = self.app.get_img()
		if ips is None: return
		if self.sli_low.GetValue()>self.sli_high.GetValue():
			self.sli_high.SetValue(self.sli_low.GetValue())
		rg = (self.sli_low.GetValue(), self.sli_high.GetValue())
		ips.rg[self.active] = rg
		minv, maxv = self.sli_low.min, self.sli_high.max
		lim1 = 1.0 * (self.sli_low.GetValue() - minv)/(maxv-minv)
		lim2 = 1.0 * (self.sli_high.GetValue() - minv)/(maxv-minv)
		self.histpan.set_lim(lim1*255, lim2*255)
		ips.update()
	
	def on_high( self, event ):
		ips = self.app.get_img()
		if ips is None: return
		if self.sli_low.GetValue()>self.sli_high.GetValue():
			self.sli_low.SetValue(self.sli_high.GetValue())
		rg = (self.sli_low.GetValue(), self.sli_high.GetValue())
		ips.rg[self.active] = rg
		minv, maxv = self.sli_low.min, self.sli_high.max
		lim1 = 1.0 * (self.sli_low.GetValue() - minv)/(maxv-minv)
		lim2 = 1.0 * (self.sli_high.GetValue() - minv)/(maxv-minv)
		self.histpan.set_lim(lim1*255, lim2*255)
		ips.update()
	
	def on_rgb( self, event, color):
		ips = self.app.get_img()
		if ips is None: return
		if isinstance(ips.cn, int):
			ips.cn = [0, 1, 2]
		chs = ['C:%d'%i for i in range(ips.channels)]
		for i in (self.com_r, self.com_g, self.com_b):
			chn = i.GetValue()
			i.SetItems(chs)
			idx = chs.index(chn) if chn in chs else 0
			i.Select(idx)
		chanred = ips.cn['rgb'.index(color)]
		chanrg = ips.rg[chanred]
		rg = ips.get_updown('all', chanred, 512)
		if (rg[0]==rg[1]): rg = (rg[0]-1e-4, rg[1]+1e-4)
		slis = 'all' if self.chk_stack.GetValue() else ips.cur
		hist = ips.histogram(rg, slis, chanred, 512)
		self.histpan.SetValue(hist)
		self.sli_low.set_para(rg, 10)
		self.sli_high.set_para(rg, 10)
		self.sli_low.SetValue(chanrg[0])
		self.sli_high.SetValue(chanrg[1])
		self.active = ips.cn['rgb'.index(color)]
		self.range = chanrg
		lim1 = (chanrg[0]-rg[0])/(rg[1]-rg[0])
		lim2 = (chanrg[1]-rg[0])/(rg[1]-rg[0])
		self.histpan.set_lim(lim1*255, lim2*255)
		ips.update()

	def on_gray(self, event):
		ips = self.app.get_img()
		if ips is None: return
		if not isinstance(ips.cn, int): ips.cn = 0
		chanrg = ips.rg[ips.cn]
		rg = ips.get_updown('all', ips.cn, 512)
		if (rg[0]==rg[1]): rg = (rg[0]-1e-4, rg[1]+1e-4)
		slis = 'all' if self.chk_stack.GetValue() else ips.cur
		hist = ips.histogram(rg, slis, ips.cn, 512)
		self.histpan.SetValue(hist)
		self.sli_low.set_para(rg, 10)
		self.sli_high.set_para(rg, 10)
		self.sli_low.SetValue(chanrg[0])
		self.sli_high.SetValue(chanrg[1])
		self.active = ips.cn
		lim1 = (chanrg[0]-rg[0])/(rg[1]-rg[0])
		lim2 = (chanrg[1]-rg[0])/(rg[1]-rg[0])
		self.histpan.set_lim(lim1*255, lim2*255)
		ips.update()

	def on_chan(self, event, color):
		ips = self.app.get_img()
		if ips is None: return
		C = (self.com_r, self.com_g, self.com_b)
		host = C['rgb'.index(color)]
		chnidx = host.GetSelection()
		ips.cn['rgb'.index(color)] = chnidx
		self.on_rgb(event, color)

	def on_8bit(self, event):
		ips = self.app.get_img()
		if ips is None: return
		rg = (0,255)
		ips.rg[self.active] = rg
		if (rg[0]==rg[1]): rg = (rg[0]-1e-4, rg[1]+1e-4)
		slis = 'all' if self.chk_stack.GetValue() else ips.cur
		hist = ips.histogram(rg, slis, self.active, 512)
		self.histpan.SetValue(hist)
		self.sli_low.set_para(rg, 10)
		self.sli_high.set_para(rg, 10)
		self.sli_low.SetValue(rg[0])
		self.sli_high.SetValue(rg[1])
		self.histpan.set_lim(0, 255)
		ips.update()

	def on_p(self, event, k):
		ips = self.app.get_img()
		if ips is None: return
		rg = ips.get_updown('all', self.active, 512)
		if (rg[0]==rg[1]): rg = (rg[0]-1e-4, rg[1]+1e-4)
		slis = 'all' if self.chk_stack.GetValue() else ips.cur
		hist = ips.histogram(rg, slis, self.active, 512)
		msk = np.abs(np.cumsum(hist)/hist.sum()-0.5)<k/2
		idx = np.where(msk)[0]
		vs = np.array([idx.min(), idx.max()])
		vs = vs*(rg[1]-rg[0])/255+rg[0]
		ips.rg[self.active] = tuple(vs)
		self.histpan.SetValue(hist)
		self.sli_low.set_para(rg, 10)
		self.sli_high.set_para(rg, 10)
		self.sli_low.SetValue(vs[0])
		self.sli_high.SetValue(vs[1])
		lim1 = (vs[0]-rg[0])/(rg[1]-rg[0])
		lim2 = (vs[1]-rg[0])/(rg[1]-rg[0])
		self.histpan.set_lim(lim1*255, lim2*255)
		ips.update()