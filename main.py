# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:03:33 2015

@author: Pomesh
Main entry point of app. Add GUI here (.cpp). Qt GUI will be hooked later.
FILE STATUS: Incomplete, There is some memory leak somewhere in the program.
Might be in the vispyviewer codes.

Nov10: Mem leak appears to be fixed, 50% reduction, still at 45% though. More variables
to be deleted. See LFPVisual.py

Nov15: More mem leaks :(

Nov19: memory usage down, some processes are still not shutting down though.
"""
import os,sys
import numpy as np

from PyQt4 import QtGui
import gui.mainGui as gui

import matplotlib.pyplot as plt

import Utils.startupConfig as config
import Utils.NL_Data as nld
import Utils.NL_Events as nle
from Utils import channelInfoParser as cip

from neuralpanda import pStructure, pStimSegment, pEvokedPotential
from neuralpanda.analyser import aEvokedPotential

#import LFPViewer as lfpv
#import VispyLFPViewer as vsp
import visView.visViewApp as vspa
import xlwings 


class Main:
    
    def __init__(self, fname, foldername):
        
        #fill constructor /GUI Code 
        print "\nStarting neuralpanda v0.1\n"
        
        self.fname = fname
        self.folderName = foldername
        
        #This will be done through GUI
        os.chdir(self.folderName) #Should really make a new dir in project folder
        
        #configFile = config.startupConfig(self.folderName, 10)
        
        if not os.path.exists("images"):
            os.makedirs("images")
            print "Image Directory Created..."
        
        #setup channel info
        self.chninfo = cip.ChannelInfoParser()
#        
#        #left channels
#        self.chninfo.l_rfa = self.chninfo.excludeChannels(self.chninfo.l_rfa, [6,7])
#        self.chninfo.l_m1 = self.chninfo.excludeChannels(self.chninfo.l_m1, [11,12])
#        self.chninfo.l_dls = self.chninfo.excludeChannels(self.chninfo.l_dls, [16,22])
#        self.chninfo.l_gp = self.chninfo.excludeChannels(self.chninfo.l_gp, [34,35])
#        self.chninfo.l_snr = self.chninfo.excludeChannels(self.chninfo.l_snr, [56,57])
#        self.chninfo.l_dms = self.chninfo.excludeChannels(self.chninfo.l_dms, [27,28])
#        self.chninfo.l_stn = self.chninfo.excludeChannels(self.chninfo.l_stn, [47])
#        self.chninfo.l_thal = self.chninfo.excludeChannels(self.chninfo.l_thal, [44])
#        
#        #right channels
#        self.chninfo.r_rfa = self.chninfo.excludeChannels(self.chninfo.r_rfa, [97,98,100])
#        self.chninfo.r_m1 = self.chninfo.excludeChannels(self.chninfo.r_m1, [105,106,108,110,111])
#        self.chninfo.r_dls = self.chninfo.excludeChannels(self.chninfo.r_dls, [112])
#        self.chninfo.r_gp = self.chninfo.excludeChannels(self.chninfo.r_gp, [66,68,69,70])
#        self.chninfo.r_snr = self.chninfo.excludeChannels(self.chninfo.r_snr, [87])
#        self.chninfo.r_dms = self.chninfo.excludeChannels(self.chninfo.r_dms, [121,122])
#        self.chninfo.r_stn = self.chninfo.excludeChannels(self.chninfo.r_stn, [])
#        self.chninfo.r_thal = self.chninfo.excludeChannels(self.chninfo.r_thal, [72,75,76,77])
        
        
        self.chninfo.l_rfa = self.chninfo.excludeChannels(self.chninfo.l_rfa, [])
        self.chninfo.l_m1 = self.chninfo.excludeChannels(self.chninfo.l_m1, [])
        self.chninfo.l_dls = self.chninfo.excludeChannels(self.chninfo.l_dls, [])
        self.chninfo.l_gp = self.chninfo.excludeChannels(self.chninfo.l_gp, [])
        self.chninfo.l_snr = self.chninfo.excludeChannels(self.chninfo.l_snr, [])
        self.chninfo.l_dms = self.chninfo.excludeChannels(self.chninfo.l_dms, [])
        self.chninfo.l_stn = self.chninfo.excludeChannels(self.chninfo.l_stn, [])
        self.chninfo.l_thal = self.chninfo.excludeChannels(self.chninfo.l_thal, [])
        
        #right channels
        self.chninfo.r_rfa = self.chninfo.excludeChannels(self.chninfo.r_rfa, [])
        self.chninfo.r_m1 = self.chninfo.excludeChannels(self.chninfo.r_m1, [])
        self.chninfo.r_dls = self.chninfo.excludeChannels(self.chninfo.r_dls, [])
        self.chninfo.r_gp = self.chninfo.excludeChannels(self.chninfo.r_gp, [])
        self.chninfo.r_snr = self.chninfo.excludeChannels(self.chninfo.r_snr, [])
        self.chninfo.r_dms = self.chninfo.excludeChannels(self.chninfo.r_dms, [])
        self.chninfo.r_stn = self.chninfo.excludeChannels(self.chninfo.r_stn, [])
        self.chninfo.r_thal = self.chninfo.excludeChannels(self.chninfo.r_thal, [])
        
        self.nlData = nld.NL_Data(self.folderName, 0,128) #memory hog, OPTIMISE
        self.nlEvents = nle.NL_Event(self.nlData)        
        self.pSeg = pStimSegment.pStimSegment(self.nlEvents)

        
    def _createStructures(self):
        #left structures
        self.s_l_rfa = pStructure.pStructure("Left mPFC", self.chninfo.l_rfa, 1)
        self.s_l_m1 = pStructure.pStructure("Left MGN", self.chninfo.l_m1, 1)
        self.s_l_dls =  pStructure.pStructure("Left NAccCore", self.chninfo.l_dls, 1)
        self.s_l_dms =  pStructure.pStructure("Left NAccShell", self.chninfo.l_dms, 1)
        self.s_l_gp =  pStructure.pStructure("Left GP", self.chninfo.l_gp, 1)
        self.s_l_snr =  pStructure.pStructure("Left Hippocampus", self.chninfo.l_snr, 1)
        self.s_l_stn =  pStructure.pStructure("Left STN", self.chninfo.l_stn, 1)
        self.s_l_thal =  pStructure.pStructure("Left Thalamus", self.chninfo.l_thal, 1)

        #right structures
        self.s_r_rfa = pStructure.pStructure("Right mPFC", self.chninfo.r_rfa, 1)
        self.s_r_m1 = pStructure.pStructure("Right MGN", self.chninfo.r_m1, 1)
        self.s_r_dls =  pStructure.pStructure("Right NAccCore", self.chninfo.r_dls, 1)
        self.s_r_dms =  pStructure.pStructure("Right NAccShell", self.chninfo.r_dms, 1)
        self.s_r_gp =  pStructure.pStructure("Right GP", self.chninfo.r_gp, 1)
        self.s_r_snr =  pStructure.pStructure("Right Hippocampus", self.chninfo.r_snr, 1)
        self.s_r_stn =  pStructure.pStructure("Right STN", self.chninfo.r_stn, 1)
        self.s_r_thal =  pStructure.pStructure("Right Thalamus", self.chninfo.r_thal, 1)

        
    def _createEP(self):
        self.pEp1 = pEvokedPotential.pEvokedPotential(self.nlData, self.nlEvents, self.s_l_dls, 0)
        self.pEp2 = pEvokedPotential.pEvokedPotential(self.nlData, self.nlEvents, self.s_l_dls, 1)
        self.pEp3 = pEvokedPotential.pEvokedPotential(self.nlData, self.nlEvents, self.s_l_dls, 2)
        self.pEp4 = pEvokedPotential.pEvokedPotential(self.nlData, self.nlEvents, self.s_l_dls, 3)
      
        self.pEP5 = pEvokedPotential.pEvokedPotential(self.nlData, self.nlEvents, self.s_r_m1, 0)
        self.pEP6 = pEvokedPotential.pEvokedPotential(self.nlData, self.nlEvents, self.s_r_m1, 1)
        self.pEP7 = pEvokedPotential.pEvokedPotential(self.nlData, self.nlEvents, self.s_r_m1, 2)
        self.pEP8 = pEvokedPotential.pEvokedPotential(self.nlData, self.nlEvents, self.s_r_m1, 3)
       
    def _calculate(self):
        self.aEp = aEvokedPotential.aEvokedPotential(self.pEp1, self.pEp2, self.pEp3, self.pEp4)
        self.bEp = aEvokedPotential.aEvokedPotential(self.pEP5, self.pEP6, self.pEP7, self.pEP8)
    
    #THIS WORKS!
    def _masterplotEP(self, segment):
        #get all structures
        os.chdir(self.folderName)
        wb = xlwings.Workbook()
        
        
        fig = plt.figure(figsize=(17, 24))#, dpi = 300)
        #fig=""
        l_structureList = [] 
       
        for i in vars(self).keys():
            if 's_' in i:
                l_structureList.append(i)
        
        l_structureList.sort()                
        print "StructureList"
        print len(l_structureList)
                
        for i in range(0, len(l_structureList)):
            if i < len(l_structureList)/2:                
                plt.subplot2grid((8,2), (i,0))
            else:
                plt.subplot2grid((8,2), (i-8, 1))
                   
        pEvokedPotentialList = []
        for i in l_structureList:
            pEvokedPotentialList.append(pEvokedPotential.pEvokedPotential(self.nlData, self.nlEvents, eval("self." + i), segment))
        
        
        master_aep = aEvokedPotential.aEvokedPotential(fig, segment, "ep", *tuple(pEvokedPotentialList))
        plt.tight_layout()
        plt.savefig("niceraw_ep_segment_" +str(segment+1) + ".png")
        #wb.xl_workbook.SaveAs(os.path.join(self.folderName,"/wb_raw_ep_segment_" + str(segment+1)))
        
        wb.save(r'' +self.fname + "wb_raw_ep_segment_" + str(segment + 1) )
        xlwings.Application(wb).quit()
        #plt.close()
        
    def _masterplotFP(self, segment):
        os.chdir(self.folderName)
        wb = xlwings.Workbook()
        fig = plt.figure(figsize=(17,24))
        plt.title("Field Potentials Segment" + str(segment+1), fontsize=9)
        
        l_structureList = [] 
        
        for i in vars(self).keys():
            if 's_' in i:
                l_structureList.append(i)
                
        for i in range(0, len(l_structureList)):
            if i < len(l_structureList)/2:                
                plt.subplot2grid((8,2), (i,0))
            else:
                plt.subplot2grid((8,2), (i-8, 1))
                
        l_structureList.sort()                
        print "StructureList"
        print len(l_structureList)
        
        pEvokedPotentialList = []
        for i in l_structureList:
            pEvokedPotentialList.append(pEvokedPotential.pEvokedPotential(self.nlData, self.nlEvents, eval("self." + i), segment))
        
        master_afp = aEvokedPotential.aEvokedPotential(fig, segment, "fp", *tuple(pEvokedPotentialList))
        plt.tight_layout()
        #plt.show()        
        plt.savefig("nlabFP_segment_" +str(segment+1) + ".png")
        plt.close()
        
        wb.save(r'' + self.fname + "nwb_fp_segment_" + str(segment + 1) )
        xlwings.Application(wb).quit()
        
    def runMain(self):        
        #lfpviewer = lfpv.LFPViewer(nlData, 32)
        #lfpviewer.plotLFP() this method is now in constructor
        #closing the mmapfile. 
        #self.vspView = vsp.LVispyviewer(self.nlData, 2)
#    
#        app = QtGui.QApplication(sys.argv)
#        ex = gui.Example(self.nlData, self.nlEvents, self.pSeg)
#        ex.show()        
#        
        self._createStructures()     
        #for i in range(1, self.nlEvents.nStimSegments-1):
        self._masterplotEP(4)

#        self._createEP()
#        self._calculate()

#        sys.exit(app.exec_())
        
        #create the canvas, one per structure
        #self._vspView = vspa.visViewApp(self.nlData, self.s_l_rfa, self.pSeg)
        #self._rm1lfp = vspa.visViewApp(self.nlData, self.s_r_m1, self.pSeg)
        #self._view2 = vspa.visViewApp(self.nlData, self.s_l_m1, self.pSeg)
        #self.nlData.closeMmapFile()
        print "mmap data file closed..."
        print "check mem usage..."
        #self.nlData.f.close()
        #del self._vspView
       
      
if __name__ == "__main__":
    
    #masterList = #[['E:\\Microstim\\2015-12-22_10-22-56_ED_FinalExp1\\', 'E:/Microstim/2015-12-22_10-22-56_ED_FinalExp1']]
#                    ['E:\\Microstim\\2015-12-23_13-28-43_ED_FinalExp3\\', 'E:/Microstim/2015-12-23_13-28-43_ED_FinalExp3'],
    #masterList = [['E:\\Microstim\\AllMicrostim_Test_2016-01-21_09-29-02_ED\\', 'E:/Microstim/AllMicrostim_Test_2016-01-21_09-29-02_ED']]
    #masterList = [['E:\\Microstim\\2015-12-23_14-51-33_ED_FinalExp5\\', 'E:/Microstim/2015-12-23_14-51-33_ED_FinalExp5']]
#                    ['E:\\Microstim\\2015-12-23_15-19-14_ED_FinalExp6\\', 'E:/Microstim/2015-12-23_15-19-14_ED_FinalExp6'],
#                    ['E:\\Microstim\\2015-12-23_15-49-44_ED_FinalExp7\\', 'E:/Microstim/2015-12-23_15-49-44_ED_FinalExp7']] 
    
    masterList= [
        ['E:\\Microstim\\ES_Microstimulation_2016-07-13_10-28-11', 'E:/Microstim/ES_Microstimulation_2016-07-13_10-28-11']  
        
    ]
#    
    for i in masterList:
        print "\nWorking: " + str(i[0]) + " and " + str(i[1])
        m = Main(i[0], i[1])
        m.runMain()
    