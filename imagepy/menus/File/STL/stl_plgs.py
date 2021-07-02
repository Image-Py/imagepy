from sciapp.action import dataio
from sciapp.object import Mesh
import numpy as np
import trimesh

def readSTL(path):
    mesh = trimesh.load(path)
    vts = np.array(mesh.vertices)
    fs = np.array(mesh.faces)
    return Mesh(vts, fs, vts[:,2], cmap='jet', mode='grid')

dataio.ReaderManager.add('stl', readSTL, 'mesh')
# dataio.WriterManager.add('stl', imsave, 'mesh')

class OpenFile(dataio.Reader):
    title = 'STL Open'
    tag = 'mesh'
    filt = ['stl','STL']

# class SaveFile(dataio.ImageWriter):
#     title = 'JPG Save'
#     tag = 'img'
#     filt = ['JPG','JPEG']

plgs = [OpenFile]