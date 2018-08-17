# -*- coding: utf-8 -*-
"""
NL_Data.py
Created on Tue Oct 20 17:04:40 2015

@author: Pomesh
This File has the dtype of the mmap file. Used to open and read memmap.
Will add electrodeHookup here too, make a dict for structures. 

FILE STATUS: IC (_extractPerChannel(): pass). Default for num of channels 
to load is 128! 
Update: need to look into mmap file being closed. There are some mem leaks in 
the program.

Nov 24: Changing to hdf5 format
"""

import os
import numpy as np
import h5py

import nlxio as nl


class NL_Data:
    """This class loads the csc files from project folder and creates a .dat 
        for faster access later. It also, for the time being, has the 
        readMmap function. Should be moved later to more appropriate location."""
        
    def __init__(self, cscFolderName, blankFiles, numFiles = 8):
        
        self._cscFolderName = cscFolderName
        
        #os.chdir(self._cscFolderName) #Moved to main file
        
        self.numfiles = numFiles
#        self.csc = []
#        self.ts = []
        #self.mmapData = []
        
        self.samples=len(nl.loadNcs('CSC1.ncs')[0])
        
#        self._nldtype = np.dtype([('ts', np.uint64), 
#                                  ('csc', np.int16, (self._numFiles, ))])

        #self._blanks = blankFiles[0]
        
        #need a dirty check here. offload to config file.                         
        if(os.path.isfile("nldata.hdf5") == False):
            print("nldata.hdf5 not found")
            self._createMmap()
            self._loadCscFolder()
            self._openhdf()
        else:
            print ("nldata.hdf5 found")
            self._openhdf()
        
        
    def _loadCscFolder(self):
       
#        for i in range(1, self._numFiles + 1):
#            try:
#                print("Extracting CSC" + str(i))
#                self._csc, self._ts = nl.loadNcs('CSC' + str(i))
#            except IOError as e:
#                print "File not found: CSC" + str(i)
#                print(os.strerror(e.errno))
        
        #only need one ts, iterating from 2+, also change to list comprehension
        
        #self._ts = nl.loadNcs('CSC1')[1]        
        #self._data.append(nl.loadNcs('CSC1.ncs')[1])   
        
        self.timestamps[:] = nl.loadNcs('CSC1.ncs')[1]
        
        for i in range(1, self.numfiles + 1):
            try:
                print("Extracting CSC" + str(i))
                #self._data.append(nl.loadNcs('CSC' + str(i) + '.ncs')[0])
                self.csc[i] = nl.loadNcs('CSC' + str(i) + '.ncs')[0] #add blank check
                #self.mmapFile.flush()                
                print("Done/Flush: CSC" + str(i)) 
            except IOError as e:
                print "File not found: CSC" + str(i)
                print(os.strerror(e.errno))       
            except TypeError as e:
                print "Type Error: " + str(i)
        print "\nAll files extracted..."

        #have to check if its really being deleted        
        self.f.close()
                

    def _createMmap(self):
        
        self.f = h5py.File("nldata.hdf5", 'w')
        self.timestamps =self.f.create_dataset("ts", shape=(self.samples,), dtype=np.uint64)
        self.csc = self.f.create_dataset("csc", shape=(self.numfiles+1, self.samples), 
                                         dtype=np.int16)

    def _openhdf(self):
        self.f = h5py.File("nldata.hdf5", 'r')

#    def _createMmap(self):
#        '''Created to speep up access. Size should be approx 12 gb for 128 channels.'''
#        
#        print("\nCreating memmap nldata.dat in project directory")
#
#        self.mmapFile = np.memmap("nldata.dat", 
#                                  dtype = self._nldtype, 
#                                  mode='w+',
#                                  shape = (self.samples))
#        
#        print("memmap file created, adding data...")        
#        
#    def readmmap(self):
#        
#        return np.memmap("nldata.dat", 
#                                  dtype = self._nldtype, 
#                                  mode='r',
#                                  shape = (self.samples))         
        
#        self.ts = self.readMmapFile['ts']
#        self.csc = self.readMmapFile['csc']
#        
        #del self.readMmapFile
#        print "_readMmap() has been called..."
#        
#    def closeMmapFile(self):
#        del self.mmapData
#        
#    def getmmap(self):
#        return self.mmapData
        
#    def _extractPerChannel(self):
#        pass           

        