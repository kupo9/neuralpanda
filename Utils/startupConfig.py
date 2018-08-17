# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 15:00:04 2015

@author: Pomesh

Startup Config file for the program. Will hold various variables that need to
be retained between runs. Right now checks if we added any csc channels, causing
mmap to be recreated. Very barebones for now, will add more later. Careful about
closing file. Also race condition, can use try: later

FILE STATUS: IC
"""

import os

class startupConfig():
    
    def __init__(self, folderName, cscChannels):
        self.configDict = {}
        
        self.fName = folderName
        self.cscChannels = cscChannels

        self._createFile()        
     
#    def _createFile(self):
#        if os.path.isfile('pandaConfig.txt'):
#            print "pandaConfig.txt found..."
#            self._file = open('pandaConfig.txt')
#        else:
#            print "pandaConfig.txt not found..."
#            self._file = open('pandaConfig.txt', 'w')
#            print "pandaConfig.txt created..."
#            self._createConfigParams()
#            self._file.close()
     
    def _createFile(self):
        
        print "reading pandaConfig.txt"
        self._file = open('pandaConfig.txt', 'w+')
        self._createConfigParams()
        self._file.close()
        
    def _createConfigParams(self):
        self.configDict = {
            'folder name: ': self.fName,
            'csc channels: ' : self.cscChannels
            }
    
        for k,v in self.configDict.iteritems():
            self._file.write(str(k) + str(v)+'\n')
    
#    def _checkForDirtyConfig(self):
#        if(self.configDict['csc channels'] != self.cscChannels):
#            pass
#            