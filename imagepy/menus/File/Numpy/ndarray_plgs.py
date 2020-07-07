from sciapp.action import dataio
import numpy as np
import os

dataio.ReaderManager.add('npy', np.load, 'img')
dataio.WriterManager.add('npy', np.save, 'img')
dataio.ReaderManager.add('npy', np.load, 'imgs')
dataio.WriterManager.add('npy', np.save, 'imgs')

class OpenFile(dataio.Reader):
	title = 'Numpy Open'
	tag = 'img'
	filt = ['npy']

class SaveFile(dataio.ImageWriter):
	title = 'Numpy Save'
	tag = 'img'
	filt = ['npy']

class Open3D(dataio.Reader):
	title = 'Numpy 3D Open'
	tag = 'imgs'
	filt = ['npy']

class Save3D(dataio.ImageWriter):
	title = 'Numpy 3D Save'
	tag = 'imgs'
	filt = ['npy']
	note = ['all', 'stack']

plgs = [OpenFile, SaveFile, '-', Open3D, Save3D]