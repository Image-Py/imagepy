from sciapp.action import Free
import time, wx, numpy as np

class Plugin(Free):
	title = 'Screen Capture'
	para = {'delay':1}
	view = [(int, 'delay', (1,10), 0, 'delay', 's')]

	def run(self, para = None):
		for i in range(5):
			self.progress(i, 5)
			time.sleep(para['delay']/5)
		screen = wx.ScreenDC()
		size = screen.GetSize()
		bmp = wx.Bitmap(size[0], size[1])
		mem = wx.MemoryDC(bmp)
		mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
		arr = np.zeros((size[1], size[0], 3), dtype=np.uint8)
		bmp.CopyToBuffer(arr)
		self.app.show_img([arr], 'Screen Capture')