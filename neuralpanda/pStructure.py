# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 16:21:53 2015

@author: Pomesh

pStructure class, holds the array of the cscs in a particular structure as
well as the name of the structure for window title. This is passed onto the 
visViewApp. 

Might be overdoing OOP! This is more like a C struct. Will add methods when 
needed.

"""

class pStructure():
    
    def __init__(self, name, cscValidArray, mainStimChannel):
        self.name = name
        self._cscValidArray = cscValidArray 
        self._stimChannel = mainStimChannel
        self.info = self.name + " CSC channels " + str(self._cscValidArray)
        
        #if self._stimChannel not in self._cscValidArray:
            #print "WARNING: Main StimChannel is not in csc array. Please check."
            #print "Program will still compile."
        self._printInfo()
        
    def _printInfo(self):
        print self.info