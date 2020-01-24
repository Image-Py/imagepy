"""
Created on Sun Jan 23 11:53:00 2020
@author: weisong
"""
from imagepy.core.engine import Simple
import numpy as np
from imagepy import IPy
from scipy.optimize import curve_fit
# from .histogram_plg import like
from skimage.exposure import histogram_matching

def simple_ratio(imgs):
    x,y,z = imgs.shape
    ref = imgs[:,:,1].sum()/x/y
    for i in range(z-1):
        imgs[:,:,i+1] *= (ref/(imgs[:,:,i+1].sum()
            /x/y)).astype(imgs.dtype)
    return imgs
def exponential_fit(imgs):
    imgs_=imgs.astype('float32')
    x,y,z = imgs.shape
    t = np.linspace(0, z-1, z)
    intensity = (imgs.sum(1).sum(0)/x/y)
    popt, pcov = curve_fit(exponential_func, t, intensity)
    for i in range(z-1):
        ratio=exponential_func(0, popt[0], popt[1], popt[2])/ \
        exponential_func(i+1, popt[0], popt[1], popt[2])
        imgs_[:,:,i+1] *= ratio
    return imgs_.astype(imgs.dtype)

def histogram_match(imgs):    
    x,y,z = imgs.shape
    for i in range(z-1):
        imgs[:,:,i+1] = histogram_matching.match_histograms(
            imgs[:,:,i+1],imgs[:,:,0])
    return imgs 

def exponential_func(t, ref, k, offset):
    return ref * np.exp(- k * t) + offset

class Plugin(Simple):
    title = 'Bleach Correction'
    note = ['8-bit','16-bit','stack']
    para = {'Method':'Simple ratio', 'Background':0}
    view = [(list, 'Method', 
    	['Simple ratio','Exponential fit','Histogram match'], 
    	str, 'Correction Method',''),
    (int,'Background',(0,65535),0,'Background intensity','')]

    def run(self, ips, imgs, para = None):
        Bconstant = para['Background']
        imgs_= imgs.transpose(1,2,0)
        if Bconstant != 0:
            for i in range (z):
                imgs_[:,:,i] -= Bconstant
            imgs_ = np.maximum(imgs_, 0)
        print (para['Method'])
        if para['Method'] == 'Simple ratio':
            imgs_=simple_ratio(imgs_)
            IPy.show_img(imgs_.transpose(2,0,1),'Corrected %s'%ips.title)
        if para['Method'] == 'Exponential fit':
            imgs_=exponential_fit(imgs_)
            IPy.show_img(imgs_.transpose(2,0,1),'Corrected %s'%ips.title)
        if para['Method'] == 'Histogram match':
            imgs_=histogram_match(imgs_)
            IPy.show_img(imgs_.transpose(2,0,1),'Corrected %s'%ips.title)



