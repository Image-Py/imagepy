from imagepy.core.util import fileio
from imagepy.core.manager import ReaderManager

def readmc(path):
    with open(path) as f:
        return f.readlines()

class Plugin(fileio.Reader):
    title = 'Run Macros'
    tag = 'macros'
    filt = ['MC']

ReaderManager.add(name='mc', tag='macros', obj=readmc)