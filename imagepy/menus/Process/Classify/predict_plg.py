from sciapp.action import Simple
from sciapp.object import Image
from glob import glob
import os.path as osp
import joblib
from imagepy.ipyalg import feature
from imagepy import root_dir

class Plugin(Simple):
	title = 'Feature Predictor'
	note = ['all']

	para = {'predictor':None, 'slice':False}
	view = [(list, 'predictor', [''], str, 'predictor', ''),
			(bool, 'slice', 'slice')]

	def __init__(self, ips=None, path=''):
		Simple.__init__(self)
		self.model = None
		self.root = osp.join(root_dir, 'data/ilastik')
		fs = glob(osp.join(self.root, '*.fcl'))
		fs = [osp.split(i)[1] for i in fs]
		if '/' in path: fs = [path]
		if len(fs) == 0: return self.app.alert('No feature classfier found!')
		self.para['predictor'] = fs[0]
		self.view[0] = (list, 'predictor', fs, str, 'predictor', '')
		

	def run(self, ips, imgs, para=None):
		if '/' in para['predictor']: path = para['predictor']
		else: path = self.root+'/'+para['predictor']
		model, key = joblib.load(path)
		if not para['slice']: imgs = [ips.img]
		slir, slic = ips.rect
		imgs = [i[slir, slic] for i in imgs]
		rst = feature.get_predict(imgs, model, key, callback=self.progress)
		if rst is None:
			return self.app.alert('image channels dismatch this predictor!')
		ips = Image(rst, ips.title+'-mark')
		ips.range = ips.get_updown('all', 'one', step=512)
		self.app.show_img(ips)