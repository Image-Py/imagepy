from sciapp import App, Source
from imagepy import root_dir
from .startup import load_plugins

class Console(App):
    def __init__( self ):
        App.__init__(self, False)

    def load_plugins(self, plgs=None):
        if plgs is None: plgs = load_plugins()[0]
        if isinstance(plgs, tuple):
            if callable(plgs[1]): 
                name, plg = plgs[:2]
                self.add_plugin(name, plg, 'plugin')
            else: self.load_plugins(plgs[1])
        if isinstance(plgs, list):
            for i in plgs: self.load_plugins(i)

if __name__ == '__main__':
    import numpy as np
    import pandas as pd
