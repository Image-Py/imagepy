# Introduction

ImagePy is an open source image processing framework written in Python. Its UI interface, image data structure and table data structure are wxpython-based, Numpy-based and pandas-based respectively. Furthermore, it supports any plug-in based on Numpy and pandas, which can talk easily between scipy.ndimage, scikit-image, simpleitk, opencv and other image processing libraries.

![newdoc01](http://idoc.imagepy.org/imgs/newdoc01.png)
<div align=center>Overview, mouse measurement, geometric transformation, filtering, segmentation, counting, etc.</div><br>

![newdoc02](http://idoc.imagepy.org/imgs/newdoc02.png)
<div align=center>If you are more a IJ-style user, try `Windows -> Windows Style` to switch</div><br>

ImagePy:
- has a user-friendly  interface
- can read/save a variety of image data formats
- supports ROI settings, drawing, measurement and other mouse operations
- can perform image filtering, morphological operations and other routine operations
- can do image segmentation, area counting, geometric measurement and density analysis.
- is able to perform data analysis, filtering, statistical analysis and others related to the parameters extracted from the image.

Our long-term goal of this project is to be used as ImageJ + SPSS (although not achieved yet)

## Installation

__OS support：windows, linux, mac, with python3.x__

1.  ImagePy is a ui framework based on wxpython, which can not be installed
    with pip on Linux. You need download [the whl according to your
    Linux system](https://wxpython.org/pages/downloads/).
2.  On Linux and Mac, there may be permission denied promblem, for
    ImagePy will write some config information, so please start with
    sudo. If you install with pip, please add \--user parameter like
    this: pip install --user imagepy
3.  If you install ImagePy in an Anaconda virtual environment, you may
    get a error when starting like this: This program needs access to the
    screen. Please run with a Framework build of python, and only when
    you are logged in on the main display, if so, please start with
    pythonw -m imagepy.

### - Pre-compiled package
This is the simplest option to run ImagePy.  
A precompiled archive can be downloaded from the [release tab](https://github.com/Image-Py/imagepy/releases) of the repository.  
Simply unzip the archive and run the ImagePy.bat file.  
This will open a command line window and open the GUI of ImagePy.

### - Using pip
In a command-prompt type `pip install imagepy`.
~~On Windows you currently need to first install shapely using conda.~~ This should also work for windows, now that shapely is available via pip.
Once installed, ImagePy can be run by typing `python -m imagepy` in a command prompt.



## Citation：
[ImagePy: an open-source, Python-based and platform-independent software package for bioimage analysis](https://academic.oup.com/bioinformatics/article/34/18/3238/4989871)

## Forum

ImagePy is a community partner of forum.image.sc, Anything about the usage and development of ImagePy could be discussed in https://forum.image.sc.



## Contribute

**Contribute Manual:** All markdown file under [doc folder](https://github.com/Image-Py/imagepy/tree/master/imagepy/doc) be parsed as manual. Plugins and manual are paired by plugins's title and manual's file name. We can browse document from the parameter dialog's Help button. We need more manual contributors, just pull request markdown file [here](https://github.com/Image-Py/imagepy/tree/master/imagepy/doc).

**Contribute Plugins:** Here is a [demo plugin](https://github.com/Image-Py/demoplugin) repositories with document to show how to write plugins and publish on ImagePy. You are wellcom and feel free to contact with us if you need help.

**Improve Main Framework:** Just fork ImagePy, then give Pull Request. But if you want to add some new feature, Please have a issue with us firstly.

## Basic operations：

ImagePy has a very rich set of features, and here, we use a specific example to show you a glimpse of the capacity of ImagePy. We choose the official coin split of scikit-image, since this example is simple and comprehensive.

### Open image

`menu: File -> Local Samples -> Coins` to open the sample image within ImagePy.
_PS: ImagePy supports bmp, jpg, png, gif, tif and other commonly used file formats. By installing ITK plug-in，dicom，nii and other medical image formats can also be read/saved. It is also possible to read/write wmv, avi and other video formats by installing OpenCV._

![newdoc03](http://idoc.imagepy.org/imgs/newdoc03.png)
<div align=center>Coins</div><br>


### Filtering & Segmentation

`menu：Process -> Hydrology -> Up And Down Watershed` Here, a composite filter is selected to perform sobel gradient extraction on the image, and then the upper and lower thresholds are used as the mark, and finally we watershed on the gradient map.
Filtering and segmentation are the crucial skills in the image processing toolkit, and are the key to the success or failure of the final measurement.
Segmentation methods such as adaptive thresholds, watersheds and others are also supported.

![newdoc04](http://idoc.imagepy.org/imgs/newdoc04.png)
<div align=center>Up And Down Watershed</div><br>

![newdoc05](http://idoc.imagepy.org/imgs/newdoc05.png)
<div align=center>Mask</div><br>

### Binarization

`menu：Process -> Binary -> Binary Fill Holes` After the segmentation, we obtained a relatively clean mask image, but there is still some hollowing out, as well as some impurities, which will interfere with counting and measurement.
_ImagePy supports binary operations such as erode, dilate, opening and closing, as well as skeletonization, central axis extraction, and distance transformation._

![newdoc06](http://idoc.imagepy.org/imgs/newdoc06.png)
<div align=center>Fill Holes</div><br>

### Geometry filtering

`menu：Analysis -> Region Analysis -> Geometry Filter` ImagePy can perform geometric filtering based on :__the area, the perimeter, the topology, the solidity, the eccentricity__ and other parameters. You can also use multiple conditions for filtering. Each number can be positive|negative, which indicates the kept object will have the corresponding parameter greater|smaller than the value respectively. The kept objects will be set to the front color, the rejected ones will be set to the back color. In this demo, the back color is set to 100 in order to see which ones are filtered out. Once satisfied with the result, set the back color to 0 to reject them. In addition, ImagePy also supports gray density filtering, color filtering, color clustering and other functions.

![newdoc07](http://idoc.imagepy.org/imgs/newdoc07.png)
<div align=center>Geometry filtering (the area is over-chosen to emphasize the distinction)</div><br>


### Geometry Analysis

`menu：Process -> Region Analysis -> Geometry Analysis` Count the area and analyze the parameters. By choosing the `cov` option, ImagePy will fit each area with an ellipse calculated via the covariance.
The parameters such as area, perimeter, eccentricity, and solidity shown in the previous step are calculated here. In fact, the filtering of the previous step is a downstream analysis of this one.

![newdoc08](http://idoc.imagepy.org/imgs/newdoc08.png)
<div align=center>Geometry Analysis</div><br>

![newdoc09](http://idoc.imagepy.org/imgs/newdoc09.png)
<div align=center>Generate the result table (dark to emphasize the ellipse)</div><br>


### Sort Table by area

`menu：Table -> Statistic -> Table Sort By Key` Select the major key as area, and select descend. The table will be sorted in descending order of area. A table is another important piece of data other than an image. In a sense, many times we need to get the required information on the image and then post-process the data in the form of a table. ImagePy supports table I/O (xls, xlsx, csv), filtering, slicing, statistical analysis, sorting and more.  (Right click on the column header to set the text color, decimal precision, line style, etc.)

![newdoc10](http://idoc.imagepy.org/imgs/newdoc10.png)
<div align=center>Table</div><br>


### Charts

`menu：Table -> Chart -> Hist Chart` From tabular data, we often need to draw a graph. Here, we plot the histograms of the area and the perimeter columns. ImagePy's tables can be used to draw common charts such as line charts, pie charts, histograms, and scatter plots (matplotlib-based). The chart comes with zooming, moving and other functions. The table can also be saved as an image.

![newdoc11](http://idoc.imagepy.org/imgs/newdoc11.png)
<div align=center>Histograms</div><br>


### 3D chart

`menu：Kit3D -> Viewer 3D -> 2D Surface` Surface reconstruction of the image. This image shows the three reconstructed results including, sobel gradient map, high threshold and low threshold. It shows how the Up And Down Watershed works:
- calculate the gradient.
- mark the coin and background through the high and low thresholds,
- simulate the rising water on the dem diagram to form the segmentation.

ImagePy can perform 3D filtering of images, 3D skeletons, 3D topological analysis, 2D surface reconstruction, and 3D surface visualization. The 3D view can be freely dragged, rotated, and the image results can be saved as a .stl file.

![newdoc12](http://idoc.imagepy.org/imgs/newdoc12.png)
<div align=center>3D visualisation</div><br>



### Macro recording and execution

`menu：Window -> Develop Tool Suite` Macro recorder is shown in the develop tool panel. We have manually completed an image segmentation. However, batch processing more than 10 images can be tedious. So, assuming that these steps are highly repeatable and robust for dealing with such problems, we can record a macro to combine several processes into a one-click program. The macro recorder is similar to a radio recorder. When it is turned on, each step of the operation will be recorded. We can click the pause button to stop recording, then click the play button to execute. When the macro is running, the recorded commands will be executed sequentially, therefore achieving simplicity and reproducibility.

Macros are saved into .mc files. drag and drop the file to the status bar at the bottom of ImagePy, the macro will be executed automatically. we can also copy the .mc file to the submenu of the menus under the ImagePy file directory. When ImagePy is started, the macro file will be parsed into a menu item at the corresponding location. By clicking the menu, the macro will also be executed.

![newdoc13](http://idoc.imagepy.org/imgs/newdoc13.png)
<div align=center>Macro Recording</div><br>


### Workflow

A macro is a sequence of predefined commands. By recording a series of fixed operations into macros, you can improve your work efficiency. However, the disadvantage is the lack of flexibility. For example, sometimes the main steps are fixed, but the parameter tuning needs human interaction. In this case, the workflow is what you want. A workflow in ImagePy is a flow chart that can be visualized, divided into two levels: __chapters and sections__.
The chapter corresponds to a rectangular area in the flow chart, and the section is a button in the rectangular area, which is also a command and is accompanied by a graphic explanation. The message window on the right will display the corresponding function description, while mousing hovering above. Click on the `Detail Document` in the top right corner to see the documentation of the entire process.


The workflow is actually written in MarkDown (a markup language), but it needs to be written respecting several specifications, as follows:

```markdown
Title
=====
## Chapter1
1. Section1
some coment for section1 ...
2. ...
## Chapter 2
	...
```
![newdoc14](http://idoc.imagepy.org/imgs/newdoc14.png)
<div align=center>Workflow</div><br>

### Report Plugin

Sometimes we need to make a report to print or generate a PDF document. ImagePy can generate report from a xlsx template. We just need put specific mark in some cells, ImagePy will parse the template and generate a parameter dialog, then we can input some information, or give image/table in, the report will be generated! more about how to make template please see [here](https://github.com/Image-Py/demoplugin/blob/master/doc/report.md).

![newdoc14](http://idoc.imagepy.org/demoplugin/38.png)

<div align=center>generate report</div><br>

### Filter Plugin

We introduced macros and workflows in the last sections, using macros and workflows to connect existing functions is convenient. But sometimes we need to create new features. In this section, we are trying to add a new feature to ImagePy. ImagePy can easily access any Numpy-based function. Let's take the Canny operator of scikit-image as an example.

```python
from skimage import feature
from imagepy.core.engine import Filter

class Plugin(Filter):
    title = 'Canny'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'sigma':1.0, 'low_threshold':10, 'high_threshold':20}

    view = [(float, 'sigma', (0,10), 1, 'sigma', 'pix'),
            ('slide', 'low_threshold', (0,50), 4, 'low_threshold'),
            ('slide', 'high_threshold', (0,50), 4, 'high_threshold')]

def run(self, ips, snap, img, para = None):
    return feature.canny(snap, para['sigma'], para['low_threshold'],
        para['high_threshold'], mask=ips.get_msk())*255
```
![newdoc15](http://idoc.imagepy.org/imgs/newdoc15.png)
<div align=center>Canny Filter Demo</div><br>

#### Steps to create a your own filter:

1. Import the package(s), often third party.
2. Inherit the __`Filter`__ class。
3. The __`title`__ will be used as the name of the menu and the title of the parameter dialog, also as a command for macro recording.
4. Tell the framework what needs to do for you in __`Note`__, whether to do type checking, to support the selection, to support _UNDO_, etc.
5. __`Para`__ is the a dictionary of parameters, including needed parameters for the
   functions.
6. Define the interaction method for each of the parameters in __`View`__, the framework will automatically generate the dialog for parameter tuning by reading these information.
7. Write the core function __`run`__. `img` is the current image, `para` is the result entre by user. if `auto_snap` is set in `note`, `snap` will be a duplicate of `img`. We can process the `snap`, store the result in `img`. <span style="color:red">If the function does not support the specified output</span>, we can also return the result, and the framework will help us copy the result to img and display it.
8. Save the file as `xxx_plg.py` and copy to the `menu` folder, restart ImagePy.
   It will be loaded as a menu item.

#### What did the framework do for us?

The framework unifies the complex tasks in a formal manner and helps us to perform:
- type checking. If the current image type does not meet the requirements in the note, the analysis is terminated.
- according to the `para`, generate automatically a dialog box to detect the input legality from the `view`.
- Real-time preview
- automatic ROI support
- undo support
- parallelization support
- image stack support
- etc.

### Table

As mentioned earlier, the table is another very important data type other than the image. Similarly, ImagePy also supports the extension of table. Here we give an example of sorting-by-key used in the previous description.

```python
from imagepy.core.engine import Table
import pandas as pd

class Plugin(Table):
    title = 'Table Sort By Key'
    para = {'major':None, 'minor':None, 'descend':False}

    view = [('field', 'major', 'major', 'key'),
    	    ('field', 'minor', 'minor', 'key'),
    	    (bool, 'descend', 'descend')]

def run(self, tps, data, snap, para=None):
    by = [para['major'], para['minor']]
    data.sort_values(by=[i for i in by if i != 'None'],
        axis=0, ascending = not para['descend'], inplace=True)
```
![newdoc16](http://idoc.imagepy.org/imgs/newdoc16.png)
<div align=center>Table Sort Demo</div><br>

#### How Table works

Same as `Filter`，`Table` also has parameters such as `title`，`note`，`para`，`view`.
When the plugin is running, the framework will generate a dialog box according to `para`
and `view`. After the parameters are chosen, they are passed to the `run` together with the current table and be processed. The table data is a pandas.DataFrame object in the current table, stored in `tps`. Other information, such as `tps.rowmsk`, `tps.colmsk` can also be retrieved from `tps` to get the row and column mask of the current selected table.

### Other type of plugins

The `Filter` and `Table` described above are the two most important plugins, but ImagePy also supports some other types of plugin extensions. There are currently ten, they are:

1. `Filter`: mainly for image processing
2. `Simple`: similar to `Filter`, but focus on the overall characteristics of the image, such as the operation of the ROI, the operation of the false color, the area measurement, or the three-dimensional analysis of the entire image stack, visualization, and so on.
3. `Free`: operate that are independant of image. Used to open image, close software etc.
4. `Tool`: use the mouse to interact on the diagram and show small icons on the toolbar, such as a brush.
5. `Table`: operate on the table, such as statistics analysis, sorting, plotting.
6. `Widget`: widgets that are displayed in panels, such as the navigation bar on the right, the macro recorder, and others.
7. `Markdown`: markup language, when clicked, a separate window will pop up to display the document.
8. `Macros`：command sequence file for serially fixed operational procedures.
9. `Workflow`: combination of macro and MarkDown to create an interactive guidance process.
10. `Report`: a xlsx template with specific mark, rename as `.rpt`, used to auto generate report.

## Motivation & Goal

Python is a simple, elegant, powerful language, and has very rich third-party libraries for scientific computing. Based on the universal matrix structure and the corresponding rules, numpy-based libraries such as scipy, scikit-image, scikit-learn and other scientific computing libraries have brought great convenience to scientific research. On the other hand, more and more problems in biology, material science and other scientific research can be efficiently and accurately solved via scientific computing, image processing.

However there are still many researchers that lack programming skills. Thus it is a crucial to make the Numpy-based scientific computing libraries available to more researchers. ImagePy brings the computing capacities closer to the non-programmer researchers, so that they won't need to be concerned about the UI and interaction design, and focus exclusively on the algorithm itself, and finally, accelerate open-source tool building or even commercial products incubation. These tools, meanwhile, can let more researchers, who are not good at programming, gain, promote and popularize scientific knowledge such as image processing and statistics.
