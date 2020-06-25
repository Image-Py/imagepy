from imagepy.core.engine import dataio
from sciapp import Source

def readmc(path):
    with open(path) as f: return f.readlines()

Source.manager('reader').add('mc', readmc, 'mc')

class Macros(dataio.Reader):
    title = 'Run Macros'
    tag = 'mc'
    filt = ['MC']

def readwf(path):
    with open(path) as f: return f.read()

Source.manager('reader').add('wf', readwf, 'wf')

class WorkFlow(dataio.Reader):
    title = 'Run WorkFlow'
    tag = 'wf'
    filt = ['wf']

plgs = [Macros, WorkFlow]