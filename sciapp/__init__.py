from .app import App
from .manager import Manager

class Source:
    managers = {}

    @classmethod
    def manager(cls, name):
        if not name in cls.managers: 
            cls.managers[name] = Manager()
        return cls.managers[name]