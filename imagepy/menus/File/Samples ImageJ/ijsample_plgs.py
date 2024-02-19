from skimage.io import imread
from urllib.request import urlopen
from io import BytesIO as StringIO

from sciapp.action import Free

class IJImg(Free):
	def __init__(self, title, name):
		self.title, self.name = title, name

	def __call__(self): return self

	def run(self, para = None):
		try:
			response = urlopen('http://imagej.net/images/'+self.name)
			stream = StringIO(response.read())
			img = imread(stream)
			self.app.show_img([img], self.title)
		except Exception as e:
			self.app.write('Open url failed!\tErrof:%s'%sys.exc_info()[1])
        
plgs = [IJImg(*i) for i in [('Leaf 36K', 'leaf.jpg'), ('Lena 68K', 'lena.jpg'), ('MRI Head 47K', 'mri.gif'),
			('AuPbSn 40 56K', 'AuPbSn40.jpg'), ('Blob 356K', 'blobs.gif'), ('Baboon 56K', 'baboon.jpg'),
			('Boats 25K', 'boats.gif'), ('Bridge 174K', 'bridge.gif'), ('Clown 14K', 'clown.jpg'),
			('Lymp 17K', 'lymp.tif'), ('M51 177K', 'm51.jpg'), ('FluorescentCells 400K', 'FluorescentCells.jpg'), 
			('Microm 32K', 'microm.jpg'), ('SmartSEMSample 780K', 'SmartSEMSample.tif'), 
			('NileBend 1.9M', 'NileBend.jpg'), ('Diatoms 60K', 'Diatoms.jpg'),('Tree Rings 48K', 'Tree_Rings.jpg'), 
			('Cartwheel Galaxy 231K', 'Cartwheel_Galaxy.jpg'), ('Cell Colony 34K', 'Cell_Colony.jpg')]]