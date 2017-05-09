# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 14:05:12 2016
@author: yxl
"""
import IPy
import webbrowser
from core.engines import Free

## TODO:Fixme!
class About(Free):
    title = 'About'
    def run(self, para=None):
        IPy.alert('ImagePy v0.2')
        
class Topic(Free):
    title = 'Topic'

    def run(self, para=None):
        webbrowser.open('http://www.imagepy.org/document')
        
class Home(Free):
    title = 'Home Page'

    def run(self, para=None):
        webbrowser.open('http://imagepy.org')

plgs = [Topic, About, '-', Home]