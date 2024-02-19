"""
Created on Sun Jan 23 11:53:00 2020
@author: weisong
"""
from sciapp.action import Simple
import numpy as np
from scipy.optimize import curve_fit
from skimage.exposure import histogram_matching
import matplotlib.pyplot as plt 
import pandas as pd

def copy(imgs):
    if isinstance(imgs, list):
        return [np.zeros_like(imgs[0])]
    else: return np.zeros_like(imgs)

def exponential_func(t, ref, k, offset):
    return ref * np.exp(- k * t) + offset

def simple_ratio(imgs, back=0, inplace=True, out=print):
    if isinstance(back, int): back=imgs[back]
    buf = imgs if inplace else copy(imgs)
    z, (x, y) = len(imgs), imgs[0].shape 
    values, k0 = np.zeros(z), back.sum()/x/y
    lim = 255 if imgs[0].dtype.type==np.uint8 else 65535
    for i in range(z):
        values[i] = imgs[i].sum()/x/y 
        np.clip(imgs[i], 0, lim/(k0/values[i]), out=buf[i])
        np.multiply(buf[i], k0/values[i], out=buf[i], casting='unsafe')
        out(i, z)
    return buf, values, k0/values

def exponential_fit(imgs, inplace=True, out=print):
    buf = imgs if inplace else copy(imgs)
    z, (x, y) = len(imgs), imgs[0].shape 
    intensity = [i.sum()/x/y for i in imgs]
    popt, pcov = curve_fit(exponential_func, np.arange(z), intensity)
    k0 = exponential_func(0, popt[0], popt[1], popt[2])
    rst = exponential_func(np.arange(z), popt[0], popt[1], popt[2])
    lim = 255 if imgs[0].dtype.type==np.uint8 else 65535
    for i in range(z):
        np.clip(imgs[i], 0, lim/(rst[i]/k0), out=buf[i])
        np.multiply(buf[i], rst[i]/k0, out=buf[i], casting='unsafe')
        out(i, z)
    return buf, popt, intensity, rst

def histogram_match(imgs, back=0, inplace=True, out=print): 
    if isinstance(back, int): back=imgs[back]   
    buf = imgs if inplace else copy(imgs)
    z, (x, y) = len(imgs), imgs[0].shape 
    for i in range(z):
        buf[i] = histogram_matching.match_histograms(imgs[i], back)
        out(i, z)
    return buf

def plot(popt, intensity, fitresult):
    t = np.arange(len(intensity))
    plt.plot(t, intensity,'r.',label='Experiment')
    plt.plot(t, fitresult,'k',label=
        'Exponential fitted curve\n y=a*exp(-bx)+c\n a=%f\n b=%f\n c=%f'%tuple(popt))
    plt.title('Exponential fitted result')
    plt.legend()
    plt.show()

def plot_after(popt, intensity, fitresult):
    import wx
    wx.CallAfter(plot, popt, intensity, fitresult)

class Plugin(Simple):
    title = 'Bleach Correction'
    note = ['8-bit','16-bit','stack']
    para = {'method':'Simple Ratio', 'new':True}
    view = [(list, 'method', ['Simple Ratio','Exponential Fit','Histogram Match'], 
        str, 'Correction Method',''),
            (bool, 'new', 'show new window'),
            ('lab', 'lab', 'Correct intensity based on your current slice!')]
            
    def run(self, ips, imgs, para = None):
        if para['method'] == 'Simple Ratio':
            rst, value, ratio = simple_ratio(imgs, ips.img, not para['new'], self.progress)
            body = pd.DataFrame({'Mean value': value, 'Ratio':ratio})
            IPy.show_table(body, '%s-simple ratio'%ips.title)
        if para['method'] == 'Exponential Fit':
            rst, popt, intensity, fitrst = exponential_fit(imgs, not para['new'], self.progress)
            plot_after(popt, intensity, fitrst)
            body = {'Intensity':intensity, 'Fit':fitrst}
            IPy.show_table(pd.DataFrame(body), '%s-exp fit'%ips.title)
        if para['method'] == 'Histogram Match':
            rst = histogram_match(imgs, ips.img, not para['new'], self.progress)
        if para['new']:  IPy.show_img(rst, '%s-corrected'%ips.title)