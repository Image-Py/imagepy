from imagepy.core.util import fileio
from scipy.io import savemat, loadmat
from sciapp import Source
import os

Source.manager('reader').add('mat', lambda path: loadmat(path)['img'], 'img')
Source.manager('writer').add('mat', lambda path, img: savemat(path, {'img':img}), 'img')
Source.manager('reader').add('mat', lambda path: loadmat(path)['img'], 'imgs')
Source.manager('writer').add('mat', lambda path, img: savemat(path, {'img':img}), 'imgs')

class OpenFile(fileio.Reader):
	title = 'Mat Open'
	tag = 'img'
	filt = ['Mat']

class SaveFile(fileio.ImageWriter):
	title = 'Mat Save'
	tag = 'img'
	filt = ['Mat']

class Open3D(fileio.Reader):
	title = 'Mat 3D Open'
	tag = 'imgs'
	filt = ['Mat']

class Save3D(fileio.ImageWriter):
	title = 'Mat 3D Save'
	tag = 'imgs'
	filt = ['Mat']
	note = ['8-bit', 'rgb', 'stack']

plgs = [OpenFile, SaveFile, '-', Open3D, Save3D]