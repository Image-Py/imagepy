# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 00:56:00 2016
@author: yxl
"""

from imagepy import IPy
import numpy as np
from imagepy.core.engine import Filter, Simple
from imagepy.core.manager import WindowsManager

def like(hist1, hist2):
    hist1 = np.cumsum(hist1)/hist1.sum()
    hist2 = np.cumsum(hist2)/hist2.sum()
    hist = np.zeros(256, dtype=np.uint8)
    i1, i2, s = 0, 0, 0
    while i2<256:
        while i1<256 and hist2[i2]>hist1[i1]:i1+=1
        hist[i2] = i1
        i2+=1
    return hist

def match(img1, img2):
    if img1.ndim == 2:
        temp = np.histogram(img1, np.arange(257))[0]
        if img2.ndim == 2:
            hist = np.histogram(img2, np.arange(257))[0]
            ahist = like(temp, hist)
            img2[:] = ahist[img2]
        if img2.ndim == 3:
            for i in range(3):
                hist = np.histogram(img2[:,:,i], np.range(257))[0]
                ahist = like(temp, hist)
                img2[:,:,i] = ahist[img2[:,:,i]]
    elif img1.ndim == 3:
        if img2.ndim == 2:
            temp = np.histogram(img1, np.arange(257))[0]
            hist = np.histogram(img2, np.arange(257))[0]
            ahist = like(temp, hist)
            img2[:] = ahist[img2]
        if img2.ndim == 3:
            for i in range(3):
                temp = np.histogram(img1[:,:,i], np.arange(257))[0]
                hist = np.histogram(img2[:,:,i], np.arange(257))[0]
                ahist = like(temp, hist)
                img2[:,:,i] = ahist[img2[:,:,i]]

class Normalize(Filter):
    title = 'Histogram Normalize'
    note = ['8-bit', 'rgb', 'auto_snap']

    def run(self, ips, snap, img, para = None):
        temp = np.ones(256)
        hist = np.histogram(img, np.arange(257))[0]
        ahist = like(temp, hist)
        img[:] = ahist[img]
        
class Match(Simple):
    """Calculator Plugin derived from imagepy.core.engine.Simple """
    title = 'Histogram Match'
    note = ['all']
    para = {'img1':'', 'img2':''}
    
    def load(self, ips):
        titles = WindowsManager.get_titles()
        self.para['img1'] = titles[0]
        self.para['img2'] = titles[0]
        Match.view = [(list, titles, str, 'template', 'img1', ''),
                       (list, titles, str, 'object', 'img2', '')]
        return True
    
    def run(self, ips, imgs, para = None):
        ips1 = WindowsManager.get(para['img1']).ips
        ips2 = WindowsManager.get(para['img2']).ips
        ips2.snapshot()

        img = ips1.img
        imgs = ips2.imgs

        sl1, sl2 = ips1.get_nslices(), ips2.get_nslices()
        cn1, cn2 = ips1.get_nchannels(), ips2.get_nchannels()
        if not(ips1.img.dtype == np.uint8 and ips2.img.dtype == np.uint8):
            IPy.alert('Two image must be type of 8-bit or rgb!')
            return
        
        for i in range(sl2):
            self.progress(i, sl2)
            match(img, imgs[i])
        ips2.update = 'pix'

plgs = [Normalize, Match]


'''

import java.awt.event.MouseListener;

import ij.*;
import ij.gui.GenericDialog;
import ij.plugin.PlugIn;
import ij.plugin.filter.PlugInFilter;
import ij.plugin.frame.PlugInFrame;
import ij.process.ByteProcessor;
import ij.process.ColorProcessor;
import ij.process.ImageProcessor;



public class Histogram_Match implements PlugInFilter{
    
    private GenericDialog gd;
    @Override
    public void run(ImageProcessor ip) {
        // TODO Auto-generated method stub
        String title = gd.getNextChoice();
        ImageProcessor temp = WindowManager.getImage(title).getProcessor();
        match((ColorProcessor)temp,(ColorProcessor)ip);
    }

    @Override
    public int setup(String arg0, ImagePlus arg1) {
        // TODO Auto-generated method stub
        gd = new GenericDialog("IJ webcam plugin...");
        int[] wList = ij.WindowManager.getIDList();
        String[] titles = new String[wList.length];
        for (int i=0; i<wList.length; i++) 
            titles[i] = ij.WindowManager.getImage(wList[i]).getTitle();
        gd.addChoice("template", titles, titles[0]);    
        gd.showDialog();
        return PlugInFilter.DOES_RGB;
    }
    
    static float[] cdf(int[] h){
        int n=0;
        for(int i : h) n+=i;
        float[] P = new float[256];
        int c = h[0];
        P[0] = (float)c/n;
        for(int i=1;i<256;i++){
            c += h[i];
            P[i] = (float)c/n;
        } return P;
    }
    
    static int[] getTrans(int[] h1, int[] h2){
        float[] pa = cdf(h1);
        float[] pb = cdf(h2);
        int[] F = new int[257];
        float diff = 0;
        int i=0, j=0;
        for(;i<256;i++){
            for(;j<256 && pb[i]>pa[j];j++);
            F[i] = j;
            diff += (j-i)*(j-i)*(pb[i]-(i==0?0:pb[i-1]));
        } 
        F[256] = (int)diff;
        return F;
    }
    
    static void match(ImageProcessor ip, int[] hist){
        for(int i=0;i<ip.getPixelCount();i++)
            ip.set(i, hist[ip.get(i)]);
    }
    
    static void match(ColorProcessor cp1, ColorProcessor cp2){
        for(int i=1;i<=3;i++){
            ByteProcessor bp1 = new ByteProcessor(cp1.getWidth(), cp1.getHeight(), cp1.getChannel(i));
            ByteProcessor bp2 = new ByteProcessor(cp2.getWidth(), cp2.getHeight(), cp2.getChannel(i));
            int[] h1 = bp1.getHistogram();
            int[] h2 = bp2.getHistogram();
            int[] F = getTrans(h1, h2);
            match(bp2, F);
            cp2.setChannel(i, bp2);
        }
    }
    /**
     * @param args
     */
    public static void main(String[] args) {
        // TODO Auto-generated method stub
        new ij.ImageJ().show();
        ImagePlus ips1 = ij.IJ.openImage("C:/Users/yxl/Desktop/temp.jpg");
        ImagePlus ips2 = ij.IJ.openImage("C:/Users/yxl/Desktop/my.jpg");
        ips1.show();
        ips2.show();
        IJ.runPlugIn("Histogram_Match","");
        /*
         *      ColorProcessor cp1 = (ColorProcessor) ips1.getProcessor();
        ColorProcessor cp2 = (ColorProcessor) ips2.getProcessor();
        match(cp1,cp2);
        ips1 = ij.IJ.openImage("C:/Users/yxl/Desktop/my.jpg");
        ips1.show();
        ips2.show();
         */
    }

}
'''