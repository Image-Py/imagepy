# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 23:45:59 2017

@author: yxl
"""
import IPy
import os
from core.engines import Macros
from core.managers import ToolsManager,PluginsManager
import sys

first = [0,0]
def extend_plugins(path, lst, err):
    rst = []
    for i in lst:
        if isinstance(i, tuple) or i=='-': 
            rst.append(i)
            
        elif i[-3:]=='.mc':
            f = open(path+'/'+i)
            cmds = f.readlines()
            f.close()
            rst.append(Macros(i[:-3], cmds))
        else:
            try:
                rpath = path.replace('/', '.').replace('\\','.')
                plg = __import__(rpath+'.'+i[:-3],'','',[''])
                if hasattr(plg, 'plgs'):
                    rst.extend([j for j in plg.plgs])
                    for p in plg.plgs:
                        if not isinstance(p, str):PluginsManager.add(p)
                else: 
                    rst.append(plg.Plugin)
                    PluginsManager.add(plg.Plugin)
            except Exception, e:
                err.append((path, i, sys.exc_info()[1]))

    return rst
            
def sort_plugins(catlog, lst):
    rst = []
    for i in catlog:
        if i=='-':rst.append('-')
        for j in lst:
            if j[:-3]==i or j[0].title==i:
                lst.remove(j)
                rst.append(j)
    rst.extend(lst)
    return rst
        
def build_plugins(path, err=None):
    root = err==None
    if err==None:err = []
    subtree = []
    cont = os.listdir(path)
    for i in cont:
        subp = os.path.join(path,i)
        if os.path.isdir(subp):
            sub = build_plugins(subp, err)
            if len(sub)!=0:subtree.append(sub)
        elif i[-6:] in ('plg.py', 'lgs.py'):
            subtree.append(i)
        elif i[-3:] == '.mc':
            subtree.append(i)
    if len(subtree)==0:return []
    
    rpath = path.replace('/', '.').replace('\\','.')
    pg = __import__(rpath,'','',[''])
    pg.title = os.path.basename(path)
    if hasattr(pg, 'catlog'):
        subtree = sort_plugins(pg.catlog, subtree)
    subtree = extend_plugins(path, subtree, err)
    
    if first[0]==0 and root and len(err)>0:
        IPy.write('some plugin may be not loaded, but not affect otheres!')
        for i in err: IPy.write('>>> %-50s%-20s%s'%i)
    if root : first[0]=1
    return (pg, subtree)  
    
def extend_tools(path, lst, err):
    rst = []
    for i in lst:
        if i[-3:]=='.mc':
            f = open(path+'/'+i)
            cmds = f.readlines()
            f.close()
            rst.append((Macros(i[:-3], cmds),  path+'/'+i[:-3]+'.gif'))
        else:
            try:
                rpath = path.replace('/', '.').replace('\\','.')
                plg = __import__(rpath+'.'+i,'','',[''])
                if hasattr(plg, 'plgs'): 
                    for i,j in plg.plgs: rst.append((i, path+'/'+j))
                else: rst.append((plg.Plugin, path+'/'+i.split('_')[0]+'.gif'))
            except Exception, e:
                err.append((path, i, sys.exc_info()[1]))
    for i in rst:ToolsManager.add(i[0])
    return rst
            
def sort_tools(catlog, lst):
    rst = []
    for i in catlog:
        if i=='-':rst.append('-')
        for j in lst:
            if j==i or j[0].title==i or j[:-3]==i:
                lst.remove(j)
                rst.append(j)
    rst.extend(lst)
    return rst
    
def build_tools(path, err=None):
    root = err==None
    if err==None:err=[]
    subtree = []
    cont = os.listdir(path)
    for i in cont:
        subp = os.path.join(path,i)
        if root and os.path.isdir(subp):
            sub = build_tools(subp, err)
            if len(sub)!=0:subtree.append(sub)
        elif not root:
            if i[len(i)-7:] in ('_tol.py', 'tols.py'):
                subtree.append(i[:-3])
            elif i[-3:] == '.mc':
                subtree.append(i)
    if len(subtree)==0:return []
    rpath = path.replace('/', '.').replace('\\','.')
    pg = __import__(rpath,'','',[''])
    pg.title = os.path.basename(path)
    if hasattr(pg, 'catlog'):
        subtree = sort_tools(pg.catlog, subtree)
    if not root:subtree = extend_tools(path, subtree, err)    
    elif first[1]==0 and len(err)>0: 
        IPy.write('tools not loaded:')
        for i in err: IPy.write('>>> %-50s%-20s%s'%i)
    if root : first[1]=1
    return (pg, subtree)
    
if __name__ == "__main__":
    print os.getcwd()
    os.chdir('../../')
    data = build_tools('tools')
