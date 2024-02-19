import numpy as np
from numba import jit
from scipy.ndimage import generate_binary_structure

def neighbors(shape):
	dim = len(shape)
	block = generate_binary_structure(dim, 1)
	block[tuple([1]*dim)] = 0
	idx = np.where(block>0)
	idx = np.array(idx, dtype=np.uint8).T
	idx = np.array(idx-[1]*dim)
	acc = np.cumprod((1,)+shape[::-1][:-1])
	return np.dot(idx, acc[::-1])

@jit(nopython=True)
def stair(img, low=0, high=255, step=20):
	img = img.ravel()
	for i in range(len(img)):
		if img[i]<low:img[i]=low
		elif img[i]>high:img[i]=high
		else: img[i] = (img[i]-low)//step*step+low

@jit(nopython=True) # my mark
def isoline_jit(img, mark, nbs):
	for p in range(len(img)):
		if mark[p]==0:continue
		s = 0
		for dp in nbs:
		    if img[p] > img[p+dp]:s+=1
		if s==0:mark[p] = 0

def isoline(img, low=0, high=255, step=20):
	stair(img, low, high, step)
	nbs = neighbors(img.shape)
	mark = np.zeros_like(img, dtype=np.uint8)
	mark[tuple([slice(1,-1)]*img.ndim)] = 255
	isoline_jit(img.ravel(), mark.ravel(), nbs)
	return mark