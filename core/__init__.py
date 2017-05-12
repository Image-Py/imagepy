a = 123
'''
from __future__ import absolute_import
from . import draw
from . import engine
from . import graph
from . import loader
from . import manager
from . import pixel
from . import roi

from . engine.filter import Filter
from . engine.simple import Simple
from . engine.free import Free
from . engine.tool import Tool
from . engine.macros import Macros

from . manager.colormanager import *
from . manager.pluginmanager import *
from . manager.windowmanager import *
from . manager.roimanager import *
from . manager.clipbdmanager import *
from . manager.configmanager import *
from . manager.shotcutmanager import *
'''