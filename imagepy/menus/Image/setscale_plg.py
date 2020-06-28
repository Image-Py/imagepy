from sciapp.action import Simple
import numpy as np

class Plugin(Simple):
    title = 'Scale And Unit'
    note = ['all']
    
    para = {'k':1.0, 'unit':'pix', 'kill':False, 'recent':'Recent'}
    view = [(float, 'k', (0,1000000), 2, 'per', 'pix'),
            (str, 'unit', 'unit', ''),
            (bool, 'kill', 'kill scale')]
    

    def run(self, ips, imgs, para = None):
        if para['kill'] : ips.unit = 1, 'pix'
        else : ips.unit = para['k'], para['unit']