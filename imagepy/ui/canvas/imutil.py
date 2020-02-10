import numpy as np
from scipy.ndimage import affine_transform
try: from numba import njit as jit
except:
    print('install numba may be several times faster!')
    jit = None
# jit = None
    
def affine_jit(img, m, offset, output_shape=0, output=0, order=0, prefilter=0):
    kr=m[0]; kc=m[1]; ofr=offset[0]; ofc=offset[1];
    for r in range(output_shape[0]):
        for c in range(output_shape[1]):
            rr = int(r*kr+ofr)
            cc = int(c*kc+ofc)
            output[r,c] = img[rr,cc]
if not jit is None: affine_transform = jit(affine_jit)

def blend(img, out, msk, mode):
    if mode=='set': out[:] = img
    if mode=='min': np.minimum(out, img, out=out)
    if mode=='max': np.maximum(out, img, out=out)
    if mode=='msk':
        msk = np.logical_not(msk)
        out.T[:] *= msk.T
        out += img
    if isinstance(mode, float):
        np.multiply(out, 1-mode, out=out, casting='unsafe')
        np.multiply(img, mode, out=img, casting='unsafe')
        out += img

if not jit is None:
    @jit
    def blend_set(img, out, msk, mode):
        for r in range(img.shape[0]):
            for c in range(img.shape[1]):
                out[r,c] = img[r,c]
    @jit
    def blend_min(img, out, msk, mode):
        for r in range(img.shape[0]):
            for c in range(img.shape[1]):
                out[r,c] = min(img[r,c], out[r,c])
    @jit
    def blend_max(img, out, msk, mode):
        for r in range(img.shape[0]):
            for c in range(img.shape[1]):
                out[r,c] = max(img[r,c], out[r,c])
    @jit
    def blend_msk(img, out, msk, mode):
        for r in range(img.shape[0]):
            for c in range(img.shape[1]):
                if img[r,c] != 0: out[r,c] = img[r,c]
    @jit
    def blend_mix(img, out, msk, mode):
        for r in range(img.shape[0]):
            for c in range(img.shape[1]):
                out[r,c] = img[r,c]*mode + out[r,c]*(1-mode)

    def blend_jit(img, out, msk, mode):
        if mode=='set': blend_set(img, out, msk, mode)
        if mode=='min': blend_min(img, out, msk, mode)
        if mode=='max': blend_max(img, out, msk, mode)
        if mode=='msk': blend_msk(img, out, msk, mode)
        if isinstance(mode, float): blend_mix(img, out, msk, mode)
    blend = blend_jit

def stretch(img, out, rg, log=False):
    if img.dtype==np.uint8 and not log and (rg==[(0,255)] or rg==(0,255)):
        out[:] = img
    elif not log:
        ptp = max(rg[1]-rg[0], 1e-6)
        np.clip(img, rg[0], rg[1], out=img)
        np.subtract(img, rg[0], out=img, casting='unsafe')
        np.multiply(img, 255/ptp, out=out, casting='unsafe')
    elif img.itemsize<3:
        length = 2**(img.itemsize*8)
        lut = np.arange(length, dtype=np.float32)
        if img.dtype in (np.int8, np.int16):
            lut[length//2:] -= length
        np.clip(lut, rg[0], rg[1], out=lut)
        np.subtract(lut, rg[0]-1, out=lut)
        ptp = np.log(max(rg[1]-rg[0]+1, 1+1e-6))
        np.log(lut, out=lut)
        lut *= 255/np.log(max(rg[1]-rg[0]+1, 1+1e-6))
        out[:] = lut[img]
    else:
        fimg = img.ravel().view(np.float32)
        fimg = fimg[:img.size].reshape(img.shape)
        np.clip(img, rg[0], rg[1], out=fimg)
        np.subtract(fimg, rg[0]-1, out=fimg)
        ptp = np.log(max(rg[1]-rg[0]+1, 1+1e-6))
        np.log(fimg, out=fimg)
        np.multiply(fimg, 255/ptp, out=out, casting='unsafe')

if not jit is None:
    @jit
    def stretch_linear(img, out, rg):
        ptp = max(rg[1]-rg[0], 1e-6)
        for r in range(img.shape[0]):
            for c in range(img.shape[1]):
                v = (img[r,c]-rg[0])/ptp*255
                out[r,c] = min(max(v, 0), 255)
    @jit
    def stretch_log(img, out, rg):
        ptp = 255/np.log(max(rg[1]-rg[0]+1, 1+1e-6))
        for r in range(img.shape[0]):
            for c in range(img.shape[1]):
                v = np.log(img[r,c]-rg[0]+1)*ptp
                out[r,c] = min(max(v, 0), 255)
    @jit
    def stretch_lut(img, out, lut):
        for r in range(img.shape[0]):
            for c in range(img.shape[1]):
                out[r,c] = lut[img[r,c]]
        
    def stretch_jit(img, out, rg, log=False):
        if img.dtype==np.uint8 and not log and (rg==[(0,255)] or rg==(0,255)):
            out[:] = img
        elif not log:
            stretch_linear(img, out, rg)
        elif img.itemsize<3:
            length = 2**(img.itemsize*8)
            lut = np.arange(length, dtype=np.float32)
            if img.dtype in (np.int8, np.int16):
                lut[length//2:] -= length
            np.clip(lut, rg[0], rg[1], out=lut)
            np.subtract(lut, rg[0]-1, out=lut)
            ptp = np.log(max(rg[1]-rg[0]+1, 1+1e-6))
            np.log(lut, out=lut)
            lut *= 255/np.log(max(rg[1]-rg[0]+1, 1+1e-6))
            stretch_lut(img, out, lut)
        else:
            stretch_log(img, out, rg)
            
    stretch = stretch_jit

def complex_norm(ori, real, img, out):
    np.abs(ori, out=out)
    return out

if not jit is None:
    @jit
    def complex_norm(ori, real, img, out):
        for r in range(img.shape[0]):
            for c in range(img.shape[1]):
                out[r,c] = (img[r,c]**2+real[r,c]**2)**0.5
        return out

def lookup(img, lut, out, mode='set'):
    blend(lut[img], out, img, mode)

if not jit is None:
    @jit
    def lookup_set(img, lut, out, mode):
        for r in range(img.shape[0]):
            for c in range(img.shape[1]):
                for i in (0,1,2):
                    out[r,c,i] = lut[img[r,c],i]
    @jit
    def lookup_min(img, lut, out, mode):
        for r in range(img.shape[0]):
            for c in range(img.shape[1]):
                for i in (0,1,2):
                    out[r,c,i] = min(lut[img[r,c],i], out[r,c,i])
    @jit
    def lookup_max(img, lut, out, mode):
        for r in range(img.shape[0]):
            for c in range(img.shape[1]):
                for i in (0,1,2):
                    out[r,c,i] = max(lut[img[r,c],i], out[r,c,i])
    @jit
    def lookup_msk(img, lut, out, mode):
        for r in range(img.shape[0]):
            for c in range(img.shape[1]):
                if img[r,c] != 0:
                    for i in (0,1,2): out[r,c,i] = 0
                for i in (0,1,2):
                    out[r,c,i] += lut[img[r,c],i]
    @jit
    def lookup_mix(img, lut, out, mode):
        for r in range(img.shape[0]):
            for c in range(img.shape[1]):
                for i in (0,1,2):
                    out[r,c,i] = lut[img[r,c],i]*mode + out[r,c,i]*(1-mode)

    def lookup_jit(img, lut, out, mode):
        if mode == 'set': lookup_set(img, lut, out, mode)
        if mode == 'msk': lookup_msk(img, lut, out, mode)
        if mode == 'max': lookup_max(img, lut, out, mode)
        if mode == 'min': lookup_min(img, lut, out, mode)
        if isinstance(mode, float): lookup_mix(img, lut, out, mode)
        
    lookup = lookup_jit

# mode: set, min, max, mix, nor
def mix_img(img, m, o, shp, buf, rgb, byt, rg=(0,255), lut=None, log=True, cns=0, mode='set'):
    if img is None: return
    img = img.reshape((img.shape[0], img.shape[1], -1))
    if isinstance(rg, tuple): rg = [rg]*img.shape[2]

    if isinstance(cns, int):
        if np.iscomplexobj(buf):
            affine_transform(img[:,:,0].real, m, o, shp, buf.real, 0, prefilter=False)
            affine_transform(img[:,:,0].imag, m, o, shp, buf.imag, 0, prefilter=False)
            buf = complex_norm(buf, buf.real, buf.imag, buf.real)
        else: affine_transform(img[:,:,cns], m, o, shp, buf, 0, prefilter=False)
        stretch(buf, byt, rg[cns], log)
        return lookup(byt, lut, rgb, mode)
    for i,v in enumerate(cns):
        if v==-1: rgb[:,:,i] = 0
        elif mode=='set' and img.dtype==np.uint8 and rg[v]==(0,255) and not log:
            affine_transform(img[:,:,v], m, o, shp, rgb[:,:,i], 0, prefilter=False)
        else:
            affine_transform(img[:,:,v], m, o, shp, buf, 0, prefilter=False)
            stretch(buf, byt, rg[v], log)
            blend(byt, rgb[:,:,i], byt, mode)

'''
rgb = np.array([[[0,0,0]]], dtype=np.uint8)
lut = np.array([[0,0,0]], dtype=np.uint8)
mix_img(img, (1,1), (0,0), (1,1), img, rgb, img, (0,255), lut, 0, 'set')
'''
