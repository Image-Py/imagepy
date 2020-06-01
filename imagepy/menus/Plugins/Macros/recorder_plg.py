from imagepy.core.util import fileio
from sciapp import Source

def readmc(path):
    with open(path) as f:
        return f.readlines()

class Plugin(fileio.Reader):
    title = 'Run Macros'
    tag = 'macros'
    filt = ['MC']

Source.manager('reader').add(name='mc', tag='macros', obj=readmc)