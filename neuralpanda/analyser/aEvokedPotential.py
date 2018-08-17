# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 14:19:31 2015

@author: Pomesh

EvokedPotential methods for analysis. For now, the matplotlib code is here.
It'll need to be moved later.

Adding write to excel and txt file, use self.currPlot to get the index to the 
current plot. Rename this in the code, A1, C1 are max, min labels
Write to A2, C2
"""
from __future__ import division

import itertools
import numpy as np
from scipy import signal
#from .. import pEvokedPotential as pe
from scipy.signal import butter, filtfilt, lfilter, argrelextrema
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import peakdetect as peakdect
import xlwings as xw

class aEvokedPotential():
    
    def __init__(self, figure, segment, _type, *pEvokedPotential):
        #self.evp = pEvokedPotential
        self.fig = figure
        if _type == "ep":
            self.infFile = open("empty_statsFile_ep" + str(segment+1) + ".txt", 'w')
        if _type == "fp":
            self.infFile = open("empty_statsFile_fp" + str(segment+1) + ".txt", 'w')
            
        for i in pEvokedPotential:        
        
#            figure.axes[pEvokedPotential.index(i)].get_xaxis().set_visible(False)
#            figure.axes[pEvokedPotential.index(i)].get_yaxis().set_visible(False)
            
            if _type == "ep":
                self.evp = i
               
                print("\nNew Axes: " + str(self.evp.name))
                #plt.figure()
                figure.axes[pEvokedPotential.index(i)].set_xticklabels([])
                figure.axes[pEvokedPotential.index(i)].set_yticklabels([])
                self.currPlot = pEvokedPotential.index(i)
                xw.Sheet.add()
                xw.Sheet(self.currPlot+1).activate()
                xw.Sheet(self.currPlot+1).name = str(self.evp.name)
                xw.Range('A1').value = 'Maxima'
                xw.Range('D1').value = 'Minima'
                self._draw()
                i.close()
                
            if _type == "fp":
                self.evp = i
                print("FP")
                figure.axes[pEvokedPotential.index(i)].set_xticklabels([])
                figure.axes[pEvokedPotential.index(i)].set_yticklabels([])
                self.currPlot = pEvokedPotential.index(i)
                xw.Sheet.add()
                xw.Sheet(self.currPlot+1).activate()
                xw.Sheet(self.currPlot+1).name = str(self.evp.name)
                xw.Range('A1').value = 'Maxima'
                xw.Range('D1').value = 'Minima'
                self.drawDiffMeasures()
                i.close()
                
        if _type == "ep":           
            self.infFile.close()
        if _type == "fp":
            self.infFile.close()
        
    def drawDiffMeasures(self):
        print("Drawing DiffMeasures")
        
        #self.fig.axes[0].legend(loc="upper right", fontsize=12)
        
        d = self.evp._getDiff()
        print "dshape" + str(d.shape)
        stdBase = np.std(d[2000:4870])
         
        data =signal.filtfilt(np.ones(3)/3, 1, np.divide(d, stdBase))
        
        maxv, minv = peakdect.peakdet(data[4850:], delta=3)
        print "data shape" + str(data.shape)
        maxv = maxv[1:]
        
        self.infFile.write("\n+++\n")
        self.infFile.write(self.evp.name)
        self.maxList = []
        self.minList = []
        print "maxv" + str(maxv)
        print "minv" + str(minv)
        
        try:
            self.fig.axes[self.currPlot].plot(maxv[:,0]+4870, maxv[:,1], 'o', color = 'red')
            self.fig.axes[self.currPlot].plot(minv[:,0]+4870, minv[:,1], 'x', color = 'green')
         
            self.writeToStatsFile(maxv, minv)
        except (IndexError) as e:
            print "----Empty"
            
        self.maxList = np.asarray(self.maxList)
        print self.maxList
        
        _curr = 2
        try:
            for i in range(0, len(self.maxList)):
                #print "Curr: " + str(_curr)
                _size = self.maxList[i].size
                #print self.maxList[i][:,0]
                self.maxList[i][:,0] = np.multiply(self.maxList[i][:,0], (1/16))
                print self.maxList[i]
                xw.Range('A'+str(_curr)).value = self.maxList[i]
                xw.Range('A'+str(_curr)).color = (255,50,78)
                _curr +=_size
        except (ValueError, IndexError) as e:
            print "Something Went Wrong, Dont ask me what"
            
        _curr = 2   
        try:
            for i in range(0, len(self.minList)):
                #print "Curr: " + str(_curr)
                _size = self.minList[i].size
                #print self.minList[i]
                self.minList[i][:,0] = np.multiply(self.minList[i][:,0], (1/16))
                xw.Range('D'+str(_curr)).value = self.minList[i]
                xw.Range('D'+str(_curr)).color = (102,205,170)
                _curr +=_size
        except (ValueError, IndexError) as e:
            print "Something Went Wrong "
            
        
        
#        try:        
#            self.infFile.write("\nMaxList\n")
#            _j = np.nanmean(self.maxList, axis= 0)
#            _j[:,0] = (_j[:,0] + 4700)*(1/16)
#            self.infFile.write(str(_j))
#            
#            self.infFile.write("\nMinList\n")
#            _g = np.nanmean(self.minList, axis= 0)
#            _g[:,0] = (_g[:,0] + 4700)*(1/16) 
#            self.infFile.write(str(_g))
#            
#        except (ValueError, IndexError) as e:
#            print "Value Error on: " + str(self.evp.name)        
#        
#        #self.fig.axes[0].set_ylim([0, 5])
        print ("Plot Diff\n")
        #self.drawAll()
        self.fig.axes[self.currPlot].set_title(self.evp.name, loc="left", fontsize=12)
        self.fig.axes[self.currPlot].set_ylim([-10, 280])
        #self.fig.axes[self.currPlot].set_ylabel('FP', fontsize=5)
        self.fig.axes[self.currPlot].plot(data, label = self.evp.name, linewidth=1.0)
        
       
        
        del d, data
       
    def _draw(self):
        #writing name to statsfile
        self.infFile.write("\n\n++++++++++++++++++++++++++++++\n")
        self.infFile.write(self.evp.name)
        self.maxList = []
        self.minList = []
        self.drawAll()
        
        print len(self.maxList)
        _curr = 2
        try:
            for i in range(0, len(self.maxList)):
                #print "Curr: " + str(_curr)
                _size = self.maxList[i].size
                #print self.maxList[i][:,0]
                self.maxList[i][:,0] = np.multiply(self.maxList[i][:,0], (1/16))
                print self.maxList[i]
                xw.Range('A'+str(_curr)).value = self.maxList[i]
                xw.Range('A'+str(_curr)).color = (255,50,78)
                _curr +=_size
        except IndexError as e:
            print "Something Went Wrong "
        _curr = 2   
        try:
            for i in range(0, len(self.minList)):
                #print "Curr: " + str(_curr)
                _size = self.minList[i].size
                #print self.minList[i]
                self.minList[i][:,0] = np.multiply(self.minList[i][:,0], (1/16))
                xw.Range('D'+str(_curr)).value = self.minList[i]
                xw.Range('D'+str(_curr)).color = (102,205,170)
                _curr +=_size
        except IndexError as e:
            print "Something Went Wrong "
            
        
        self.maxList = np.asarray(self.maxList)
        self.minList = np.asarray(self.minList)
        try:        
            self.infFile.write("\nMaxList\n")
            _j = np.nanmean(self.maxList, axis= 0)
            _j[:,0] = (_j[:,0] + 5000)*(1/16)
            self.infFile.write(str(_j))
            
            self.infFile.write("\nMinList\n")
            _g = np.nanmean(self.minList, axis= 0)
            _g[:,0] = (_g[:,0] + 5000)*(1/16) 
            self.infFile.write(str(_g))
            
        except (ValueError, IndexError) as e:
            print "Value Error on: " + str(self.evp.name)
#          
#        plt.title("EP: " + self.evp.info + " Segment: " + str(self.evp._seg + 1) + "MCS_" + str(self.evp._mainStimChannel))
#        plt.legend(loc= "upper right")
#        plt.ylim([-5000, 5000])
        _val = plt.xticks()
        plt.xscale
        #plt.savefig("images/" +self.evp.info + "MCS_" + str(self.evp._mainStimChannel) + "_segment_" + str(self.evp._seg + 1) + ".png")
        
    def _plotEvokedPotential(self, a):
        #ask about these
        data = np.mean(self.evp.getCSC_e(a), axis = 0)
        d =signal.filtfilt(np.ones(50)/50, 1, data)
        #print "dshape" + str(d.shape)
      
        #_test = signal.filtfilt(np.ones(50)/50, 1, data[5000:])
        maxv, minv = peakdect.peakdet(d[2650:], delta=250)
        
        maxv = maxv[1:]
        #minv = minv[1:]
        try:
            #self.fig.axes[self.currPlot].plot(maxv[:,0]+2700, maxv[:,1], 'o', color = 'red')
            self.fig.axes[self.currPlot].plot(minv[:,0]+2700, minv[:,1], 'o', color = 'green')
         
            self.writeToStatsFile(maxv, minv)
        except (IndexError) as e:
            print "----Empty"
        
        
        
#        for i in range(0, len(_alt)):
#            plt.plot(_alt[i] + 5000, _test[_alt][i], 'o', color = 'red')
#       
        print("Plotting EPs")
        twix = self.fig.axes[self.currPlot]
        twix.set_ylim([-3000, 5000])
        twix.set_yticklabels([])
        twix.set_title(self.evp.name, loc="left", fontsize=12)
        twix.plot(d, label = "Channel : " + str(a), linewidth=0.4)
        
#        for i in range(0, len(maxi[0])):            
#              self.fig.axes[self.currPlot].plot(maxi[0][i]+5000, d[5000:7000][maxi][i], 'o', color='gray')
#            
#        for i in range(0, len(mini[0])):            
#              self.fig.axes[self.currPlot].plot(mini[0][i]+5000, d[5000:7000][mini][i], 'x', color = 'red')
        del d, data 
        
    def drawAll(self):
        self.f = list(itertools.combinations(self.evp._cscArray,2))
        g = self.f[ :len(self.evp._cscArray)-1]
        #self.evp.getSubSignals(g)
        for i in self.evp._cscArray:
            self._plotEvokedPotential(i)
            
    def writeToStatsFile(self, maxv, minv):
        #maxAvg = np.average(maxv, axis=0)
        #minAvg = np.average(minv, axis=0)
        
        self.infFile.write("\n")
        self.infFile.write("\nmax values")
        self.infFile.write(str(maxv))
        self.infFile.write("\nmin values")
        self.infFile.write(str(minv))
        #self.infFile.write("\nMax Avg: " + str(maxAvg))
        #self.infFile.write("\nMin Avg: " + str(minAvg))
        self.infFile.write("\n")
        self.maxList.append(maxv)
        self.minList.append(minv)
        
    def butter_bandpass(self, lowcut, highcut, fs, order=2):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='stop')
        return b, a
            
#    def _drawAll(self):
#        #what to index here?
#        [self._calcAndDraw(x) for x in self.evp.getAll()]

""" Old file, for checking purposes"""

## -*- coding: utf-8 -*-
#"""
#Created on Tue Nov 17 14:19:31 2015
#
#@author: Pomesh
#
#EvokedPotential methods for analysis. For now, the matplotlib code is here.
#It'll need to be moved later.
#
#TODO: Refactor to separate class for handling the drawing. 
#This class should only be for analysis. Should return an array of µv values
#that are plotted with pandaplot.
#
#"""
#from __future__ import division
#
#import itertools
#import numpy as np
##from .. import pEvokedPotential as pe
#
#import matplotlib.pyplot as plt
#from matplotlib.ticker import FormatStrFormatter
#from scipy import signal
#
#class aEvokedPotential():
#    
#    def __init__(self, *pEvokedPotential):
#        #self.evp = pEvokedPotential
#        fig = plt.figure()
#        
#        for i in pEvokedPotential:        
#            self.evp = i
#            self._draw()
#            plt.close()
#        
#    def createSubplots(self, i ):
#        pass 
#    
#    def _draw(self):
#        self._drawAll()
##        plt.title("EP: " + self.evp.info + " Segment: " + str(self.evp._seg + 1) +
##                "MCS_" + str(self.evp._mainStimChannel))
#        plt.legend(loc= "lower right")
#        ax = plt.axes()
#        tks=ax.get_xticks()
#        ax.set_xticklabels(np.round(np.multiply(tks,(1/1017))-0.3, 1))
#        #ax.xaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
#        plt.ylim([-1000, 1000])
#        plt.savefig("images/" +self.evp.info + "MCS_" + str(self.evp._mainStimChannel) + 
#                    "_segment_" + str(self.evp._seg + 1) + ".png", dpi = 300)
#       #print np.multiply(tks, (1/1017))
#        del tks, ax
#    
#    def _drawAll(self):
#        f = list(itertools.combinations(self.evp._cscArray,2))
#        g = f[ :len(self.evp._cscArray)-1]
#        #self.evp.getSubSignals(g)
#        for i in self.evp._cscArray:
#            self._calcAndDraw(i)
#            
#    def _calcAndDraw(self, a):
#        #ask about these
#        self.calulatedEp = self.evp.getEvokedPotential(a, 3)
##        print "length ep: " + str(n+1) + str(len(self.calulatedEp)) +"\n"
#        plt.plot(self.calulatedEp, label = "Channel : " + str(a), linewidth=0.3)
#        return self.calulatedEp