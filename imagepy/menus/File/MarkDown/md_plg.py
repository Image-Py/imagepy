from imagepy.core.engine import dataio
from sciapp import Source

def read(path):
	with open(path) as f: return f.read()

Source.manager('reader').add('md', read, 'md')

class Plugin(dataio.Reader):
	title = 'MarkDown Open'
	tag = 'md'
	filt = ['MD']