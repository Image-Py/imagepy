import matplotlib.pyplot as plt
import numpy as np
import skimage.io as io
import skimage.transform as transform
from scipy.signal import convolve
from scipy.signal import medfilt2d
from scipy.sparse import spdiags
from scipy.sparse.linalg import cg
from skimage import img_as_float

npa = np.array

def rgb2ycbcr(img):
    origT = npa([[65.481,128.553,24.966],[-37.797,-74.203,112],[112,-93.786,-18.214]])
    oriOffset = npa([[16,128,128]]).transpose()

    if img.dtype.name == 'uint8':
        t = 1
        offset = 1.0/255
    elif img.dtype.name == 'float64':
        t = 1.0 / 255
        offset = 1.0/255
    elif img.dtype.name == 'uint16':
        t = 257.0/65535
        offset = 257

    T = origT * t
    Offset = oriOffset * offset

    ycbcr = np.zeros(img.shape, dtype=img.dtype)
    for p in range(3):
        ycbcr[:,:,p] = T[p,0]*img[:,:,0] + T[p,1]*img[:,:,1]+T[p,2]*img[:,:,2]+Offset[p]

    return ycbcr

def ycbcr2rgb(img):
    origT = npa([[65.481, 128.553, 24.966], [-37.797, -74.203, 112], [112, -93.786, -18.214]])
    oriOffset = npa([[16, 128, 128]]).transpose()
    tinv = np.linalg.inv(origT)
    if img.dtype.name == 'uint8':
        t = 255
        offset = 255
    elif img.dtype.name == 'float64':
        t = 255
        offset = 1
    elif img.dtype.name == 'uint16':
        t = 65535 / 257.0
        offset = 65535

    T = tinv * t
    Offset = offset * tinv.dot(oriOffset)

    rgb = np.zeros(img.shape, dtype=img.dtype)
    for p in range(3):
        rgb[:, :, p] = T[p, 0] * img[:, :, 0] + T[p, 1] * img[:, :, 1] + T[p, 2] * img[:, :, 2] - Offset[p]

    if img.dtype.name == 'float64':
        rgb[rgb>1] = 1
        rgb[rgb<0] = 0
    return rgb

def imshow(I):
    io.imshow(I)

def histeq(img, nbr_bins=256):
    """ Histogram equalization of a grayscale image. """

    # 获取直方图p(r)
    imhist, bins = np.histogram(img.flatten(), nbr_bins, normed=True)

    # 获取T(r)
    cdf = imhist.cumsum()  # cumulative distribution function
    cdf = 255 * cdf / cdf[-1]

    # 获取s，并用s替换原始图像对应的灰度值
    result = np.interp(img.flatten(), bins[:-1], cdf)

    return result.reshape(img.shape), cdf

def natural_histogram_matching(img):

    img_map = npa(range(257))/256.0
    ho = np.zeros(256)
    po = np.zeros(256)
    for i in range(256):
        f = (img>=img_map[i]) & (img <= img_map[i+1])
        po[i] = np.sum(f)
    po = po / np.sum(po)
    ho[0] = po[0]
    # for i in range(1, 256):
    #     ho[i] = ho[i - 1] + po[i]
    ho = np.cumsum(po)
    p1 = lambda x: (1 / 9.0) * np.exp(-(255 - x) / 9.0)
    p2 = lambda x: (1.0 / (225 - 105)) * (x >= 105 and x <= 225)
    p3 = lambda x: (1.0 / np.sqrt(2 * np.pi * 11)) * np.exp(-((x - 90) ** 2) / float((2 * (11 ** 2))))
    p = lambda x: (76 * p1(x) + 22 * p2(x) + 2 * p3(x)) * 0.01
    prob = np.zeros(256)
    histo = np.zeros(256)
    total = 0
    for i in range(256):
        prob[i] = p(i)
        total = total + prob[i]
    prob = prob / np.sum(prob)

    histo[0] = prob[0]
    for i in range(1, 256):
        histo[i] = histo[i - 1] + prob[i]

    Iadjusted = np.zeros((img.shape[0], img.shape[1]))
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            ind = np.where(img_map>=img[x, y])[0][0]
            histogram_value = ho[ind]
            i = np.argmin(np.absolute(histo - histogram_value))
            Iadjusted[x, y] = i

    Iadjusted = np.float64(Iadjusted) / 255.0
    return Iadjusted

def pencil_drawing(img, ks, width, dirNum, gammaS, gammaI, pencil):
    print(img.shape)
    """
    Generate the pencil drawing I based on the method described in
    "Combining Sketch and Tone for Pencil Drawing Production" Cewu Lu, Li Xu, Jiaya Jia
    International Symposium on Non-Photorealistic Animation and Rendering (NPAR 2012), June, 2012
    :param img: the input image.
    :param ks: the length of convolution line.
    :param width: the width of the stroke.
    :param dirNum: the number of directions.
    :param gammaS: the darkness of the stroke.
    :param gammaI: the darkness of the resulted image.
    :return: I
    """
    im = img_as_float(img)

    # Convert from rgb to yuv when nessesary
    if len(im.shape) == 3:
        H, W, sc = im.shape
        if sc == 3:
            yuvIm = rgb2ycbcr(im)
            lumIm = yuvIm[:, :, 0]
        else:
            lumIm = im
            sc = 1
    else:
        H, W = im.shape
        lumIm = im
        sc = 1

    # Generate the stroke map
    s = genStroke(lumIm, ks, width, dirNum)**(gammaS)  # darken the result by gamma

    # Generate the tone map
    j = genToneMap(lumIm)**(gammaI)  # darken the result by gamma

    # plt.figure(1)
    # plt.imshow(j)
    # axes = plt.subplot(111)
    # axes.set_xticks([])
    # axes.set_yticks([])
    # plt.show()

    # Read the pencil texture

    p = io.imread('C:/Users/54631/Documents/PencilDrawing_python3/pencils/pencil1.jpg', True)
    # p = img_as_float(p)
    # Generate the pencil map
    t = genPencil(lumIm, p, j)
    # Compute the result
    lumIm = s*t

    if sc == 3:
        yuvIm[:,:, 0] = lumIm
        I = ycbcr2rgb(yuvIm)
    else:
        I = lumIm

    # s = np.loadtxt('s.txt')
    # j = genToneMap(lumIm) ** (gammaI)
    return I

def genStroke(im, ks, width, dirNum):
    """
      Compute the stroke structure 'S'

    :param im:  input image ranging value from 0 to 1.
    :param ks: kernel size.
    :param width: width of the strocke
    :param dirNum: number of directions.
    :return:
    """
    # Initialization
    h = im.shape[0]
    w = im.shape[1]
    im = im.reshape((h, w))
    # Smoothing
    im = medfilt2d(im, (3, 3))

    # Image gradient

    imX = np.hstack((np.abs(im[:, :-1] - im[:, 1:]), np.zeros((h, 1))))
    imY = np.vstack((np.abs(im[:-1, :] - im[1:, :]), np.zeros((1, w))))

    imEdge = imX + imY
    #
    # response = np.zeros((dirNum, height, width))
    # L = get_eight_directions(2 * ks + 1)
    # for n in range(dirNum):
    #     ker = rotate_img(kernel_Ref, n * 180 / dirNum)
    #     response[n, :, :] = cv2.filter2D(img, -1, ker)
    #
    # Cs = np.zeros((dirNum, height, width))
    # for x in range(width):
    #     for y in range(height):
    #         i = np.argmax(response[:, y, x])
    #         Cs[i, y, x] = img_gredient[y, x]
    #
    # spn = np.zeros((8, img.shape[0], img.shape[1]))

    # Convolution kernel with horizontal direction
    kerRef = np.zeros((ks * 2 + 1, ks * 2 + 1))
    kerRef[ks, :] = 1

    # Classification
    response = np.zeros((h, w, dirNum))

    for i in range(dirNum):
        ker = transform.rotate(kerRef, angle=i * 180.0 / dirNum, resize=False)
        response[:, :, i] = convolve(imEdge, ker, 'same')

    c = np.zeros((h, w, dirNum))
    for x in range(w):
        for y in range(h):
            i = np.argmax(response[y, x, :])
            c[y, x, i] = imEdge[y, x]

    spn = np.zeros((h, w, dirNum))
    for n in range(width):
        if (ks - n) >= 0:
            kerRef[ks - n, :] = 1
        if (ks + n) < ks * 2:
            kerRef[ks + n, :] = 1

    kerRef = np.zeros((2 * ks + 1, 2 * ks + 1))
    kerRef[ks, :] = 1

    for i in range(dirNum):
        ker = transform.rotate(kerRef, angle=i * 180.0 / dirNum, resize=False)
        # ker = rotate_img(kernel_Ref, i * 180 / dirNum)
        # spn[i] = cv2.filter2D(c[i], -1, ker)
        spn[:,:,i] = convolve(c[:,:,i], ker, mode='same')
    sp = np.sum(spn, axis=2)
    sp = (sp - np.min(sp)) / (np.max(sp) - np.min(sp))
    s = 1 - sp

    return s

def genToneMap(im):
    # Parameters
    ub = 225
    ua = 105

    p = np.zeros(256)
    p[ua: ub + 1] = 1.0 / (ub - ua)

    # Smoothing
    im = medfilt2d(im, [5,5]);

    # Histgram matching

    j = natural_histogram_matching(im)

    # Smoothing
    g = np.ones((10,10))/100
    j = convolve(j, g, 'same')

    j[j>1.0] = 1
    j[j<0.0] = 0
    return j

def genPencil(im, p, j):
    """
    Compute the pencil map 'T'
    :param im: input image ranging value from 0 to 1.
    :param P: the pencil texture.
    :param J: the tone map.
    :return:
    """
    # Parameters
    theta = 0.2
    if len(im.shape) == 2:
        sc = 1
        h, w = im.shape
    elif len(im.shape) == 3:
        h, w, sc = im.shape

    # Initialization
    p = transform.resize(p, (h,w))
    p = p.reshape((1,h * w))
    logP = np.log(p)
    logP = spdiags(logP, [0], h * w, h * w)
    j = transform.resize(j, (h, w))
    j = j.reshape((h * w, 1))

    logJ = np.log(j)

    e = np.ones((1, h * w))
    dx = spdiags(np.vstack((-e, e)), npa([0, h]), h * w, h * w)
    dy = spdiags(np.vstack((-e, e)), npa([0, 1]), h * w, h * w)
    # Compute matrix A and b
    b = logP.transpose().dot(logJ)
    A = theta * (dx.dot(dx.transpose()) + dy.dot(dy.transpose())) + logP.transpose().dot(logP)
    # Conjugate gradient
    beta, info = cg(A, b, tol=1e-6, maxiter=60)
    beta = beta.reshape((h, w))
    p = p.reshape((h, w))
    t = np.power(p, beta)

    return t

from imagepy.core.engine import Filter
class Plugin(Filter):
    """Gaussian: derived from imagepy.core.engine.Filter """
    title = 'Pencil Draw'
    note = ['rgb', 'not_channel', 'auto_msk', 'auto_snap', 'preview']
    para = {'ks':8,'width':1,'dirNum':8,'gammaS':1.0,'gammaI':1.0,'stroke':'strok1'}

    view = [(int, (0,30), 0,  'ks', 'ks', 'pix'),
            (int, (0,30), 0,  'width', 'width', 'pix'),
            (int, (0,30), 0,  'dirNum', 'dirNum', 'pix'),
            (float, (0,30), 1,  'gammaS', 'gammaS', 'pix'),
            (float, (0,30), 1,  'gammaI', 'gammaI', 'pix'),
            (list, ['strok1','strok2','strok3'], int, 'list', 'l', 'u')]

    def run(self, ips, snap, img, para = None):
        img[:] = pencil_drawing(snap, para['ks'], para['width'], para['dirNum'], 
            para['gammaS'], para['gammaI'], para['stroke']) * 255

if __name__ == '__main__':

    im = io.imread('inputs/2--31.jpg')
    print(im.shape)
    I = pencil_drawing(im, 8, 1, 8, 1.0, 1.0)
    print(I.shape)
    io.imsave('lena_pencil.jpg', I)
    plt.figure(0)

    plt.imshow(I)

    axes = plt.subplot(111)
    axes.set_xticks([])
    axes.set_yticks([])
    plt.show()