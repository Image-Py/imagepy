ImagePy Basic Tutorial   
======================
[https://github.com/yxdragon/imagepy.git](https://github.com/yxdragon/imagepy.git)

**Introduction:**ImagePy is an image processing software developed in Python, supporting bmp, rgb, png and other commonly used image formats. It can handle grayscale images and multi-channel (color) images, and supports image stack (sequence) operations. It supports a variety of selection operations (point, line, surface, multi-line, multi-face, hollow polygon).  It can carry out a variety of commonly used mathematical operations, commonly used filter operation, image measurements, as well as pixel statistics. It can carry on dem surface reconstruction and three-dimensional reconstruction of image sequences. And the framework is based around Python development. The image data is represented by numpy. And thus it can easily access scikit-image, opencv, itk, mayavi and other third-party mature image processing libraries.

Main Interface
--------------
![](http://idoc.imagepy.org/imgs/p1.png "title")  
The main interface consists of four parts, from top to bottom: the title bar, menu bar, toolbar, and status bar. 
Here are a few examples to illustrate what ImagePy can do.

First example: Mathematical operations, filter operations.
--------------------------------------------------------------
<table>
    <tr>
      <td rowspan="2"><img src="http://idoc.imagepy.org/imgs/p2.png"/> </td>
      <td align="center", valign="top"><img src="http://idoc.imagepy.org/imgs/p3.png"/> <br>Original Image</br></td>
      <td align="center", valign="top"><img src="http://idoc.imagepy.org/imgs/p4.png"/> <br>Color Balance</br></td>
    </tr>
    <tr>
      <td align="center", valign="top"><img src="http://idoc.imagepy.org/imgs/p5.png"/><br>Gauss Laplace</br></td>
      <td align="center", valign="top"><img src="http://idoc.imagepy.org/imgs/p6.png"/><br>UnSharp Mask</br></td>
    </tr>
</table>

**Selection Introduction**:
Selection refers to processing the image only in the the specific identification areas on the image. ImagePy supports single point, multi-point, single line, multi-line, rectangular, circular, arbitrary polygon and free curve selection.  It can superimpose something using Shift key, hollow out something using Ctrl key. In addition, all the selection objects can carry out expansion, shrink, convex hull and other geometric operations.

![](http://idoc.imagepy.org/imgs/p10.png "title") ![](http://idoc.imagepy.org/imgs/p11.png "title") ![](http://idoc.imagepy.org/imgs/p12.png "title")  
4)Rectangular selection 5)rectangle + free curve (stroke) 6)free curve (Buffer)  

**Geometric Transformation:**ImagePy supports geometric transformations.  It can carry out rotation, translation and other conventional matrix transformations. What’s more, these rotations are interactive and support selection.  

![](http://idoc.imagepy.org/imgs/p13.png "title") ![](http://idoc.imagepy.org/imgs/p14.png "title") ![](http://idoc.imagepy.org/imgs/p15.png "title")  
1) Image rotation 2)Rotation in circular selection 3)Scaling in circular selection  

Second example: An example of a cell count
----------------------------------------------

**Look up table introduction:**  
![](http://idoc.imagepy.org/imgs/p16.png "title") ![](http://idoc.imagepy.org/imgs/p17.png "title") ![](http://idoc.imagepy.org/imgs/p18.png "title")  
1)Original image 2)red look up table 3)ICA look up table

**Index color** is also called false color. The essence of it is to map the gray color to a predefined spectrum. The index color does not increase the amount of information in the image, but does enhance the visual contrast.

![](http://idoc.imagepy.org/imgs/p19.png "title") ![](http://idoc.imagepy.org/imgs/p20.png "title") ![](http://idoc.imagepy.org/imgs/p21.png "title")  
1)Gaussian Blur 2)USM Sharpen 3)Threshold  
![](http://idoc.imagepy.org/imgs/p22.png "title") ![](http://idoc.imagepy.org/imgs/p23.png "title") ![](http://idoc.imagepy.org/imgs/p24.png "title")  
4)Label, the index color 5)The calculation area centroid 6)Pixel statistics  

Here, for a cell under a microscope, we organize the image and compute statistics.  

1. Open the original image and go on Gaussian blur to anti-noise.  
2. In order to highlight the cells, a large-scale USM mask treatment was performed.  
3. After processing the picture, it is easy to use the threshold function to carry on binarization.  
4. Label the binary image, mark unicom area.  
5. Calculate the centroid of each Unicom area  
6. Calculate the area occupied by each cell  



Third example: Image matching
----------------------------------

Use the Surf feature matching algorithm implemented in OpenCV.
<table>
    <tr>
      <td rowspan="2" valign="top"><img src="http://idoc.imagepy.org/imgs/p25.png"/> </td>
      <td align="center"><img src="http://idoc.imagepy.org/imgs/p26.png"/></td>
    </tr>
    <tr>
      <td align="center">
        <img src="http://idoc.imagepy.org/imgs/p27.png"/>
        <img src="http://idoc.imagepy.org/imgs/p28.png"/>
      </td>
    </tr>
</table>

1. The two graphs are covered by points, that is, Surf feature points, where the correct match is shown in yellow.  
2. Also output a log of the opations. Identify the feature points of the two graphs, the correct number of matches, and the rotation matrix between the two graphs.  
3. When a point is clicked with the mouse, the dot will be red with the corresponding match point of the other picture at the same time.  

Fourth example: Dem Reconstruction
--------------------------------------
Use the mayavi library, to perform a large number of three-dimensional reconstructions and three-dimensional visualization functions.  

![](http://idoc.imagepy.org/imgs/p29.png "title") ![](http://idoc.imagepy.org/imgs/p30.png "title")  
1) Dem image 2) Reconstructed 3D Surface

**Dem** is the digital elevation model, which means that the brightness of the image represents the elevation. Through the Dem data, you can calculate the height, slope. You can draw contours, and perform surface reconstruction.

Fifth example: CT data 3D reconstruction
--------------------------------------------

The following image represents dental MicroCT data.  The data were filtered, segmented and three-dimensional reconstructed, as well as visually manipulated.

<table>
    <tr>
        <td><img src="http://idoc.imagepy.org/imgs/p31.png"/></td>
        <td valign="top"><img src="http://idoc.imagepy.org/imgs/p32.png"/></td>
    </tr>
        <tr>
        <td><img src="http://idoc.imagepy.org/imgs/p33.png"/></td>
        <td><img src="http://idoc.imagepy.org/imgs/p34.png"/></td>
    </tr>
</table>




The figure above is a tooth CT data. Importing the image sequence, you can view the three views, and then go on its three-dimensional reconstruction.  

**Image Stack:** ImagePy supports image stack processing, it has the following two characteristics:  

1. Images in the image stack have the same format and the same size.  
2. They will act on each image in the stack when processed.  

Plugins and Macros:
-------------------

In ImagePy itself, each functional component is plug-in (all menus, tools). The implementation of each function, in essence, is through interaction to get a group of parameters and then act on the current image. We can view the plug-in's organizational structure in Plugin Tree View, find plug-ins quickly in Plugin List View, record macros in Macros Recorder, and batch process when needed to do series of related functions and improve work efficiency.

![](http://idoc.imagepy.org/imgs/p35.png "title") ![](http://idoc.imagepy.org/imgs/p36.png "title")  
From the two views above, you can get a global view of all the plug-ins, like viewing its related information, introduction, and source code. You can 
quickly find the commands. You can run a related command directly by double-clicking.  

**Macro Recording of Cell Count Example:**  
We open the Plugins -> Macros -> Macros Recorder plug-in, and then re-operate the cell counting process...

<table>
    <td><img src="http://idoc.imagepy.org/imgs/p16.png"/></td>
    <td><img src="http://idoc.imagepy.org/imgs/p19.png"/></td>
    <td><img src="http://idoc.imagepy.org/imgs/p20.png"/></td>
    <td><img src="http://idoc.imagepy.org/imgs/p21.png"/></td>
    <td><img src="http://idoc.imagepy.org/imgs/p37.png"/></td>
    <td><img src="http://idoc.imagepy.org/imgs/p22.png"/></td>
    <td><img src="http://idoc.imagepy.org/imgs/p24.png"/></td>
</table>

After each step, Macros Recorder will add a log. When all is completed, you can get the following log:

These logs, each line essentially records “plug-in name> {parameter}”. Click “Run> Run Macros (F5)” to perform each action of the record in turn. You can also use the mouse to select a line or a few lines. Click “Run> Run Line (F6)” to implement the selected line. In addition macros have the following characteristics.

![](http://idoc.imagepy.org/imgs/p38.png "title") ![](http://idoc.imagepy.org/imgs/p16.png "title") ![](http://idoc.imagepy.org/imgs/p22.png "title") 

1. You can save a file where the suffix of macro is (.mc). You can run the specified macro file via Plugins -> Macros -> Run Macros.  
2. Put the macro file on the menus directory or any of its subdirectories in the project.  Starting once again, the macro will be loaded as a menu item. The title is the file name. In fact, some project function are in series by the macro.  

Extend a filter:
----------------

The examples above only list some of the functionality of the ImagePy. However, ImagePy is not only an image processing program, but a highly scalable framework. Any numpy-based processing function can be easily incorporated. For example, to make a Gaussian blur filter, we only need：  

``` python
# -*- coding: utf-8 -*
import scipy.ndimage as nimg
from core.engines import Filter

class Gaussian(Filter):
    title = 'Gaussian'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #parameter
    para = {'sigma':2}
    view = [(float, (0,30), 1,  'sigma', 'sigma', 'pix')]

    #process
    def run(self, ips, snap, img, para = None):
        nimg.gaussian_filter(snap, para['sigma'], output=img)
```

![](http://idoc.imagepy.org/imgs/p39.png "title") ![](http://idoc.imagepy.org/imgs/p40.png "title")  
1)dialog auto-build 2)result with a oval selection.  

Create a Filter:  

1. Import related class library.  It can be third-party or implemented in C.  
2. Create a class that subclasses `Filter`.  
3. `title`, this line is the name of the plug-in and will also serve as the title of the menu.  
4. `note` indicates how the plug-in works and the associated preprocessing and post-processing work. This includes which types of images can be processed, whether selections are supported or not, and so on.  
5. `para` is the parameter the kernel function needs.  
6. `view` and `para` are corresponding. They inform how the various parameters of the framework plug-in interact (the framework will generate your interactive interface automatically).  
7. `run` is the core function, if conditional, given `img` to the results of the process (save memory), or return out (the framework will help you give img).  
8. Place the file in any subdirectory of menus in the project, and it will be loaded as a menu item at startup.  

**What has the framework helped us do?**

They framework enables complex tasks in a uniform way. Simply, you do not need to determine for yourself whether the image type is legitimate. You do not need to make your own image cache to support undo. You do not need to support the selection by yourself. Do not need to monitor the interface by yourself to achieve real-time preview. You do not need to write any interface code after you have defined the required parameters, the type and the range of values for each parameter. When a color image is encountered, the each channel of the image is processed sequentially. When the image stack is encountered, each frame is automatically traversed.  You are free to work on either the task
of image analysis, or creating new plugins for the framework.

Extend a Tool:
--------------
Another scenario is to interact on the canvas through the mouse, like the selection operations mentioned above. Here is an example of a brush:  

``` python
from core.draw import paint
from core.engines import Tool
import wx

class Plugin(Tool):
  title = 'Pencil'
  para = {'width':1}
  view = [(int, (0,30), 0, 'width', 'width', 'pix')]

  def __init__(self):
    self.sta = 0
    self.paint = paint.Paint()
    self.cursor = wx.CURSOR_CROSS

  def mouse_down(self, ips, x, y, btn, **key):
    self.sta = 1
    self.paint.set_curpt(x,y)
    ips.snapshot()

  def mouse_up(self, ips, x, y, btn, **key):
    self.sta = 0

  def mouse_move(self, ips, x, y, btn, **key):
    if self.sta==0:return
    self.paint.lineto(ips.get_img(),x,y, self.para['width'])
    ips.update = True

  def mouse_wheel(self, ips, x, y, d, **key):pass
```

![](http://idoc.imagepy.org/imgs/p41.png "title") ![](http://idoc.imagepy.org/imgs/p42.png "title")   
1)config the line width 2)draw with difference line width  

**Create Tool:**

1. Inherited from `Tool` in the `engines`.  
2. Specify the `title`, which will be the tool name, and the message of the status bar.  
3. Adds several methods to achieve mouse_down, mouse_up, mouse_move, mouse_wheel.  
4. If the tool requires parameters (for example, pen width), use the dictionary to assign to `para`. Similarly, `view` specifies its interactive interface. When the tool is double-clicked, the dialog box will pop-up in accordance with the specified interface.  
5. Files are stored in the sub-folder of tools, with a generated 16 * 16 thumbnail icon. The icon and the tool are stored in the same name as the gif file.  

About ImagePy:
--------------
The above only lists some features of ImagePy, covering the basic mathematical operations, filters, pixel statistics, a slightly complex feature extraction, 3D reconstruction and other functions. It gives a brief introduction to macros , how to write new filters, tools and integrate them like ImagePy. Stay tuned for more detail in the coming manual and development documents.

I (yxdragon) have used ImageJ for a long time and also used to use Python for scientific computing. ImageJ's outstanding plug-in design philosophy allows it to absorb the contributions of industry professionals quickly. However, Python has an advantage over Java in image processing.  

1. Java is a system language, the relative threshold of it is relatively high.
2. The related open source libraries under Java are not as rich as C / C++.  
3. Python has simple grammar so it is easy to learn. It is a good choice for non-computer professionals.  
4. Python has a wealth of third-party extensions, such as Scikit-image, OpenCV, Matplotlib, Mayavi, etc.  
5. Almost all scientific computing class libraries are based on Numpy! so the framework can be built up easily.  
6. Python can be extended by C/C++ with ctypes/cython.  

Because of busy work, I wrote ImagePy in my spare time. All of the development work lasted about two months. Personally I think that this efficiency is mainly due to a large number of third-party libraries of Python as well as the project’s "borrowlism" design ideas. The project uses wxpython as the interface library, Numpy as the base data type. Because the time is short, many interactive details of the plug-in will show problems, you please give a positive feedback to me. I will do my best to safeguard the healthy growth of this project.

[https://github.com/yxdragon/imagepy.git](https://github.com/yxdragon/imagepy.git)

![](http://idoc.imagepy.org/imgs/p43.png "title")  
It is me, yxdragon.  
Email:imagepy@sina.com  
