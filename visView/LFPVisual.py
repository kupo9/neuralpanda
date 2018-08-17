# -*- coding: utf-8 -*-
"""
Created on Sat Nov 07 15:12:44 2015

@author: Pomesh

An LFP Custom Visual object. To be used in grids. Custom camera should be added to limit
scaling in y axis. Have to be VERY careful about the index.

Added del to some variables. Memory usage lowered. The timeIndex values are 
handled by the visViewApp for now. Since they're common for all lfps, they 
only need to be calculated once, and deleted at the end of the program.

FILE STATUS: IC, need to add some lod/dynamic subsampling if it can't handle the 
bigger files (100mb+). Otherwise, it's usable for quick  visualisation.

Nov15: Adding indexing support for the various stim segments. They should be 
different colours.

"""

from __future__ import division

vertex=""" 
varying float index;

void main()
{
    //check this again

    index = $position.x;
    gl_Position = $transform(vec4($position, 0, 1));
}

"""

frag = """ 
varying float index;

void main()
{
//add color coding to epochs. easy to do with index. should be random colors vec4()
//add glow when mouse over epochs, get selected epoch and open in separate canvas
//with full res/sample

    //testing index colors
    if (index > $ind3 && index < $ind4)
    {
        gl_FragColor= vec4(1.0, 0.3, 0.4, 1.0);
    }
    else if (index > $ind1 && index < $ind2)
    {
        gl_FragColor= vec4(0.4, 0.3, 0.4, 1.0);
    }
    else if (index > $ind5 && index < $ind6)
    {
        gl_FragColor= vec4(0.8, 0.5, 0.4, 1.0);
    }
    else if (index > $ind7 && index < $ind8)
    {
        gl_FragColor= vec4(0.4, 0.3, 1.0, 1.0);
    }
    else
    {
        gl_FragColor = $color;
    }
}
"""

import numpy as np
from scipy.signal import butter, filtfilt

from vispy import visuals, gloo

class LFP_Visual(visuals.Visual):
    """ A custom Visual object for displaying LFPs"""
    
    def __init__(self, nldata, timeIndex, cscChannel, stimsegment, sample=64):
        visuals.Visual.__init__(self, vertex, frag)
        
        self._c = cscChannel
        self._s = sample
        self.tInd = timeIndex[::self._s]
        
        #self._csc = nldata.mmapData['csc']
        self.b, self.a = self.butter_bandpass(40, 60, 1024)
        self.sig = filtfilt(self.b, self.a, nldata.f['csc'][self._c][::self._s])
        self.normData =self.sig/np.max(self.sig)
        
        self.vbo = gloo.VertexBuffer( data=np.c_[self.tInd, self.normData].astype(np.float32))
        self.shared_program.vert['position'] = self.vbo
                
        #test new indexing :)
        
        self.shared_program.frag['ind1'] = timeIndex[stimsegment.npSegArray[0]]
        self.shared_program.frag['ind2'] = timeIndex[stimsegment.npSegArray[1]]
        
        self.shared_program.frag['ind3'] = timeIndex[stimsegment.npSegArray[2]]
        self.shared_program.frag['ind4'] = timeIndex[stimsegment.npSegArray[3]]
        
        self.shared_program.frag['ind5'] = timeIndex[stimsegment.npSegArray[4]]
        self.shared_program.frag['ind6'] = timeIndex[stimsegment.npSegArray[5]]
        
        self.shared_program.frag['ind7'] = timeIndex[stimsegment.npSegArray[6]]
        self.shared_program.frag['ind8'] = timeIndex[stimsegment.npSegArray[7]]
        
#        self.shared_program.frag['segarray[0]'] = timeIndex[stimsegment.npSegArray[3]]
#        self.shared_program.frag['segarray[1]'] = timeIndex[stimsegment.npSegArray[2]]
#        self.shared_program.frag['segarray[2]'] = timeIndex[stimsegment.npSegArray[4]]
        
#        for i in range(0, 2*stimsegment._nStimEvents):
#            self.shared_program.frag['segarray[{}]'.format(str(i))] = timeIndex[stimsegment.npSegArray[i]]

        self.shared_program.frag['color'] = (1, 0, 0, 1)        
        self._draw_mode = 'line_strip'
        
        #better management system for these. Once the buffers have been uploaded to gpu,
        #they're no longer needed.
        del self.normData
        #del self._csc
        
    #look into transforms later    
    def _prepare_transforms(self, view):
        view.view_program.vert['transform'] = view.get_transform()
        
    def butter_bandpass(self, lowcut, highcut, fs, order=6):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='stop')
        return b, a


