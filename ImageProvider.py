from PySide2 import QtCore, QtGui, QtWidgets
import networkx as nx
from graphviz import Graph
from motivo_utils import *
from collections import OrderedDict
import shutil
"""
Image Provider implement a LRU cache
which stores  key = "Motif Signature" , value "filepath"

ResultsVisualzer and ResultsExporter uses ImageProvider to 
retrieve filepath of motif
"""
class ImageProvider:
    def __init__(self, maxLength=100000):
        self.cache = OrderedDict()
        self.maxLength = maxLength
        self.imageDirectory = "./motifSVGCache"

    def __setitem__(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
        else:
            # Based on the motif create svg
            dot= Graph('G', engine="circo",strict=True)
            dot.format = 'svg'
            g=Graphlet(key)
            dot.attr(bgcolor='transparent')
            dot.attr('node', shape='circle')
            dot.attr('node', color='black')
            dot.attr('node', style='filled')
            dot.attr('node', fillcolor='#8EC13A')
            #dot.attr('node', label='')
            for u,v in (g.edge_list()):
                dot.edge(str(v),str(u))
            dot.render(self.imageDirectory+"/"+str(key))
            value=self.imageDirectory+"/"+str(key)+".svg"
        self.cache[key] = value
        if len(self.cache) > self.maxLength:
            self.cache.popitem(last=False)
    def __getitem__(self, key):
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        else:
            self.__setitem__(key,"")
            return self.cache[key]
    def __del__(self):
        shutil.rmtree(self.imageDirectory,ignore_errors=True)
