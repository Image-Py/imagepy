from core.engines import Filter
from skimage.morphology import skeletonize
from skimage.morphology import medial_axis

class Skeleton(Filter):
    title = 'Skeleton'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #process
    def run(self, ips, snap, img, para = None):
        img[:] = skeletonize(snap>0)
        img *= 255

class MedialAxis(Filter):
	title = 'Medial Axis'
	note = ['all', 'auto_msk', 'auto_snap', 'preview']
	para = {'dis':False}
	view = [(bool,'distance transform', 'dis')]

	#process
	def run(self, ips, snap, img, para = None):
		rst = medial_axis(snap>0,return_distance=para['dis'])
		if not para['dis']:
			img[:] = rst
			img *= 255
		else:
			img[:] = rst[0]
			img *= rst[1]

plgs = [Skeleton, MedialAxis]