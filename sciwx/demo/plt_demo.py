import sys
sys.path.append('../../')

from skimage.data import astronaut, camera
from sciwx import plt
print(plt, '=========')

import numpy as np
import pandas as pd

if __name__ == '__main__':
    plt.imshow(camera(), cn=0)
    
    plt.imstackshow([astronaut(), 255-astronaut()], cn=(0,1,2))
    
    plt.tabshow(pd.DataFrame(np.zeros((100,5))))
    
    plt.txtshow('abcdefg')
    
    plt.mdshow('#Markdown\n## paragraph')
    
    fg = plt.figure()
    ax = fg.add_subplot()
    ax.plot(np.random.rand(100))

    #mesh = plt.meshshow()
    #vts, fs, ns, cs = plt.build_ball((100,100,100),50, (1,0,0))
    #mesh.add_surf('ball',vts, fs, ns, cs)

    plt.parashow({'c':(255,0,0)}, [('color', 'c', 'select', 'color')], False)
    plt.show()
