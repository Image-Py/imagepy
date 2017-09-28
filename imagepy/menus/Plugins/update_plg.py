from dulwich.repo import Repo
from dulwich.client import get_transport_and_path
from imagepy import IPy
from imagepy.core.engine import Free
from io import StringIO

class Update(Free):
    title = 'Update Software'

    def run(self, para=None):
        IPy.set_info('update now, waiting...')
        repo = Repo('../')
        client, remote_path = get_transport_and_path('https://github.com/Image-Py/imagepy.git')
        a = client.fetch(remote_path, repo)
        IPy.alert('imagepy update done!')

class Refresh(Free):
    title = 'Reload Plugins'

    def run(self, para=None):
        IPy.curapp.reload_plugins()

plgs = [Update, Refresh]