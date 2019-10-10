from imagepy.core.engine import Simple
from imagepy.core import ImagePlus
from imagepy import IPy
from glob import glob
import os.path as osp
import joblib
from .features import get_feature, get_predict
from imagepy.core.manager import ReaderManager, ViewerManager

class Plugin(Simple):
	title = 'Feature Predictor'
	note = ['all']

	para = {'predictor':None, 'slice':False}
	view = [(list, 'predictor', [''], str, 'predictor', ''),
			(bool, 'slice', 'slice')]

	def __init__(self, ips=None, path=''):
		Simple.__init__(self, ips)
		self.model = None
		self.root = osp.join(IPy.root_dir, 'data/ilastik')
		fs = glob(osp.join(self.root, '*.fcl'))
		fs = [osp.split(i)[1] for i in fs]
		if path != '': 
			self.root = ''
			fs = [path]
		
		if len(fs) == 0: return IPy.alert('No feature classfier found!')
		self.para['predictor'] = fs[0]
		self.view[0] = (list, 'predictor', fs, str, 'predictor', '')
		

	def run(self, ips, imgs, para=None):
		if '/' in para['predictor']: path = para['predictor']
		else: path = self.root+'/'+para['predictor']
		model, key = joblib.load(path)
		lut = {'ori':1, 'blr':key['grade'], 'sob':key['grade'], 'eig':key['grade']*2}
		if sum([lut[i] for i in key['items']])*ips.channels != len(key['titles']):
			return IPy.alert('image channels dismatch this predictor!')
		if not para['slice']: imgs = [ips.img]
		rst = []
		for i in range(len(imgs)):
			self.progress(i+1, len(imgs))
			rst.append(get_predict(imgs[i], model, key))
		ips = ImagePlus(rst, ips.title+'-mark')
		ips.range = ips.get_updown('all', 'one', step=512)
		IPy.show_ips(ips)