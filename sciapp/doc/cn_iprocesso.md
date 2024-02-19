# Process Demo

我们这里用一个具体的例子，演示如何读取图像，滤波处理，保存图像。我们结合前两节的内容，



### IO操作

如同前一节，我们添加ImageReader, ImageWriter。

```python
from sciapp import App, Manager
from sciapp.action import SciAction
import os.path as osp
from skimage.io import imread, imsave
from skimage.data import camera
from scipy.ndimage import gaussian_filter

ReaderManager = Manager()
ReaderManager.add('png', imread)

class ImageReader(SciAction):
    '''supporting different image format'''
    name = 'ImageReader'

    def start(self, app, para=None):
        path = input('input the file path, or just a.png for test:')
        name, ext = osp.splitext(osp.split(path)[1])
        reader = ReaderManager.get(ext[1:])
        if reader is None:
            return app.alert('no reader for %s!'%ext[1:])
        app.show_img([reader(path)], name)

WriterManager = Manager()
WriterManager.add('png', imsave)

class ImageWriter(SciAction):
    '''write current image'''
    name = 'ImageWriter'

    def start(self, app, para=None):
        img = app.get_img()
        if img is None: return app.alert('no image')
        path = input('input the file path to save:')
        name, ext = osp.splitext(osp.split(path)[1])
        writer = WriterManager.get(ext[1:])
        if writer is None: 
            return app.alert('no writer for %s!'%ext[1:])
        writer(path, img.img)
```



### Gaussian滤镜

如同前一节，我们添加Gaussian滤波器。然后我们依次start三个Action，按照提示，输入读取图像路径，高斯滤波sigma，输出图像路径，最后完成。

```python
class ImageAction(SciAction):
    name = 'ImageAction'
    para, view = None, None

    def run(self, img, para):pass

    def start(self, app, para=None): 
        image = app.get_img()
        if image is None: return app.alert('no image!')
        if self.para != None:
            app.show_para(self.name, self.para, self.view)
        self.run(image.img, self.para)

class Gaussian(ImageAction):
    '''now a gaussian filter should be like this'''
    name = 'Gaussian'
    para = {'sigma':5}
    view = [(int, 'sigma', (0,30), 0, 'sigma', 'px')]

    def run(self, img, para):
        img[:] = gaussian_filter(img, para['sigma'])


app = App()
ImageReader().start(app)
Gaussian().start(app)
ImageWriter().start(app)

# >>> input the file path, or just a.png for test:camera.png
# >>> UINT8  512x512  S:1/1  C:0/1  0.25M
# >>> sigma: ? px <int> 5
# >>> input the file path to save:blur.png
```

**备注：**本章只是为了讲解Action如何作用，并且如何通过逐层继承，使得Action子类分化出越来越具体的功能，但并不是说我们需要按照这里的方法从底层搭建Action，况且这里的IOAction依然不够完善，具体我们可以直接使用advanced.dataio模板。

