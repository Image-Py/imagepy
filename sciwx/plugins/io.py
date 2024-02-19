from sciapp.action import SciAction, ImgAction
from skimage.io import imread, imsave

class Open(SciAction):
	name = 'Open'
	def start(self, app, para=None):
		path = app.get_path('Open', ['png','bmp','jpg'], 'open')
		if path is None: return
		app.show_img(imread(path))

class Save(ImgAction):
	name = 'Save'
	para = {'path':''}

	def show(self):
		path = self.app.get_path('Open', ['png','bmp','jpg'], 'save')
		if path is None: return
		self.para['path'] = path
		return True

	def run(self, ips, img, snap, para):
		imsave(para['path'], img)