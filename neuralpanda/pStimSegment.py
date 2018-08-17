# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 10:15:48 2015

@author: Pomesh

pStimSegment: defines a stimulation "trial" or segment from the experiment. This
is needed when the experiment contains multiple stimulation paradigms. 

NB: This class has been put on hold for time being. Most of the work will be done 
in pStructure, until I think of better management of individual stim events in 
the structures vs stimsegments.

Nov15: Off-hold, going to be a single instance class created in main.init() This instance
will be passed into the pStructure object. It'll have an array of indices (in pairs)
of the stimsegments.'
"""
import numpy as np

class pStimSegment():
    
    def __init__(self, nlevents):
        """ pStimSegment.Needs instance of NEV to get the stimulation segements"""
            
        self._nStimEvents = nlevents.nStimSegments
        self.segArray = []
        
        print "Following stim segment indices in csc INDICES"
        for i in range(0, self._nStimEvents):
            self.segArray.append(nlevents.getStimSegmentCSCIndex(i))
            print nlevents.getStimSegmentCSCIndex(i)
        self.npSegArray = np.array(self.segArray).flatten()

        print ("\nStimSegments added to segArray...\n")
        print self.npSegArray
        

