# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 14:05:12 2016

@author: yxl
"""
import IPy
from core.engines import Free
from ui.logwindow import TextLog

class About(Free):
    title = 'About'
    #process
    def run(self, para=None):
        IPy.alert('ImagePy v0.1')
        
info = '''Hi:
I am yxdragon, I write this item in 2 month,
I build the frame work, now it's esay to glue
some other libs, ez:opencv, matplotlib, mayavi...

I wrote it in Ubuntu, As wxpython is cross platform,
but I am not sure it works OK in Windows.

It's a valuable work i beleive, but now I got some problem.

1. I do not have so much time to go on, I must earn a living.
2. I must write some doc, but I am a chinese, my english is poor.
3. I had got the 'imagepy.org' and I want to build a community just like ImageJ, but I am a System engineer, not good at web development.

then if you are intresting in this item, and if you are a Image process programer, or a web programer, or you are good at writing document please contact with me!
you can also desine a logo for imagepy, or donate, even just let me known this item is useful for you! I will be more inspiring!

Mail:imagepy@sina.com
yxdragon

'''

class Topic(Free):
    title = 'Topic'

    #process
    def run(self, para=None):
        IPy.write(info, "Let's build it together!")
        
class Home(Free):
    title = 'Home Page'

    #process
    def run(self, para=None):
        IPy.alert('http:\\imagepy.org, but i have no energy to develop it, if you are a web programer and intresting in this item, contact with me!, mail:imagepy@sina.com yxdragon')
        
plgs = [Topic, About, Home]