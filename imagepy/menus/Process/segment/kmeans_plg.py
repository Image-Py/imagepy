from imagepy.core.engine import Filter
from imagepy import IPy
import numpy as np 
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
class K_means(Filter):
	"""FillHoles: derived from imagepy.core.engine.Filter """
	title = 'K-Mean'
	note = ['rgb', 'not_channel','auto_msk', 'auto_snap','preview']
	para = {'n_clusters':8,'init':'k-means++','n_init':10,'max_iter':300}
	view = [(int, 'n_clusters', (0,99999), 0,  'n_clusters', ''),
	(int, 'n_init', (0,99999), 0,  'n_init', ''),
	(int, 'max_iter', (0,99999), 0,  'max_iter', ''),
	(list, 'init', ['k-means++', 'random'], str, 'init', 'pix'),]
	def recreate_image(self,codebook, labels, w, h):
		"""Recreate the (compressed) image from the code book & labels"""
		d = codebook.shape[1]
		image = np.zeros((w, h, d))
		label_idx = 0
		for i in range(w):
			for j in range(h):
				image[i][j] = codebook[labels[label_idx]]
				label_idx += 1
		return image
	def run(self, ips, snap, img, para = None):
		print(img.shape)
		image = np.array(snap, dtype=np.float64) 
		w, h,d= tuple(image.shape)
		assert d == 3
		image_array = np.reshape(image, (w * h, d))
		image_array_sample = shuffle(image_array, random_state=0)[:1000]
		kmeans = KMeans(n_clusters=para['n_clusters'],init=para['init'],
			n_init=para['n_init'],max_iter=para['max_iter'], random_state=0).fit(image_array_sample)
		labels = kmeans.predict(image_array)
		img[:,:,:]=self.recreate_image(kmeans.cluster_centers_, labels, w, h)

plgs = [K_means]