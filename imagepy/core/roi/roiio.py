from .convert import roi2shape, shape2roi
import pickle
from shapely import wkt

def roi2wkt(roi): return wkt.dumps(roi2shape(roi))
def wkt2roi(con): return shape2roi(wkt.loads(con))

def readroi(path):
	f = open(path, 'rb')
	roi = pickle.load(f)
	f.close()
	return roi

def readwkt(path):
	f = open(path)
	roi = wkt2roi(f.read())
	f.close()
	return roi

def saveroi(roi, path):
	f = open(path, 'wb')
	pickle.dump(roi, f)
	f.close()

def savewkt(roi, path):
	f = open(path, 'w')
	f.write(roi2wkt(roi))
	f.close()
