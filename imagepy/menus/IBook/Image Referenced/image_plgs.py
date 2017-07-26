from imagepy import IPy, root_dir
from imagepy.core.engine import Free
from scipy.misc import imread
import os

class Data(Free):
	def __init__(self, name):
		self.name = name
		self.title = name.split('.')[0]

	def run(self, para = None):
		name = 'menus/IBook/Image Referenced/'+self.name
		img = imread(os.path.join(root_dir, name))
		if img.ndim==3 and img.shape[2]==4:
			img = img[:,:,:3].copy()
		IPy.show_img([img], self.title)

	def __call__(self):
		return self

datas = ['Angkor.jpg','qrcode.png','street.jpg','road.jpg','house.jpg',
'neubauer.jpg','windmill.jpg','sunglow.jpg', 'UK.jpg']

plgs = [Data(i) for i in datas]