# SciApp

SciApp是一个交互式科学计算的后端框架，主要用于搭建科学分析应用。SciApp并不是算法库，也不包含任何界面，SciApp的目的是为算法类应用提供一个标准接口，具体如下：

1. 定义了科学计算常用的数据结构封装类
2. 对数据结构定义了一些基础操作函数
3. 定义了一个通用Manager，一个App，将各种数据进行管理
4. 定义了Action对象，可以对App进行操作



### Object模块

object模块定义了科学计算中常用的基础数据结构封装类，当然，如果仅仅为了计算，绝大多数时候，Numpy，Pandas等数据类型已经可以胜任，这里的封装，主要是面向交互与展示的，例如Image对象是图像数据，里面带了一个lut成员，用于在展示时映射成伪彩色。

1. Image：多维图像，基于Numpy

2. Table：表格，基于DataFrame

3. Shape: 点线面，任意多边形，基于Shapely

4. Surface：三维表面



### Util模块

Util定义了一些针对Object数据类型的基础操作函数，这些函数也是为了完成交互与展示，并非为了数据分析。

1. imutil: 主要实现图像的快速采样，多图层融合等算法

2. shputil: 主要实现多边形与给定点之间的几何关系，用于鼠标编辑。



### Action模块

App：

\1. Manager：Manager是一个通用容器，类似于mongodb的用法，具有add，get，

Sciapp: