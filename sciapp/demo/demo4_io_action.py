import sys
sys.path.append('../../')

from sciapp import App, Manager
from sciapp.action import SciAction
import os.path as osp
from skimage.io import imread, imsave
from skimage.data import camera
from pandas import read_csv
import pandas as pd
import numpy as np

# overwrite the imread, read_csv, to make the demo works
# you can annotation it, but you need give a true path in this demo
def imread(path): return camera()
def read_csv(path): return pd.DataFrame(np.arange(25).reshape(5,5))

class ImageReader1(SciAction):
    '''read a image and show it'''
    name = 'ImageReader1'

    def start(self, app):
        path = input('input the file path, or just a.png for test:')
        name, ext = osp.splitext(osp.split(path)[1])
        app.show_img([imread(path)], name)

def image_read_demo1():
    app = App()
    ImageReader1().start(app)
    print(app.img_names())

ReaderManager = Manager()

class ImageReader(SciAction):
    '''supporting different image format'''
    name = 'ImageReader'

    def start(self, app):
        # input the file path, or just a.png for test
        path = app.get_path()
        name, ext = osp.splitext(osp.split(path)[1])
        reader = ReaderManager.get(ext[1:])
        if reader is None:
            return app.alert('no reader for %s!'%ext[1:])
        app.show_img([reader(path)], name)

ReaderManager.add('png', imread)
# if you want support other format, just add it to the manager
# ReaderManager.add('dicom', 'xxx')

def image_read_demo2():
    app = App()
    ImageReader().start(app)

class FileReader(SciAction):
    '''supporting different type, image/table or other...'''
    name = 'FileReader'

    def start(self, app):
        # input the file path, or just a.png/a.csv for test
        path = app.get_path()
        name, ext = osp.splitext(osp.split(path)[1])
        readers = ReaderManager.gets(ext[1:])
        if len(readers)!=1:
            return app.alert('no reader or many readers for %s!'%ext[1:])
        else: key, reader, tag = readers[0]
        if tag=='img':app.show_img([reader(path)], name)
        if tag=='tab':app.show_table(reader(path), name)

ReaderManager = Manager()
ReaderManager.add('png', imread, tag='img')
ReaderManager.add('csv', read_csv, tag='tab')

#ReaderManager.add('dicom', 'xxx')

def image_read_demo3():
    app = App()
    FileReader().start(app)
    print('images:', app.img_names(), 'tables:', app.table_names())

WriterManager = Manager()

class ImageWriter(SciAction):
    '''write current image'''
    name = 'ImageWriter'

    def start(self, app):
        img = app.get_img()
        if img is None: return app.alert('no image')
        # input the file path to save
        path = app.get_path()
        name, ext = osp.splitext(osp.split(path)[1])
        writer = WriterManager.get(ext[1:])
        if writer is None: 
            return app.alert('no writer for %s!'%ext[1:])
        writer(path, img.img)

WriterManager.add('png', imsave)

def img_write_demo4():
    app = App()
    FileReader().start(app)
    ImageWriter().start(app)

if __name__ == '__main__':
    image_read_demo1()
    image_read_demo2()
    image_read_demo3()
    img_write_demo4()
