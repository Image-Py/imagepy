from sciapp.action import dataio


def readmc(path):
    with open(path) as f: return f.readlines()

dataio.ReaderManager.add('mc', readmc, 'mc')

class Macros(dataio.Reader):
    title = 'Run Macros'
    tag = 'mc'
    filt = ['MC']

def readwf(path):
    with open(path) as f: return f.read()

dataio.ReaderManager.add('wf', readwf, 'wf')

class WorkFlow(dataio.Reader):
    title = 'Run WorkFlow'
    tag = 'wf'
    filt = ['wf']

plgs = [Macros, WorkFlow]