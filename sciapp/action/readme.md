# SciApp

SciApp是一个交互式科学计算的后端框架，主要用于搭建科学分析应用。SciApp并不是算法库，也不包含任何界面，SciApp的目的是为算法类应用提供一个标准接口，具体如下：

1. 定义了科学计算常用的数据结构封装类
2. 对数据结构定义了一些基础操作函数
3. 定义了一个通用Manager，将各种数据进行管理，聚合为一个App对象
4. 定义了Action对象，可以对App对象进行操作



### Object模块

object模块定义了科学计算中常用的基础数据结构封装类，当然，如果仅仅为了计算，绝大多数时候，Numpy，Pandas等数据类型已经可以胜任，这里的封装，主要是面向交互与展示的，例如Image对象是图像数据，里面带了一个lut成员，用于在展示时映射成伪彩色。

1. Image：多维图像，基于Numpy
2. Table：表格，基于DataFrame
3. Shape: 点线面，任意多边形，可与GeoJson，Shapely互转
4. Surface：三维表面



### Util模块

Util定义了一些针对Object数据类型的基础操作函数，这些函数也是为了完成交互与展示，并非为了数据分析。

1. imutil: 主要实现图像的快速采样，多图层融合等算法

2. shputil: 主要实现多边形与给定点之间的几何关系，用于鼠标编辑。



### App容器

Manager：通用管理器对象，类似一个键值对管理器，里面装入key, value, tag样式的三元组，可以对元素进行增删查改。

App：一个科学容器，里面包含若干Manager，用于管理App所持有的Image，Table等Object，同时定义了一套标准展示接口，例如show_img, get_img, close_img等，（Table，Shape类似）



* [[Manager 对象]](./manager.md) 可以增删查改的对象容器
* [[App 对象]]() 科研应用接口，各类Object的大容器



### Action模块

Action：对App对象的一个操作，例如获取当前图像，做某种滤波，然后从图像中获取某种信息，最后show一个Table处理。其通用模板是Action().start(app)。可以在其子类中重载start，对app进行任何操作。

* [如何衍生出图像滤波类Action]()
* [如何衍生出数据读写类Action]()
* [读取-处理-写入，完成具体工作]()

以上例子是为了说明Action的作用机制，也展示了框架的构建思路，但并不意味着我们需要按照以上方法，从SciAction构建各种模板，我们已经构建了相当丰富，功能也更为完善的Action派生树，以下进行列举。



### Action的继承树

因为绝大多数的Action都和交互有关，而SciApp自身主要实现对象管理功能，交互只能通过print进行展示，所以很多功能这里只是列距，具体用法我们会在sciwx实现的一个App实例中展示。



**SciAction:** 所有Action的基类，start内获取app对象，进行处理

* ImageAction: 用于处理图像，自动获取当前图像，需要重载para，view进行交互，重载run进行图像处理

* TableAction: 用于处理表格，自动获取当前表格，需要重载para，view进行交互，重载run进行图像处理

* Tool: 工具，用于在某种控件上的鼠标交互

  * ImageTool: 图像工具，例如画笔，魔术棒等，需要重载一系列鼠标事件（参数坐标已转入图像坐标系）

  * TableTool：表格工具，需要重载一系列鼠标事件（参数坐标已自动转如单元格行列）
  * ShapeTool: 矢量编辑，例如点线面，多边形绘制（参数坐标已自动转如数据坐标系）

**Advanced:** 这个包下面是一些高级的Action模板，也是我们扩展插件主要使用的

* dataio: 里面实现了Reader，Writer类的Action，我们只需要将读写函数注册给对于的Manager
* Free: 继承SciAction，添加了para， view交互，添加了多线程支持。
* Filter: 继承ImageAction，主要用于做图像滤波，自动多通道，自带批量特性，多线程支持。
* Simple: 继承ImageAction，主要用于图像操作，自带多线程支持。
* Table: 继承TableAction，主要用于表格操作，比如表格统计，数据绘图等。
* Macros: 将一段字符串作为宏执行，构造时传入字符串，start后依次质心。

**Plugins:** 这个包下面有一些带有具体功能，开箱即用的Action

* filters：滤波类
  * Gaussian：高斯滤波
* generalio: 数据读取类
  * bmp, jpg, png, tif格式图像的读写支持
* ShapeTool: 矢量图像编辑工具
  * PointEditor: 编辑点
  * LineEditor: 编辑线
  * PolygonEditor: 编辑多边形
  * RectangleEditor: 编辑矩形
  * EllipseEditor: 编辑椭圆
  * FreeLineEditor: 编辑任意线
  * FreePolygonEditor: 编辑任意多边形

* ROITool: 类似于Shape，但作用对象是图像上的ROI
  * PointEditor: 编辑点
  * LineEditor: 编辑线
  * PolygonEditor: 编辑多边形
  * RectangleEditor: 编辑矩形
  * EllipseEditor: 编辑椭圆
  * FreeLineEditor: 编辑任意线
  * FreePolygonEditor: 编辑任意多边形

* MeasureTool: 类似于Shape，绘制同时会展示数值
  * CoordinateTool: 坐标测量
  * DistanceTool: 距离测量
  * AngleTool: 角度测量
  * SlopeTool: 梯度测量
  * AreaTool: 面积测量