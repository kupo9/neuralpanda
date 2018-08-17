# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 07:59:34 2015

@author: Pomesh

pEvokedPotential class. Takes in structure. And the nlEvents class. This is
more of a struct which is passed along to the aEvokedPotential class which does 
the calculations. 

Returns an array, _e, with the csc volts values between the time indicies specified
around stimchannel index. 

TODO: Add ability to have custom pre/post, need to convert to a time INDEX though!
use 1/123
"""
from __future__ import division 
import itertools
import numpy as np
from scipy.signal import butter, filtfilt, lfilter, firwin

class pEvokedPotential():
    
    def __init__(self, nlData, nlevents, structure, segment):
        self._cscArray = structure._cscValidArray
        self._mainStimChannel = structure._stimChannel
        self._nlE = nlevents
        self._seg = segment
        self.nldata = nlData
        self.info = structure.info 
        self.name = structure.name
        self._stimAt = self._nlE.getStimChannelCSCIndex(self._mainStimChannel, self._seg)
        self.samples = len(self.nldata.f['csc'][0])
        
        #-2440, 5691,-488,-81         
        #-61, -10
        self._epcscpairs = [self._epParams(i, -2441, 5697) for i in self._stimAt]  
        self._epnormwindow = [self._epParams(i, -500, -80) for i in self._stimAt]
        
        #so this works for now, dont know how it'll behave with other data
        
        
        self._a = len(nlData.f['csc'][0][self._epcscpairs[1][0] : self._epcscpairs[1][1]])
        
        self._e = np.empty((len(self._epcscpairs), self._a), dtype=np.int16, order='F')
        self._f = np.empty((len(self._epnormwindow), 1), dtype=np.int16, order='F')
    
        self.sig = np.empty(len(nlData.f['csc'][0]))
        #self.fil=self.high_pass(600, 16278)
        print(len(self._epcscpairs))
        print (len(self._epnormwindow))
    
    def close(self):
        del self._a, self._e, self._f, self.sig, self._epcscpairs, self._epnormwindow
        
    def getCSC_e(self, n):
        tmp = self.nldata.f['csc'][n]#, self.nldata.f['csc'][f])
        #tmp = filtfilt(self.b, self.b, self.sig)
        #tmp = np.subtract(self.sig, filtfilt(self.fil, 1.0, self.sig))
        for i in range(0,len(self._epcscpairs)):  
            self._f[i] = np.mean(tmp[self._epnormwindow[i][0]:self._epnormwindow[i][1]])
            self._e[i] = np.subtract(tmp[self._epcscpairs[i][0]:self._epcscpairs[i][1]], self._f[i])
        #print "channel " + str(n+1) + str(self._f.shape)
        #print "done signal" + str(n) + str(f)
        del tmp
        return self._e
        
    def getCSC_ee(self, n, m):
        tmp = np.subtract(self.nldata.f['csc'][n], self.nldata.f['csc'][m])
        #tmp = filtfilt(self.b, self.b, self.sig)
        print("\nAdding " + str(n) + ", " + str(m))
        for i in range(0,len(self._epcscpairs)):  
            self._f[i] = np.mean(tmp[self._epnormwindow[i][0]:self._epnormwindow[i][1]])
            self._e[i] = np.subtract(tmp[self._epcscpairs[i][0]:self._epcscpairs[i][1]], self._f[i])
        #print "channel " + str(n+1) + str(self._f.shape)
        #print "done signal" + str(n) + str(f)
        del tmp
        print self._e.shape
        return self._e

    def _getDiff(self):
        f = list(itertools.combinations(self._cscArray,2))
        g = np.empty((len(f), 8138), dtype=np.int16)
        print("Made Empty Array")
        for i in f:
            g[f.index(i)] = np.mean(self.getCSC_ee(*i), axis= 0)
            print("Added " + str(i))
            
        print("Returning std")
        print g.shape
        return np.std(g, axis=0)
        
        
    def _getDiffSegments(self, l, m):
        tmp = np.subtract(self.nldata.f['csc'][l], self.nldata.f['csc'][m])
        print "Subtracted Signals"
        for i in range(0, len(self._epcscpairs)):
            self._f[i] = np.mean(tmp[self._epnormwindow[i][0]:self._epnormwindow[i][1]])
            self._e[i] = np.subtract(tmp[self._epcscpairs[i][0]:self._epcscpairs[i][1]], self._f[i])
        return self._e                        
    
#    def getDiffMeasures(self):
#        print("GetDiffMeasures")
#        f = list(itertools.combinations(self._cscArray,2))
#        print(f)
#        tmp = np.empty((len(f), self.samples), dtype=np.int16, order='F')
#        print("Made Empty")
#        
#        print(tmp)
#        for i in f:
#            tmp[f.index(i)] = np.subtract(self.nldata.f['csc'][i[0]], self.nldata.f['csc'][i[1]])
#            print("Added" + str(i))
#        
#        print(tmp)
#        print(tmp.nbytes)
#        print(tmp.shape)
#        return tmp
#            
#    def getStandardSignal(self):
#        print("GetStandardSignal")
#        tmp = self.getDiffMeasures()
#        print("tempArr.shape")
#        tempArr = np.empty((tmp.shape[0], len(self._epcscpairs), self._a), dtype=np.int16)
#        print(tempArr.shape)        
#        for j in range(0, tmp.shape[0]):
#            for i in range(0,len(self._epcscpairs)):  
#                self._f[i] = np.std(tmp[j][self._epnormwindow[i][0]:self._epnormwindow[i][1]])
#                tempArr[j,i,:] = np.divide(tmp[j][self._epcscpairs[i][0]:self._epcscpairs[i][1]], self._f[i])   
#            #del tmp
#        print("tempArr.nbytes and shape")
#        print tempArr.nbytes
#        print tempArr.shape
#        return tempArr
#        
        
    def _epParams(self, i, pre, post):
        return i+pre, i+post   
                   
    def getonewindow(self, channel, i):
        tmp = self.nldata.f['csc'][channel]
        return tmp[self._epcscpairs[i][0]:self._epcscpairs[i][1]]
        
    def high_pass(self, high, fs, order=28):
            nyq = 0.5 * fs
            numtaps=order+1
            h = high/nyq
            return firwin(numtaps, h)
    def butter_bandpass(self, lowcut, highcut, fs, order=2):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='stop')
        return b, a