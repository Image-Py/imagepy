from imagepy.core.engine import Filter, Simple
from imagepy import IPy
from pystackreg import StackReg
import numpy as np
import pandas as pd
from skimage import transform as tf
from imagepy.core.manager import TableManager

class Register(Simple):
	title = 'Stack Register'
	note = ['8-bit', '16-bit', 'int', 'float', 'stack']

	para = {'trans':'RIGID_BODY', 'ref':'previous', 'tab':False, 'new':'Inplace'}
	view = [(list, 'trans', ['TRANSLATION', 'RIGID_BODY', 'SCALED_ROTATION', 'AFFINE', 'BILINEAR'], str,  'transform', ''),
			(list, 'ref', ['previous', 'first', 'mean'], str, 'image', ''),
			(list, 'new', ['Inplace', 'New', 'None'], str, 'reference', ''),
			(bool, 'tab', 'show table')]

	def run(self, ips, imgs, para = None):
		news = np.array(imgs)
		sr = StackReg(eval('StackReg.%s'%para['trans']))
		sr.register_stack(news, reference=para['ref'])
		mats = sr._tmats.reshape((sr._tmats.shape[0],-1))
		if para['tab']: IPy.show_table(pd.DataFrame(
			mats, columns=['A%d'%(i+1) for i in range(mats.shape[1])]), title='%s-Tmats'%ips.title)
		if para['new'] == 'None': return
		for i in range(sr._tmats.shape[0]):
			tform = tf.ProjectiveTransform(matrix=sr._tmats[i])
			if para['new'] == 'Inplace':
				imgs[i] = tf.warp(imgs[i], tform)*imgs[i].max()
			if para['new'] == 'New':
				news[i] = tf.warp(imgs[i], tform)*imgs[i].max()
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
		for i in range(len(mats)):
			tform = tf.ProjectiveTransform(matrix=mats[i].reshape((3,3)))
			img = tf.warp(imgs[i], tform)
			img -= imgs[i].min(); img *= imgs[i].max() - imgs[i].min()
			if para['new']: newimgs.append(img)
			else: imgs[i] = img
		if para['new']: IPy.show_img(newimgs, '%s-trans'%ips.title)

plgs = [Register, Transform]