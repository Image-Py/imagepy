from sciapp.action import Filter, Simple
from pystackreg import StackReg
import numpy as np
import pandas as pd
from skimage import transform as tf
import scipy.ndimage as ndimg

class Register(Simple):
	title = 'Stack Register'
	note = ['8-bit', '16-bit', 'int', 'float', 'stack']

	para = {'trans':'RIGID_BODY', 'ref':'previous', 'tab':False, 'new':'Inplace', 'diag':0, 'sigma':0}
	view = [(list, 'trans', ['TRANSLATION', 'RIGID_BODY', 'SCALED_ROTATION', 'AFFINE', 'BILINEAR'], str,  'transform', ''),
			(list, 'ref', ['previous', 'first', 'mean'], str, 'reference', ''),
			(list, 'new', ['Inplace', 'New', 'None'], str, 'image', ''),
			(int, 'diag', (0, 2048), 0, 'diagonal', 'scale'),
			(float, 'sigma', (0,30), 1, 'sigma', 'blur'),
			(bool, 'tab', 'show table')]

	def run(self, ips, imgs, para = None):
		k = para['diag']/np.sqrt((np.array(ips.img.shape)**2).sum())
		size = tuple((np.array(ips.img.shape)*k).astype(np.int16))
		IPy.info('down sample...')
		news = []
		for img in imgs:
			if k!=0: img = tf.resize(img, size)
			if para['sigma']!=0:
				img = ndimg.gaussian_filter(img, para['sigma'])
			news.append(img)

		IPy.info('register...')
		sr = StackReg(eval('StackReg.%s'%para['trans']))
		sr.register_stack(np.array(news), reference=para['ref'])

		mats = sr._tmats.reshape((sr._tmats.shape[0],-1))
		if k!=0: mats[:,[0,1,3,4,6,7]] *= k
		if k!=0: mats[:,[0,1,2,3,4,5]] /= k

		if para['tab']: IPy.show_table(pd.DataFrame(
			mats, columns=['A%d'%(i+1) for i in range(mats.shape[1])]), title='%s-Tmats'%ips.title)

		if para['new'] == 'None': return
		IPy.info('transform...')
		for i in range(sr._tmats.shape[0]):
			tform = tf.ProjectiveTransform(matrix=sr._tmats[i])
			img =  tf.warp(imgs[i], tform)
			img -= imgs[i].min(); img *= imgs[i].max() - imgs[i].min()
			if para['new'] == 'Inplace': imgs[i][:] = img
			if para['new'] == 'New': news[i] = img.astype(ips.img.dtype)
			self.progress(i, len(imgs))
		if para['new'] == 'New': IPy.show_img(news, '%s-reg'%ips.title)

class Transform(Simple):
	title = 'Register By Mats'
	note = ['all']

	para = {'mat':None, 'new':True}
	view = [('tab', 'mat', 'transfrom', 'matrix'),
			(bool, 'new', 'new image')]

	def run(self, ips, imgs, para = None):
		mats = TableManager.get(para['mat']).data.values
		if len(imgs) != len(mats):
			IPy.alert('image stack must has the same length as transfrom mats!')
			return
		newimgs = []
		img = np.zeros_like(ips.img, dtype=np.float64)
		for i in range(len(mats)):
			tform = tf.ProjectiveTransform(matrix=mats[i].reshape((3,3)))
			if imgs[i].ndim==2: 
				img[:] = tf.warp(imgs[i], tform)
			else:
				for c in range(img.shape[2]):
					img[:,:,c] = tf.warp(imgs[i][:,:,c], tform)
			img -= imgs[i].min(); img *= imgs[i].max() - imgs[i].min()
			if para['new']: newimgs.append(img.astype(ips.img.dtype))
			else: imgs[i] = img
			self.progress(i, len(mats))
		if para['new']: IPy.show_img(newimgs, '%s-trans'%ips.title)

plgs = [Register, Transform]