# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 11:37:50 2015

@author: Pomesh

Class to get the stimTimeArray: Time array of stimulation. Look at timestamps 
and nttl to get which channels,times stimulated. Create indexed array with these 
that can be used elsewhere.

Should put this class in NL_Data.py. Then the NL_Data instance can be passed everywhere.
Doesn't even need to be a class. Just keep the methods?

TODO: Get epochs by looking at time differences between stims, see the first
index when diff > 5min or so. 

This file should be run once (make singleton?) at program start so that it gets all events in
csc timestamps. Then the instance can be passed around to the pEpoch files,
where they can extract the individual times.

Should be memmapped with custom dtype later. 
"""

import numpy as np
import scipy.interpolate as spi

import nlxio as nl


class NEV:
    """Util Class For Getting Stimulation Timestamps"""
    
    def __init__(self, cscTs):
        #cscTs are the timestamps from the csc file, it can be any file
        self.ts, self.evId, self.nTTL, self.evStr = nl.loadNev('Events.nev')
        
        self.cscTimeStamps = cscTs
     
        #dont need these initialisations
        self.nTTL_not_zero = []
        #this is run once to make the function which is used later
        self._appFunc = spi.interp1d(self.cscTimeStamps, range(0,len(self.cscTimeStamps)), 
                                    kind='nearest')
        
        self.stimTimeStamps = self._getEventTimes(self.cscTimeStamps)
        
        
    def _getEventTimes(self, tsArray):
        """Returns event times in csc for the tsArray's given"""
        
        for i in range(1, len(self.tsArray)):
            arrayOfClosestIndex = []
            arrayOfClosestIndex.append(int(self._appFunc(self.tsArray[i])))
            
        return self.cscTimeStamps[arrayOfClosestIndex]
        #these should be the event times of the stimulation events
        #clear array at end for new run. better way to do this.
        
    def _getStimIndexForChannel(self, channel):
        """ channel: 1-8 """
        """ returns index, ts"""
        channelStimAtTimes = self.ts[np.where(self.nTTL == channel)] #indexing
        print("Channel " + str(channel) + "stimulated: " + str(len(channelStimAtTimes)) + " times")
        return channelStimAtTimes, self._getEventTimes(channelStimAtTimes)
            
        
    #def _getStimTimes(self):
        
        #self.stimTimes = self.ts[self.nTTL_not_zero] #this is indexing the array
        #return self.stimTimes
        
#    def getStimTimeArray(self):
#        #Problem: Don't know if the clock resets after the stimulation is restarted.
#        #What I purpose is to check the differences in the time stamps, and get the 
#        #index values above 1s. There should be 4 of them. This should also give epoch
#        #timestamps
#        """returns an array of ts, where the stimulation has occured"""
#        self.nTTL_not_zero = np.where(self.nTTL != 0)
#        self.stimTimes = self.ts[self.nTTL_not_zero] #this is indexing the array
#        c = np.in1d(self.cscTimeStamps, self.ts)
#        self.stimTrueIndex = np.where(c == True)
#         
#        #make sure this is a copy
#        return self.cscTimeStamps[self.stimTrueIndex]
        
        
#    def getStimulatedChannel(self, timeStamp):
#        
#        """Returns stimulated channel at particular time?"""
##        return self.nTTL_not_zero
##   
#        pass
        