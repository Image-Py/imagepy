from imagepy.core.util import fileio
import numpy as np
from sciapp import Source
import os

Source.manager('reader').add('npy', np.load, 'img')
Source.manager('writer').add('npy', np.save, 'img')
Source.manager('reader').add('npy', np.load, 'imgs')
Source.manager('writer').add('npy', np.save, 'imgs')

class OpenFile(fileio.Reader):
	title = 'Numpy Open'
	tag = 'img'
	filt = ['npy']

class SaveFile(fileio.ImageWriter):
	title = 'Numpy Save'
	tag = 'img'
	filt = ['npy']

class Open3D(fileio.Reader):
	title = 'Numpy 3D Open'
	tag = 'imgs'
	filt = ['npy']

class Save3D(fileio.ImageWriter):
	title = 'Numpy 3D Save'
	tag = 'imgs'
	filt = ['npy']
	note = ['all', 'stack']

plgs = [OpenFile, SaveFile, '-', Open3D, Save3D]