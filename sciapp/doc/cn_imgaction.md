# ImageAction

App是科学应用容器，具备各种数据类型的展示，关闭功能，并对其进行管理。SciAction是对app对象的某种操作，而后续SciApp功能的丰富，主要就是依赖于Action的丰富。



### 原始SciAction

SciAction是对app对象的某种操作，接口函数非常简单，只有一个 **start(self, app, para)**，你可以在start内对app对象进行各种操作。而原始的SciApp只是用app对象弹出了一个提示。

```python
class SciAction:
    '''base action, just has a start method, alert a hello'''
    name = 'SciAction'

    def start(self, app, para=None): 
        self.app = app
        app.alert('Hello, I am SciAction!\n')
        
app = App()
SciAction().start(app)
```



### 用SciAction实现滤波

这里我们在start内，获取当前图像，并对其进行一个sigma为5的高斯滤波

```python
class GaussianAction1(SciAction):
    name = 'GaussianAction1'

    def start(self, app, para=None): 
        image = app.get_img()
        image.img[:] = gaussian_filter(image.img, 5)
        
app = App()
from skimage.data import camera
app.show_img([camera()], 'camera')
GaussianAction1().start(app)
```



### 带参数交互的滤波

这里我们使用app.show_para来和用户进行交互，获取参数。当然，这个例子中，我们可以使用python自带的input函数，然而app对象作为通用接口，我们在action中进来使用通用函数，以便在App对象的界面实现中依然可以使用。

```python
class GaussianAction3(SciAction):
    name = 'GaussianAction3'

    def start(self, app, para=None): 
        image = app.get_img()
        para = {'sigma':5}
        view = [(int, 'sigma', (0,30), 0, 'sigma', 'px')]
        app.show_para('GaussianAction3', para, view)
        image.img[:] = gaussian_filter(image.img, para['sigma'])
        
app = App()
from skimage.data import camera
app.show_img([camera()], 'camera')
GaussianAction3().start(app)
```



### 参数标准化分离

在上一个例子的基础上，我们将para，view提升为类变量，把滤波函数提出来，定义为run函数，这样做的好处是，start部分就相对固定化了。

```python
class GaussianAction4(SciAction):
    name = 'GaussianAction4'
    para = {'sigma':5}
    view = [(int, 'sigma', (0,30), 0, 'sigma', 'px')]

    def run(self, img, para):
        img[:] = gaussian_filter(img, para['sigma'])

    def start(self, app, para=None): 
        image = app.get_img()        
        app.show_para(self.name, self.para, self.view)
        self.run(image.img, self.para)
        
app = App()
from skimage.data import camera
app.show_img([camera()], 'camera')
GaussianAction4().start(app)
```



### ImageAction 初步版

上一个版本已经非常完善，我们把具体功能移除，形成一个抽象版的ImageAction，start内做如下事情：

1. 获取当前图像，如果没有打开图像则弹出提示，终止后续
2. 判断是否有参数，如果有则调用show_para进行交互
3. 将当前图像和交互完成后的para送入run进行处理

```python
class ImageAction(SciAction):
    name = 'ImageAction'
    para, view = None, None

    def run(self, img, para=None):pass

    def start(self, app, para=None): 
        image = app.get_img()
        if image is None: return app.alert('no image!')
        if self.para != None:
            app.show_para(self.name, self.para, self.view)
        self.run(image.img, self.para)
```

现在我们的Gaussian滤波器写成了这样，只需继承ImageAction，定义para，view，然后重载run函数即可。

```python
class Gaussian(ImageAction):
    '''now a gaussian filter should be like this'''
    name = 'Gaussian'
    para = {'sigma':5}
    view = [(int, 'sigma', (0,30), 0, 'sigma', 'px')]

    def run(self, img, para):
        img[:] = gaussian_filter(img, para['sigma'])
        
app = App()
from skimage.data import camera
app.show_img([camera()], 'camera')
Gaussian().start(app)
```

**备注：**本章只是为了讲解Action如何作用，并且如何通过逐层继承，使得Action子类分化出越来越具体的功能，但并不是说我们需要按照这里的方法从底层搭建Action，况且这里的ImageAction依然不够完善，比如可以继续添加图像类型的判定，多线程支持等。好在advanced里面已经定义好了更为丰富的Action模板，我们可以直接继承高级模板。

