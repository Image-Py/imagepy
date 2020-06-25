from imagepy.core.engine import dataio
from scipy.io import savemat, loadmat
from sciapp import Source
import os

Source.manager('reader').add('mat', lambda path: loadmat(path)['img'], 'img')
Source.manager('writer').add('mat', lambda path, img: savemat(path, {'img':img}), 'img')
Source.manager('reader').add('mat', lambda path: loadmat(path)['img'], 'imgs')
Source.manager('writer').add('mat', lambda path, img: savemat(path, {'img':img}), 'imgs')

class OpenFile(dataio.Reader):
	title = 'Mat Open'
	tag = 'img'
	filt = ['Mat']

class SaveFile(dataio.ImageWriter):
	title = 'Mat Save'
	tag = 'img'
	filt = ['Mat']

class Open3D(dataio.Reader):
	title = 'Mat 3D Open'
	tag = 'imgs'
	filt = ['Mat']

class Save3D(dataio.ImageWriter):
	title = 'Mat 3D Save'
	tag = 'imgs'
	filt = ['Mat']
	note = ['8-bit', 'rgb', 'stack']

plgs = [OpenFile, SaveFile, '-', Open3D, Save3D]