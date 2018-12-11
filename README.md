<!-- 简介 -->

<!-- ImagePy是基于Python开发的开源图像处理框架，采用wxpython界面基础，基于Numpy为核心图像数据结构，pandas为核心表格数据结构，并支持任何基于Numpy，pandas的插件扩展，可以方便的接入scipy.ndimage, scikit-image, simpleitk, opencv等算法库进行插件扩展。-->

# Introduction

ImagePy is an open source image processing framework written in Python. Its UI interface, image data structure and table data structure are wxpython-based, Numpy-based and pandas-based respectively. Furthermore, it supports any plug-in based on Numpy and pandas, which can talk easily between scipy.ndimage, scikit-image, simpleitk, opencv and other image processing libraries.  

<div align=center>
	<img src="imgs/image001.png" alt="Overview" width="900"/>  
	Overview, mouse measurement, geometric transformation, filtering, segmentation, counting, etc.
</div>
<!-- 总览，鼠标测量，几何变换，滤波，分割，计数等 -->

<div align=center>
	<img src="imgs/image002.png" alt="ij style" width="900"/>   
	If you are more a IJ-style user, try `Windows -> Windows Style` to switch
</div>

ImagePy:
- has a user-friendly  interface
- can read/save a variety of image data formats
- supports ROI settings, drawing, measurement and other mouse operations
- can perform image filtering, morphological operations and other routine operations
- can do image segmentation, area counting, geometric measurement and density analysis. 
- is able to perfrom data analysis, filtering, statistical analysis and others related to the parameters extracted from the image. 

Our long-term goal of this project is to be used as ImageJ + SPSS (although not achieved yet)   

## Citation：
[ImagePy: an open-source, Python-based and platform-independent software package for bioimage analysis](https://academic.oup.com/bioinformatics/article/34/18/3238/4989871)

# Installation

__OS support：windows, linux, mac, with python2.7 and python3.__4+

1.  ImagePy is a ui framework based on wxpython, which can not install
    with pip on Linux. You need download [the whl acrodding to your
    Linux system](https://wxpython.org/pages/downloads/).

2.  On Linux and Mac, there may be permission denied promblem, for
    ImagePy will write some config information, So please start with
    sudo. If you install with pip, please add \--user parameter like
    this: pip install -user imagepy

3.  If you install ImagePy in a Anaconda virtual environment, you may
    got a error when start like this: This program needs access to the
    screen. Please run with a Framework build of python, and only when
    you are logged in on the main display, if so, please start with
    pythonw -m imagepy.

## Basic operations：

ImagePy has a very rich set of features, and here, we use a specific example to show you a glimpse of the capacity of ImagePy. We choose the official coin split of scikit-image, since this example is simple and comprehensive.  

### Open image

`menu: File -> Local Samples -> Coins` to open the sample image within ImagePy. 
_PS: ImagePy supports bmp, jpg, png, gif, tif and other commonly used file format. By installing ITK plug-in，dicom，nii and other medical image format can also be read/saved. It is also possible to read/write wmv, avi and other video format by installing OpenCV._  

<div align=center>
	<img src="imgs/image003.png" alt="ij style" width="900"/>   
</div>


### Filtering & Segmentation  

`menu：Process -> Hydrology -> Up And Down Watershed`  
Here, a composite filter is selected to perform sobel gradient extraction on the image, and then the upper and lower thresholds are used as the mark, at last we watershed on the gradient map.  
Filtering and segmentation are the crucial skills in the image processing toolkit, and are the key to the success or failure of the final measurement.  
Segmentation methods such as adaptive thresholds, watersheds and others are also supported.

<div align=center>
	<img src="imgs/image004.png" width="900"/>   
</div>

<div align=center>
	<img src="imgs/image005.png" width="900"/>   
</div>

### Binarization

`menu：Process -> Binary -> Binary Fill Holes`  

After the segmentation, we obtained a relatively clean mask image, but there are still some hollowing out, as well as a little impurities, which will interfere with counting and measurement.  
_ImagePy supports binary operations such as erode, dilate, opening and closing, as well as skeletonization, central axis extraction, and distance transformation._  

<div align=center>
	<img src="imgs/image006.png" width="900"/>   
</div>

### Geometry filtering  

`menu：Analysis -> Region Analysis -> Geometry Filter`  

ImagePy can perform geometric filtering based on :__the area, the perimeter, the topology, the solidity, the eccentricity__ and other parameters. You can also use multiple conditions filtering. Each number can be positive|negative. It indicates the kept object will have the corresponding parameter greater|smaller than the value respectively. The kept objects will be set to the front color, the rejected ones will be set to the back color. In this demo, the back color is set to 100 in order to see which ones are filtered out. Once satisfied with the result, set the back color to 0 to reject them. In addition, ImagePy also supports gray density filtering, color filtering, color clustering and other functions.  

<div align=center>
	<img src="imgs/image007.png" width="900"/>   
	Geometry filtering (the area is over-chosen to emphasize the distinction) 
</div>


### Geometry Analysis   

`menu：Process -> Region Analysis -> Geometry Analysis`  
Count the area and analyze the parameters. By choosing the `cov` option, ImagePy will fit each area with an ellipse calculated via the covariance.  
The parameters such as area, perimeter, eccentricity, and solidity shown in the previous step are calculated here. In fact, the filtering of the previous step is a downstream analysis of this one.

<div align=center>
	<img src="imgs/image008.png" width="900"/>   
	<img src="imgs/image009.png" width="900"/>   
	Geometry Analysis	
</div>

（这里为了看清椭圆，把区域亮度降低了）

### Sort Table by area  

`menu：Table -> Statistic -> Table Sort By Key`  

Select the major key as area, and select descend. The table will be sorted in descending order of area. A table is another important piece of data other than an image. In a sense, many times we need to get the required information on the image and then post-process the data in the form of a table. ImagePy supports table I/O (xls, xlsx, csv), filtering, slicing, statistical analysis, sorting and more.  

<div align=center>
	<img src="imgs/image010.png" width="900"/>   
	Right click on the column header to set the text color, decimal precision, line style, etc.
</div>


### Charts 

`menu：Table -> Chart -> Hist Chart`  

From tabular data, we often need to draw a graph. Here, we plot the histograms of the area and the perimeter columns. ImagePy's tables can be used to draw common charts such as line charts, pie charts, histograms, and scatter plots (matplotlib-based). The chart comes with zooming, moving and other functions. The table can also be saved as an image.  


<div align=center>
	<img src="imgs/image011.png" width="900"/>   
	Histograms
</div>


### 3D chart

`menu：Kit3D -> Viewer 3D -> 2D Surface`  


Surface reconstruction of the image. This image shows the three reconstructed results including, sobel gradient map, high threshold and low threshold. It shows how the Up And Down Watershed works:  
- calculate the gradient.
- mark the coin and background through the high and low thresholds,
- simulate the rising water on the dem diagram to form the segmentation.  

ImagePy can perform 3D filtering of images, 3D skeletons, 3D topological analysis, 2D surface reconstruction, and 3D surface visualization. The 3D view can be freely dragged, rotated, and the image results can be saved as a .stl file.

<div align=center>
	<img src="imgs/image012.png" width="900"/>   
	3D visualisation	
</div>



### Macro recording and execution  

`menu：Window -> Develop Tool Suite`  

Macro recorder is shown in the develop tool panel. We have manually completed an image segmentation. However, batch processing more than 10 images can be tedious. So, assuming that these steps are highly repeatable and robust for dealing with such problems, we can record a macro to combine several processes into a one-click program. The macro recorder is similar to a radio recorder. When it is turned on, each step of the operation will be recorded. We can click the pause button to stop recording, then click the play button to execute. When the macro is running, the recorded commands will be executed sequentially, therefore achieving simplicity and reproducibility.

Macros are saved into .mc files. drag and drop the file to the status bar at the bottom of ImagePy, the macro will be executed automatically. we can also copy the .mc file to the submenu of the menus under the ImagePy file directory. When ImagePy is started, the macro file will be parsed into a menu item at the corresponding location. By clicking the menu, the macro will also be executed.

<div align=center>
	<img src="imgs/image013.png" width="900"/>   
	Macro Recording
</div>


### Workflow

A macro is a sequence of predefined commands. By recording a series of fixed operations into macros, you can improve your work efficiency. However, the disadvantage is the lack of flexibility. For example, sometimes the main steps are fixed, but the parameter tuning needs human interaction. In this case, the workflow is what you want. A workflow in ImagePy is a flow chart that can be visualized, divided into two levels: __chapters and sections__.  
The chapter corresponds to a rectangular area in the flow chart, and the section is a button in the rectangular area, which is also a command and is accompanied by a graphic explanation. The message window on the right will display the corresponding function description, while mousing hovering above. Click on the `Detail Document` in the top right corner to see the documentation of the entire process.


The workflow is actually written in MarkDown (a markup language), but it needs to be written respecting several specifications, as follows:

```
Title
===
## Chapter1
1.  Section1
some coment for section1 ...
2.  ...
## Chapter 2
	...
```
<div align=center>
	<img src="imgs/image014.png" width="900"/>   
	Workflow
</div>



### Filter Plugin

以上我们介绍了宏和工作流，利用宏和工作流可以串联已有的功能，但不能制造新的功能，而这里我们试图为ImagePy添加一个新功能。ImagePy可以方便的接入任何基于Numpy的函数，我们以scikit-image的Canny算子为例。

```
from skimage import feature

from imagepy.core.engine import Filter

class Plugin(Filter):

title = \'Canny\'

note = \[\'all\', \'auto\_msk\', \'auto\_snap\', \'preview\'\]

para = {\'sigma\':1.0, \'low\_threshold\':10, \'high\_threshold\':20}

view = \[(float, \'sigma\', (0,10), 1, \'sigma\', \'pix\'),

(\'slide\', \'low\_threshold\', (0,50), 4, \'low\_threshold\'),

(\'slide\', \'high\_threshold\', (0,50), 4, \'high\_threshold\')\]

def run(self, ips, snap, img, para = None):

return feature.canny(snap, para\[\'sigma\'\], para\[low\_threshold\'\],

para\[\'high\_threshold\'\], mask=ips.get\_msk())\*255
```
<div align=center>
	<img src="imgs/image015.png" width="900"/>   
</div>


滤波器的作用机制:

1.  引入需要的库，往往是第三方的库。

2.  继承Filter。

3.  Title，标题，将作为菜单的名称和参数对话框的标题，也作为宏录制的命令。

4.  Note，指明需要框架为你做什么，是否需要做类型检查，是否支持选区，是否支持撤销等。

5.  Para，参数字典，核心函数需要用到的参数

6.  View，参数视图，指明每个参数对应的交互方式，框架会根据这里的信息自动生成交互对话框。

7.  核心函数，img是当前图像，para参数交互结果，如果note里设定了auto\_snap，则img也被复制到snap，我们可以对snap进行处理，将结果存放在img中，如果函数不支持指定输出，我们也可以return处理结果，框架会帮我们将结果拷贝给img并展示。

8.  将文件存储为xxx\_plg.py，并拷贝到ImagePy \>
    Menus目录下，重启，会被加载成一个菜单项。

框架帮我们做了什么？

框架将复杂的任务进行了形式上的统一，并且帮我们进行类型检查，如果当前图像类型不符合note中的要求，则终止分析，根据para，view自动生成对话框，检测输入合法性，对图像进行实时预览，自动提供ROI支持，撤销支持，并提供多通道支持，提供图像序列支持等。

表格

正如前面所说的，表格是图像之外另一种非常重要的数据，同样ImagePy也支基于表格的功能扩展，我们用前面用到过的按照住键排序的例子来做说明。
```
from imagepy.core.engine import Table

import pandas as pd

class Plugin(Table):

title = \'Table Sort By Key\'

para = {\'major\':None, \'minor\':None, \'descend\':False}

view = \[(\'field\', \'major\', \'major\', \'key\'),

(\'field\', \'minor\', \'minor\', \'key\'),

(bool, \'descend\', \'descend\')\]

def run(self, tps, data, snap, para=None):

by = \[para\[\'major\'\], para\[\'minor\'\]\]

data.sort\_values(by=\[i for i in by if i != \'None\'\],

axis=0, ascending=not para\[\'descend\'\], inplace=True)
```
<div align=center>
	<img src="imgs/image010.png" width="900"/>   
</div>

Table的作用机制

类比Filter，Table同样有title，note，para，view参数，当插件运行是框架通过para，view解析为对话框，交互完成后，参数和当表格会一起传递给run，run中对表格进行核心处理，data是当前表格对应的pandas.DataFrame对象，tps中存储了其他信息，比如tps.rowmsk，tps.colmsk可以拿到当前表格被选中的行列掩膜。

其他插件类型

上面介绍的Filter和Table是最重要的两种插件，但ImagePy也支持其他一些类型的插件扩展，目前有九种，他们是：

1.  Filter：主要用来对图像进行处理

2.  Simple：类似于Filter，但侧重与图像的整体特性，比如对ROI的操作，对假彩色的操作，区域测量，或者对整个图像栈进行的三维分析，可视化等。

3.  Free：用于不依赖图像的操作，比如打开图像，关闭软件等。

4.  Tool：借助鼠标在图上进行交互，将以小图标的形式出现在工具栏上，例如画笔。

5.  Table：对表格进行操作，例如统计，排序，出图。

6.  Widget：以面板形式展现的功能部件，例如右侧的导航栏，宏录制器等。

7.  Markdown：MarkDown标记语言，点击后会弹出独立窗口展示文档。

8.  Macros：命令序列文件，用于串联固定的操作流程。

9.  Workflow：工作流，宏和MarkDown的结合，用于制作交互式指引流程。

开发意义

Python是一门简单，优雅，强大的语言，并且在科学计算方面有非常丰富的第三方库，并且Numpy制定了良好的规范，建立在Numpy基础上的Scipy，scikit-image，scikit-learn等科学计算库给科研工作带来了极大的便利。另一方面，科学计算，图像处理在生物，材料等科研领域可以高效准确的解决越来越多的问题，然而依然有很多科研工作者编程能力比较薄弱，因此让Numpy系列的科学计算库造福更多科研工作者是一项非常有意义的工作。而ImagePy就是一座桥梁，尽可能的让科学计算工作者隔离自己不擅长的UI和交互设计，着重精力处理算法本身，并且可以快速形成工具甚至产品，而这些工作又可以让更多不擅长编程的科研工作者收益，推广和普及图像处理，统计等科学知识。
