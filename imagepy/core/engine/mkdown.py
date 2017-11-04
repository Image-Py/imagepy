from imagepy import IPy

class MkDown:
	def __init__(self, title, cont, url=''):
		self.title = title
		self.cont = cont

	def __call__(self): return self

	def run(self): IPy.show_md(self.title, self.cont)

	def start(self, para=None, callafter=None): self.run()

if __name__ == '__main__':
	app = wx.App()
	show_help('title', 'abc', '')
	app.MainLoop()