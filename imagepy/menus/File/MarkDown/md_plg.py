from sciapp.action import dataio

def read(path):
	with open(path) as f: return f.read()

dataio.ReaderManager.add('md', read, 'md')

class Plugin(dataio.Reader):
	title = 'MarkDown Open'
	tag = 'md'
	filt = 'MD'