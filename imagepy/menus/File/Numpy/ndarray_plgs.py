from imagepy.core.util import fileio
import numpy as np
from imagepy.core.manager import ReaderManager, WriterManager
from imagepy import IPy
import os

ReaderManager.add('npy', np.load)
WriterManager.add('npy', np.save)

class OpenFile(fileio.Reader):
	title = 'Numpy Open'
	filt = ['npy']

class SaveFile(fileio.Writer):
	title = 'Numpy Save'
	filt = ['npy']

class Open3D(fileio.Reader):
	title = 'Numpy 3D Open'
	filt = ['npy']

	def run(self, para = None):
		imgs = np.load(para['path'])
		fp, fn = os.path.split(para['path'])
		fn, fe = os.path.splitext(fn) 
		IPy.show_img(imgs, fn)

class Save3D(fileio.Writer):
	title = 'Numpy 3D Save'
	filt = ['npy']
	note = ['all', 'stack']

	def run(self, ips, imgs, para = None):
		np.save(para['path'], imgs)

plgs = [OpenFile, SaveFile, '-', Open3D, Save3D]