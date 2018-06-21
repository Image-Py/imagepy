from imagepy.core.engine import Table, Simple
from imagepy.core.manager import TableManager
from imagepy.core.manager import ImageManager

# 图像拼接函数
def combine_image(img1, img2, matrix):
	pass

# 从特征计算变换矩阵
def count_matrix(pts1, feats1, pts2, feats2):
	pass

# 计算变换矩阵插件
class CountMatrix(Table):
	title = 'Count Transform From Feats'
	para = {'feats1':None, 'feats2':None}
	view = [('tab', 'feats1', 'features set 1', ''),
			('tab', 'feats2', 'features set 2', '')]

	def run(self, tps, data, snap, para = None):
		tps1 = TableManager.get(para['feats1'])
		tps2 = TableManager.get(para['feats2'])
		# tps1.data, tps2.data 可以拿到pandas.dataframe对象
		# IPy.show_table(count_matrix(...

class CombineImage(Simple):
	title = 'Combine Images By Matrix'
	note = ['all']
	para = {'img1':None, 'img2':None, 'mat':None}
	view = [('img', 'img1', 'first image', ''),
			('img', 'img2', 'second image', ''),
			('tab', 'feats2', 'features set 2', '')]

	def run(self, ips, imgs, para = None):
		ips1 = ImageManager.get(para['img1'])
		ips2 = ImageManager.get(para['img2'])
		tps = TableManager.get(para['mat'])

		# IPy.show_img(combine_image(...)

plgs = [CountMatrix, CombineImage]
