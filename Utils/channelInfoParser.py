# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 14:34:34 2015

@author: Pomesh

Simple Python extractor for ChannelInfo.mat. Due to no support for parsing of
matlab tables, the file needs to be converted to a cellarray (table2cell)
Then this is used. Will write a small snippet and put in the utils directory.

For now, much of the things in this file are hardcoded, i.e. the names must
be used as they are defined here. To double check, the strucutre of the table
can be glanced in matlab.

uses loadmat from scipy.io

"""

import numpy as np
from scipy.io import loadmat


class ChannelInfoParser():
    
    def __init__(self, filename="channelinfocell"):
        """filename: Don't append .mat at the end of the file """
        matFile = loadmat(filename)
        #this is the name saved in matlab
        self.cell = np.array(matFile['cell'])
        
        self.leftHem = np.where(self.cell[:,3] == 'Left')
        self.rightHem = np.where(self.cell[:,3] == 'Right')
        
        #extracting the strucutres. Use these later from instance
        """ TODO: Add these later"""
    
#        self.l_rfa = self.getLeftChannel('RFA')
#        self.r_rfa = self.getRightChannel('RFA')
#    
#        self.l_m1 = self.getLeftChannel('M1')
#        self.r_m1 = self.getRightChannel('M1')
#        
#        self.l_dls = self.getLeftChannel('DLS')
#        self.r_dls = self.getRightChannel('DLS')
#        
#        self.l_thal = self.getLeftChannel('Thal')
#        self.r_thal = self.getRightChannel('Thal')
#        
#        self.l_snr = self.getLeftChannel('SNr')
#        self.r_snr = self.getRightChannel('SNr')
#        
#        self.l_dms = self.getLeftChannel('DMS')
#        self.r_dms = self.getRightChannel('DMS')
#        
#        self.l_gp = self.getLeftChannel('GP')
#        self.r_gp = self.getRightChannel('GP')
#        
#        self.l_stn = self.getLeftChannel('STN')
#        self.r_stn = self.getRightChannel('STN') 
    
        
        self.l_rfa = self.getLeftChannel('mPFC')
        self.r_rfa = self.getRightChannel('mPFC')
    
        self.l_m1 = self.getLeftChannel('MGN')
        self.r_m1 = self.getRightChannel('MGN')
        
        self.l_dls = self.getLeftChannel('NAccCore')
        self.r_dls = self.getRightChannel('NAccCore')
        
        self.l_thal = self.getLeftChannel('Thal')
        self.r_thal = self.getRightChannel('Thal')
        
        self.l_snr = self.getLeftChannel('Hippo')
        self.r_snr = self.getRightChannel('Hippo')
        
        self.l_dms = self.getLeftChannel('NAccShell')
        self.r_dms = self.getRightChannel('NAccShell')
        
        self.l_gp = self.getLeftChannel('GP')
        self.r_gp = self.getRightChannel('GP')
        
        self.l_stn = self.getLeftChannel('STN')
        self.r_stn = self.getRightChannel('STN')

        self.blanks = np.where(self.cell[:,7] == 'Blank')
        
    def excludeChannels(self, array, channelsToRemove):
        print "Removing channels: " + str(channelsToRemove)
        removal = np.where(np.in1d(array, np.array(channelsToRemove)))
        return np.delete(array, removal)
    
#cant think of a better way to do this.    
    def getRightChannel(self, name):
        tmp = np.where(self.cell[:,2] == name)[0]
        tmp2 = np.where(tmp > 64)
        return np.add(tmp[tmp2[0]],1)
    
    def getLeftChannel(self, name):
        tmp = np.where(self.cell[:,2] == name)[0]
        tmp2 = np.where(tmp < 65)
        return np.add(tmp[tmp2[0]],1)
        
        

