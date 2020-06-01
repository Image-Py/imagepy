import numpy as np

def cross(winbox, conbox):
    two = np.array([winbox, conbox])
    x1, y1 = two[:,:2].max(axis=0)
    x2, y2 = two[:,2:].min(axis=0)
    return [x1, y1, x2, y2]

def merge(winbox, conbox):
    two = np.array([winbox, conbox])
    x1, y1 = two[:,:2].min(axis=0)
    x2, y2 = two[:,2:].max(axis=0)
    return [x1, y1, x2, y2]

def multiply(rect, kx, ky):
    return rect * [kx, ky, kx, ky]

def layx(winbox, conbox):
    conw = conbox[2]-conbox[0]
    winw = winbox[2]-winbox[0]   
    if conw<winw:
        mid = (winbox[0]+winbox[2])/2
        conbox[0] = mid-conw/2
        conbox[2] = mid+conw/2
    elif conbox[0] > winbox[0]:
        conbox[0] = winbox[0]
        conbox[2] = conbox[0] + conw
    elif conbox[2] < winbox[2]:
        conbox[2] = winbox[2]
        conbox[0] = conbox[2] - conw

def layy(winbox, conbox):
    winh = winbox[3]-winbox[1]
    conh = conbox[3]-conbox[1] 
    if conh<winh:
        mid = (winbox[1]+winbox[3])/2
        conbox[1] = mid-conh/2
        conbox[3] = mid+conh/2
    elif conbox[1] > winbox[1]:
        conbox[1] = winbox[1]
        conbox[3] = conbox[1] + conh
    elif conbox[3] < winbox[3]:
        conbox[3] = winbox[3]
        conbox[1] = conbox[3] - conh

def lay(winbox, conbox):
    layx(winbox, conbox)
    layy(winbox, conbox)

def like(ori, cont, cell):
    kx = (cont[2]-cont[0])/(ori[2]-ori[0])
    ky = (cont[3]-cont[1])/(ori[3]-ori[1])
    ox = cont[0] - ori[0]*kx
    oy = cont[1] - ori[1]*kx
    return [cell[0]*kx+ox, cell[1]*ky+oy, 
        cell[2]*kx+ox, cell[3]*kx+oy]

def mat(ori, con, cell, cros):
    kx = (ori[2]-ori[0])/(con[2]-con[0])
    ky = (ori[3]-ori[1])/(con[3]-con[1])
    ox = (cros[1]-cell[1])*ky
    oy = (cros[0]-cell[0])*kx
    return (ox, oy), (kx, ky)