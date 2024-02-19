# IOAction

继上一篇ImageAction之后，其实可以类似的拓展到TableAction，然而上一篇的例子中的图像，我们都是利用代码show，进而载入到app中的，本章我们就来编写数据读写的IOAction。



### 原始实现

我们在start内部获取用户输入的路径，然后解析出文件名和扩展名，调用app.show_img进行展示

```python
from skimage.io import imread

class ImageReader1(SciAction):
    '''read a image and show it'''
    name = 'ImageReader1'

    def start(self, app, para=None):
        path = input('input the file path, or just a.png for test:')
        name, ext = osp.splitext(osp.split(path)[1])
        app.show_img([imread(path)], name)
        
app = App()
ImageReader1().start(app)
```



### 支持多种格式数据

这个例子我们通过扩展名对读取方法进行管理，放入ReadManager，这样当添加新的读取格式时，只需将扩展名和读取方法加入ReaderManager。同样我们这里使用了get_path函数来获取路径，这同样是为了后续界面版本的App可以通用。

```python
from skimage.io import imread
ReaderManager = Manager()

class ImageReader(SciAction):
    name = 'ImageReader'

    def start(self, app, para=None):
        # input the file path, or just a.png for test
        path = app.get_path()
        name, ext = osp.splitext(osp.split(path)[1])
        reader = ReaderManager.get(ext[1:])
        if reader is None:
            return app.alert('no reader for %s!'%ext[1:])
        app.show_img([reader(path)], name)

ReaderManager.add('png', imread)
ReaderManager.add('jpg', imread)
# ReaderManager.add('dcm', read_dicom) other format

app = App()
ImageReader().start(app)
```



### ImageWriter

保存操作和打开类似，不同的是需要获取当前图像，其实某种意义上，可以当作一个ImageAction。

```python
from skimage.io import imsave
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
```



**备注：**本章只是为了讲解Action如何作用，并且如何通过逐层继承，使得Action子类分化出越来越具体的功能，但并不是说我们需要按照这里的方法从底层搭建Action，况且这里的IOAction依然不够完善，具体我们可以直接使用advanced.dataio模板。

