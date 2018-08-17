# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 19:51:11 2015

@author: Pomesh

Will be used to display 8 lfp per window. Unsure if it should be in Qt or 
mpl. Will change later if need be. mpl may be too slow for high density data.
Ability to add visual sampling, to make graphing faster. Default sub-sampling is 32.

FILE STATUS: Incomplete, obsolete, using vispy instead. MPL will be used for final
graphs. 
"""

import matplotlib.pyplot as plt
import numpy as np
#from vispy.plot import Fig

class LFPViewer:
    """Class to plot LFPs"""
    
    def __init__(self, nlData, sampling=32):
        ''' nlData contains:ts,csc,len
            sampling for visual purposes, faster, default = 32
        '''
        self._ts = nlData.mmapData['ts']
        self._csc = nlData.mmapData['csc']
        self._len = nlData.samples
        self._s = sampling
        #self.chn = 0
        
        self.plotLFP()
    
    def plotLFP(self):
        """ plotLFP: plots 1 lfp for time being. Uses start:stop:skip
            self._csc[:, chn-1] selects the right column from the csc datastruct 
            to plot"""
            
        print("\nPlotting LFP")
        
        #Add another list here where there will be 8 lfp /structure, 
        #then plot over structure. Will add another argument to plotLFP
        #plotLFP(self, structure)
        #plotWidget=pg.plot(title="LFP")
        self.chn = 1,2,3,4
        
        self.fig, self.ax = plt.subplots(4,sharex=False)
        self.ax[0].set_title('LFP For 4 Channels')
        
        for i in range(0,4):
            
            self.ax[i].get_xaxis().set_visible(False)
            self.ax[i].get_yaxis().set_visible(False)
            self.ax[i].plot(self._ts[::self._s].astype(np.float32), self._csc[:,i][::self._s])
    
#    def addLFPSubplots(self, row, column, number):
#        for i in range(1,row):
#            for c in range(1, column):
#                for n in range(1,number):
#                    self.fig.add_subplots(str(i,c,n).replace(',','')[1:-1])