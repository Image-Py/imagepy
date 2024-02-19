import wx

def alert(info, title='SciWx'):
	dialog=wx.MessageDialog(None, info, title, wx.OK)
	dialog.ShowModal() == wx.ID_OK
	dialog.Destroy()

def get_path(title, filt, io, name=''):
	filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in filt])
	dic = {'open':wx.FD_OPEN, 'save':wx.FD_SAVE}
	dialog = wx.FileDialog(None, title, '', name, filt, dic[io])
	rst = dialog.ShowModal()
	path = dialog.GetPath() if rst == wx.ID_OK else None
	dialog.Destroy()
	return path

if __name__ == '__main__':
	app = wx.App()
	frame = wx.Frame(None)
	frame.Show()

	frame2 = wx.Frame(None)
	frame2.Show()

	path = get_path('file', ['png','bmp'], 'save')
	print(path)
	app.MainLoop()