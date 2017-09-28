from dulwich.repo import Repo
from dulwich.porcelain import pull
from imagepy import IPy
from imagepy.core.engine import Free
from io import StringIO

class Plugin(Free):
    title = 'Update Software'

    def run(self, para=None):
        repo = Repo('../')
        output = StringIO()
        pull(repo, 'https://github.com/Image-Py/imagepy.git')
        repo.close()
        #IPy.write(output.read())