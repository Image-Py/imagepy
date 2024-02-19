# cellpose-planer
**Path:** https://gitee.com/imagepy/cellpose-planer

**Version:** 0.1

**Author:** YXDragon, Y.Dong

**Email:** yxdragon@imagepy.org

**Keyword:** cellpose, segment, unet

**Description:** cellpose on planer framework for imagepy.


[Cellpose](https://github.com/MouseLand/cellpose) is a generalist algorithm for cellular segmentation, Which written by Carsen Stringer and Marius Pachitariu.

[Planer](https://github.com/Image-Py/planer) is a light-weight CNN framework implemented in pure Numpy-like interface. It can run only with Numpy. Or change different backends. (Cupy accelerated with CUDA, ClPy accelerated with OpenCL).

So Cellpose-Planer is the **cellpose** models on **planer** framework. We generate onnx from torch models, then deduce it to planer model. 

**We just use cellpose's models, but we rewrite all the pre-after processing and render algorithm, So the result is not same as the official one**

## Features
* cellpose-planer is very light, only depend on [Numpy](https://github.com/numpy/numpy) and Scipy.
* cellpose-planer can be accelerated with [Cupy](https://github.com/cupy/cupy).
* without ui, with out object or class, pure function oriented designed.
* optimize cellpose 's pre-after processing and render algorithm, having a better performance and result.

## Install
**pip install cellpose-planer**

Option: *pip install cupy-cuda101* on envidia gpu, install cuda and cupy would get a large acceleration.

# Usage
```python
import cellpose_planer as cellpp
from skimage.data import coins

img = coins()
x = img.astype(np.float32)/255

net = cellpp.load_model('cyto_0')
flowpb, style = cellpp.get_flow(net, x, size=480)
lab = cellpp.flow2msk(flowpb, level=0.2)

flowpb = cellpp.asnumpy(flowpb)
lab = cellpp.asnumpy(lab)
cellpp.show(img, flowpb, lab)
```
![demo](https://user-images.githubusercontent.com/24822467/111028247-4d549580-83aa-11eb-9bf4-2cb87332530e.png)

## first time: search and download models
search the models you need, and download them. (just one time)
```python
>>> import cellpose_planer as cellpp
>>> cellpp.search_models()
cyto_0 : --
cyto_1 : --
cyto_2 : --
cyto_3 : --
nuclei_0 : --
nuclei_1 : --
nuclei_2 : --
nuclei_3 : --

>>> cellpp.download(['cyto_0', 'cyto_1', 'cyto_2', 'cyto_3'])
download cyto_0 from http://release.imagepy.org/cellpose-planer/cyto_0.npy
100%|█████████████████████████████████████| 100/100 [00:10<00:00,  2.37it/s]
download cyto_1 from http://release.imagepy.org/cellpose-planer/cyto_1.npy
100%|█████████████████████████████████████| 100/100 [00:10<00:00,  2.37it/s]
download cyto_2 from http://release.imagepy.org/cellpose-planer/cyto_2.npy
100%|█████████████████████████████████████| 100/100 [00:10<00:00,  2.37it/s]
download cyto_3 from http://release.imagepy.org/cellpose-planer/cyto_3.npy
100%|█████████████████████████████████████| 100/100 [00:10<00:00,  2.37it/s]

>>> cellpp.list_models()
['cyto_0', 'cyto_1', 'cyto_2', 'cyto_3']
```

## 1. load models
you can load one model or more, when multi models, you would get a mean output.
```python
nets = cellpp.load_model('cyto_0')
nets = cellpp.load_model(['cyto_0', 'cyto_1', 'cyto_2', 'cyto_3'])
```

## 2. get flow image
**def get_flow(nets, img, cn=[0,0], sample=1, size=512, tile=True, work=1, callback=progress)**

* *nets:* the nets loaded upon.

* *img:* the image to process

* *cn:* the cytoplasm and nucleus channels

* *sample:* if not 1, we scale it. (only avalible when tile==True)

* *size:* when tile==True, this is the tile size, when tile==False, we scale the image to size.

* *tile:* if True, method try to process image in tiles. else resize the image.

* *work:* open multi-thread to process the image. (GPU not recommend)
```python
flowpb, style = cellpp.get_flow(net, coins(), [0,0], work=4)
```

## 3. flow to mask
**def flow2msk(flowpb, level=0.5, grad=0.5, area=None, volume=None)**

* *flowpb:* get_flow 's output

* *level:* below level means background, where water can not flow. So level decide the outline.

* *grad:* if the flow gradient is smaller than this value, we set it 0. became a watershed. bigger gradient threshold could suppress the over-segmentation. especially in narrow-long area.

* *area:* at end of the flow process, every watershed should be small enough. (<area), default is 0 (auto).

* *volume:* and in small area, must contian a lot of water. (>volume), default is 0 (auto).

```python
msk = cellpp.flow2msk(flowpb, level=0.5, grad=0.5, area=None, volume=None)
```
## 4. render
cellpose-planer implements some render styles.
```python
import cellpose_planer as cellpp

# get edge from label msask
edge = cellpp.msk2edge(lab)
# get build flow as hsv 2 rgb
hsv = cellpp.flow2hsv(flow)
# 5 colors render (different in neighborhood)
rgb = cellpp.rgb_mask(img, lab)
# draw edge as red line
line = cellpp.draw_edge(img, lab)
```
![cell](https://user-images.githubusercontent.com/24822467/111029250-93acf300-83b0-11eb-9e83-41bc0cf045dd.png) 

## 5. backend and performance
Planer can run with numpy or cupy backend, by default, cellpose-planer try to use cupy backend, if failed, use numpy backend. But we can change the backend manually. (if you switch backend, the net loaded befor would be useless, reload them pleanse)
```python
import cellpose-planer as cellpp

# use numpy and scipy as backend
import numpy as np
import scipy.ndimage as ndimg
cellpp.engine(np, ndimg)

# use cupy and cupy.scipy as backend
import cupy as cp
import cupyx.scipy.ndimage as cpimg
cellpp.engine(cp, cpimg)
```
here we time a 1024x1024 image on I7 CPU and 2070 GPU.
```
user switch engine: numpy
    net cost: 11.590
    flow cost: 0.0797

user switch engine: cupy
    net cost: 0.0139
    flow cost: 0.009
```

# Model deducing and releasing
Planer only has forward, so we need train the models in torch. then deduc it in planer.

## deduce from torch
```python
# train in cellpose with torch, and export torch as onnx file.
from planer import onnx2planer
onnx2planer(xxx.onnx)
```
then you would get a json file (graph structure), and a npy file (weights).

## model releasing
if you want to share your model in cellpose-planer, just upload the json and npy file generated upon to any public container, then append a record in the **models list** tabel below, and give a pull request.
*infact, when we call cellpp.search_models, cellpp pull the text below and parse them.*

## models list
| model name | auther | description | url |
| --- | --- | --- | --- |
| cyto_0  | carsen-stringer | [for cell cyto segmentation](http://www.cellpose.org/) | [download](http://release.imagepy.org/cellpose-planer/cyto_0.npy) |
| cyto_1  | carsen-stringer | [for cell cyto segmentation](http://www.cellpose.org/) | [download](http://release.imagepy.org/cellpose-planer/cyto_1.npy) |
| cyto_2  | carsen-stringer | [for cell cyto segmentation](http://www.cellpose.org/) | [download](http://release.imagepy.org/cellpose-planer/cyto_2.npy) |
| cyto_3  | carsen-stringer | [for cell cyto segmentation](http://www.cellpose.org/) | [download](http://release.imagepy.org/cellpose-planer/cyto_3.npy) |
| nuclei_0  | carsen-stringer | [for cell nuclear segmentation](http://www.cellpose.org/) | [download](http://release.imagepy.org/cellpose-planer/nuclei_0.npy) |
| nuclei_1  | carsen-stringer | [for cell nuclear segmentation](http://www.cellpose.org/) | [download](http://release.imagepy.org/cellpose-planer/nuclei_1.npy) |
| nuclei_2  | carsen-stringer | [for cell nuclear segmentation](http://www.cellpose.org/) | [download](http://release.imagepy.org/cellpose-planer/nuclei_2.npy) |
| nuclei_3  | carsen-stringer | [for cell nuclear segmentation](http://www.cellpose.org/) | [download](http://release.imagepy.org/cellpose-planer/nuclei_3.npy) |

 *cellpp.search_models function pull the text below and parse them, welcom to release your models here!*

 ## Use cellpose-planer as ImagePy plugins
 cellpose-planer can also start as ImagePy's plugins. supporting interactive and bat processing.
 ![image](https://user-images.githubusercontent.com/24822467/111069844-ce339000-8483-11eb-9dce-caa8f6ab80af.png)