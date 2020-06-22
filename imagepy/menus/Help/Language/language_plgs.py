from sciapp import Source
from imagepy.core.engine import Free

class Language(Free):
	def __init__(self, key):
		self.title = key
		asyn = False

	def run(self, para = None):
		Source.manager('config').remove('language')
		Source.manager('config').add('language', self.title)
		self.app.load_all()

	def __call__(self):
		return self

plgs = [Language(i) for i in Source.manager('dictionary').get('language')]