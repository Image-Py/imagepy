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
<!--特点：软件具有友好的用户操作界面，能读取，保存多种图像数据格式，支持ROI设定，绘图，测量等鼠标操作。能完成图像滤波，形态学运算等常规操作，可以很好的完成一些分割，区域计数，几何测量，密度分析相关的工作。并可以对分析结果进行数据筛选，过滤，统计等相关工作。（软件功能定位可以理解为ImageJ  + SPSS，虽然目前尚未达到 -->


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

<!--ImagePy具有非常丰富的功能，而这里，我们仅仅用一个特定的例子，来对ImagePy进行一个初步的认识，我们这里选取scikit-image官方的硬币分割，相比之下，这个例子简单而全面。-->

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
<!--这里选用一个复合滤波器，对图像进行sobel梯度提取，然后通过上下阈值标定作为mark，在梯度图上进行分水岭分割。滤波，分割是图像处理过程中的核心技巧，是最终测量结果成败的关键，ImagePy支持常见的高斯，均值，中值，梯度，拉普拉斯，差分高斯等滤波，也包含自适应阈值，分水岭等分割方法。-->

<div align=center>
	<img src="imgs/image004.png" width="900"/>   
</div>

<div align=center>
	<img src="imgs/image005.png" width="900"/>   
</div>

### Binarization

`menu：Process -> Binary -> Binary Fill Holes`

经过上述分割，我们得到了相对纯净的掩膜图像，但依然存在一些镂空，以及少许外界杂质，这些会对计数和测量造成干扰，我们对图像进行二值填充。ImagePy支持腐蚀，膨胀，开，闭等二值化基础操作，也支持骨架，中轴线提取，距离变换等操作。

<div align=center>
	<img src="imgs/image006.png" width="900"/>   
</div>

区域过滤

菜单：Analysis \> Region Analysis \> Geometry
Filter，对区域进行过滤，这里可以简单的通过面积进行过滤，ImagePy的几何过滤可以通过面积，周长，拓扑，丰满度，偏心率等指标对区域进行过滤，可以输入复合条件，正数表示选择大于等于，负数表示选择小于，通过过滤的被设定为front
color，没通过的设定为back color，back
color设定为100可以清楚看到有哪些被滤掉了，如果确认符合要求，back
color设定为0，即清除。同时ImagePy也支持灰度密度过滤，颜色过滤，色彩聚类等功能。

<div align=center>
	<img src="imgs/image007.png" width="900"/>   
</div>

区域过滤（这里为了看清效果，area设定的较大，实际只需要过滤碎片）

区域分析

菜单：Process \> Region Analysis \> Geometry
Analysis，对区域进行计数和指标分析，这里我们勾上cov，即对区域进行协方差椭圆拟合。ImagePy支持面积，周长，偏心率，丰满度等指标，其实上一步的过滤正是在这里的分析结果基础上进行的。

<div align=center>
	<img src="imgs/image008.png" width="900"/>   
</div>

区域分析

<div align=center>
	<img src="imgs/image009.png" width="900"/>   
</div>

支持xls, xlsx,
csv表格格式，
生成结果表格（这里为了看清椭圆，把区域亮度降低了）

按照面积排序

菜单：Table \> Statistic \> Table Sort By
Key，选择第一主键为area，勾上descend，即按照面积降序排列。表格是图像之外的另外一种重要的数据，某种意义上，很多时候我们都需要在图像上得到需要的信息后，以表格的形式对数据进行后期加工。ImagePy支持表格筛选，截取，统计，排序等功能。

<div align=center>
	<img src="imgs/image010.png" width="900"/>   
</div>

在列头单击右键可以设定文字颜色，小数精度，线条样式等

统计图表

菜单：Table \> Chart \> Hist
Chart，表格数据一个常见的需求是绘制图表，这里我们对面积，周长两列进行直方图统计，得到分布直方图。ImagePy的表格可以绘制折线图，饼状图，柱状图，散点图等常见的图表。图表自带缩放，移动等功能，也可以存储为图片。

<div align=center>
	<img src="imgs/image011.png" width="900"/>   
</div>

统计直方图

三维图

菜单：Kit3D \> Viewer 3D \> 2D
Surface，对图像进行表面重建，这里其实是分别重建了sobel梯度图，高阈值，低阈值三个结果。图上可以清楚的看懂Up
And Down
Watershed的工作原理，首先计算梯度，然后通过高低阈值标记硬币和背景，最终在dem图上模拟涨水，形成分割。ImagePy可以做图像的三维滤波，三维骨架，三维拓扑分析，也可以对数据进行二维表面重建，以及三维表面可视化。三维视图中可以自由拖动，旋转视角，图片结果也可以输出为stl文件。

<div align=center>
	<img src="imgs/image012.png" width="900"/>   
</div>

height="4.347222222222222in"}

三维可视乎

宏录制与执行

菜单：Window \> Develop Tool Sute，
打开开发者工具，我们看到宏录制器。以上我们手工完成了一个图像数据分割，假设这些流程非常固定，并且很适合处理这类问题，而一次次的重复点击会让人审美疲劳。这种情况我们可以通过宏录制，来将若干过程捏合成一步。宏录制器类似一个录音机，打开时，我们每一步操作会形成一行记录。而我们可以点暂停键停止录制，点播放键执行。当宏运行是，会依次质心记录下来的命令，从而实现将若干步骤捏合成一步。

我们将宏保存为一个.mc文件，将文件拖放到ImagePy最下方的状态栏，宏会自动被执行，我们还可以将mc文件拷贝到ImagePy文件目录下的menus的子目录下，文件启动时，宏文件会被在对应位置解析成一个菜单项，当我们点击菜单，宏也会执行。

<div align=center>
	<img src="imgs/image013.png" width="900"/>   
</div>

宏录制

工作流

宏是一串固定的命令序列，通过将一系列固定的操作制作成宏，可以提高工作效率，但缺点是缺乏变通性，比如有时候我们的流程基本固定，但是一些细节，或者参数的设定上需要借助人工交互，这时候，工作流就可以很好的满足我们。工作流是一个流程图，分成，章，节，两个层次。章在流程图中对应于一个矩形区域，而节是矩形区域中的一个按钮，也是一条命令，并配有一段图文解释。当鼠标移动到按钮上，右侧的信息窗就会显示对应的功能说明。点击右上角的Detail
Document，查看整个流程的文档。

工作流的编写，实际上是一段MarkDown标记语言，但是需要按照规范编写，大致如下：

Title

===

\#\# Chapter1

1.  Section1

some coment for section1 \...

2.  \...

\#\# Chapter 2

\...

<div align=center>
	<img src="imgs/image014.png" width="900"/>   
</div>

![](imgs/image014.png){width="5.763888888888889in"
height="3.6944444444444446in"}

工作流

Filter插件

以上我们介绍了宏和工作流，利用宏和工作流可以串联已有的功能，但不能制造新的功能，而这里我们试图为ImagePy添加一个新功能。ImagePy可以方便的接入任何基于Numpy的函数，我们以scikit-image的Canny算子为例。

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

<div align=center>
	<img src="imgs/image015.png" width="900"/>   
</div>

![](imgs/image015.png){width="5.763888888888889in" height="4.5in"}

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
