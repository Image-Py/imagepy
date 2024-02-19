# cellpose-plgs

**Path:** https://github.com/Image-Py/cellpose-plgs

**Version:** 0.1

**Author:** YXDragon, Carsen-Stringer

**Email:** yxdragon@imagepy.org

**Keyword:** cellpose, segment, unet

**Description:** cellpose is a generalist algorithm for cell and nucleus segmentation, this is a cellpose plugin for imagepy.



## Document
### Install

there are two method to install  cellpose-plgs, Install Plugins or use Plugins Manager

1. **Menus: Plugins > Install > Install Plugins** then input https://github.com/Image-Py/cellpose-plgs

   ![](http://skimgplgs.imagepy.org/cellpose/install.png)

   

2. **Menus:  Plugins > Manager > Plugins Manager**, befor you open the manager, you should update the software, (to getting the newest plugins catlog). for git version, please pull, for release version, please use *Menus: Plugins > Updata Software*.

   ![](http://skimgplgs.imagepy.org/cellpose/manager.png)

when the cellpose-plgs is installed seccessfully, The cellpose would appears below the **Plugins** menus.



### Usage

**Menus: File > Open** to Open a Image, you can also use **Menus: File > Import > Import Sequence** to open a sequence. Then **Menus: Plugins > Cell Pose > Cell Pose Eval**, you would got a parameter dialog, Setting the parameter, then OK.



**Parameters:**

**model:** select model

**cytoplasm:** select the cytomplasm channel. 0: gray, 1:red, 2:green, 3:blue

**nucleus:** select the nucleus channel,  if there is no, select 0.

**show color flow:** the color flow result would be shown when checked.

**show diams tabel:** the diams result would be shown when checked.

**slice:** process the current image or all images when it is a sequence.

![](http://skimgplgs.imagepy.org/cellpose/cellpose.png)



### Analysis

**Menus: Analysis > Region Analysis > Geometry Analysis** do a region analysis. And we can do many other things in ImagePy, such as set a colormap, or overlay the mask on the original image.

![](http://skimgplgs.imagepy.org/cellpose/region.png)



### Reference

Thanks for CellPose and the supporting from  Carsen Stringer and Marius Pachitariu. More detail about CellPose please read the [paper](https://t.co/4HFsxDezAP?amp=1) or watch the [talk](https://t.co/JChCsTD0SK?amp=1). 