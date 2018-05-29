import wx

class NumCtrl(wx.TextCtrl):
	def __init__(self, parent):
		wx.TextCtrl.__init__(self, parent, -1, 'text')

	def Bind(self, f):self.f = f

	def __del__( self ): print('text ctrl deleted!')

class ParaDialog (wx.Dialog):
    def __init__( self, parent, title):
        wx.Dialog.__init__ (self, parent, -1, title, style = wx.DEFAULT_DIALOG_STYLE)

    def init_view(self): 
    	txtctrl = NumCtrl(self)
    	txtctrl.Bind(self.f)

    def f(self, key): pass

    def __del__( self ): print('panel config deleted!')

class Frame(wx.Frame):
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = 'Test' )

		btn = wx.Button(self, wx.ID_ANY, "abc")
		btn.Bind(wx.EVT_BUTTON, self.show)

	def show(self, event):
		with ParaDialog(self, 'Dialog') as dialog:
			dialog.init_view()
			dialog.ShowModal()

	def __del__(self): print('form delete')

if __name__ == '__main__':
	app = wx.App(False)
	frame = Frame(None)
	frame.Show()
	app.MainLoop()