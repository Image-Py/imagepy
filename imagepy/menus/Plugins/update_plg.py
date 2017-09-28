from imagepy import IPy
from imagepy.core.engine import Free

class Update(Free):
	title = 'Update Software'
	def load(self):
		try:
			from dulwich.repo import Repo
			from dulwich.client import get_transport_and_path
			self.repo, self.trans = Repo, get_transport_and_path
		except:
			IPy.alert('dulwich is needed, you can use Plugins > Install > Install Packages:\ndulwich --global-option="--pure" to install')
			return False
		return True

	def run(self, para=None):
		IPy.set_info('update now, waiting...')
		repo = self.repo('../')
		client, remote_path = self.trans('https://github.com/Image-Py/imagepy.git')
		a = client.fetch(remote_path, repo)
		IPy.alert('imagepy update done!')

class Refresh(Free):
	title = 'Reload Plugins'

	def run(self, para=None):
		IPy.curapp.reload_plugins()

plgs = [Update, Refresh]