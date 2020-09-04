from skimage.io import imread
from skimage.data import astronaut, camera
from scipy.ndimage import map_coordinates
import numpy as np
# import matplotlib.pyplot as plt

def linear_polar(img, o=None, r=None, order=1, cont=0, output=None):
    if o is None: o = np.array(img.shape[:2])/2 - 0.5
    if r is None: r = (np.array(img.shape[:2])**2).sum()**0.5/2
    cns = 1 if img.ndim == 2 else img.shape[2]
    if output is None:
        shp = int(round(r)), int(round(r*2*np.pi))
        output = np.zeros(shp+(cns,), dtype=img.dtype)
    elif isinstance(output, tuple):
        output = np.zeros(output+(cns,), dtype=img.dtype)
    out_h, out_w, _ = output.shape
    out_img = np.zeros((out_h, out_w), dtype=img.dtype)
    rs = np.linspace(0, r, out_h)
    ts = np.linspace(0, np.pi*2, out_w)
    xs = rs[:,None] * np.cos(ts) + o[1]
    ys = rs[:,None] * np.sin(ts) + o[0]
    img = img.reshape(img.shape[:2]+(-1,))
    for i in range(cns):
        map_coordinates(img[:,:,i], (ys, xs), order=order, output=output[:,:,i])
    return output.reshape(output.shape[:2]) if output.shape[2]==1 else output

def polar_linear(img, o=None, r=None, order=1, cont=0, output=None):
    if r is None: r = img.shape[0]
    cns = 1 if img.ndim == 2 else img.shape[2]
    if output is None:
        output = np.zeros((r*2, r*2, cns), dtype=img.dtype)
    elif isinstance(output, tuple):
        output = np.zeros(output+(cns,), dtype=img.dtype)
    if o is None: o = np.array(output.shape[:2])/2 - 0.5
    out_h, out_w, _ = output.shape
    ys, xs = np.mgrid[:out_h, :out_w] - o[:,None,None]
    rs = (ys**2+xs**2)**0.5
    ts = np.arccos(xs/rs)
    ts[ys<0] = np.pi*2 - ts[ys<0]
    ts *= (img.shape[1]-1)/(np.pi*2)
    img = img.reshape(img.shape[:2]+(-1,))
    for i in range(cns):
        map_coordinates(img[:,:,i], (rs, ts), order=order, output=output[:,:,i])
    return output.reshape(output.shape[:2]) if output.shape[2]==1 else output


if __name__ == '__main__':
    img = camera()
    ax = plt.subplot(311)
    ax.imshow(img)
    out = linear_polar(img)
    ax = plt.subplot(312)
    ax.imshow(out)
    img = polar_linear(out, output=img.shape[:2])
    ax = plt.subplot(313)
    ax.imshow(img)
    plt.show()