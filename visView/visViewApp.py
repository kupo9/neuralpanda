# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 07:52:02 2015

@author: Pomesh

Standalone canvas (to be integrated into qt), to test lfp viewer with multiple lfps
Note that this will auto-display 8 lfps. Need strucutre arg. Will add after I
have a parser for electrodeHookup.m

Nov15: Added structure.

NB: unfreeze to access attributes in init

sampling at 1024 (speed), depends on computer
Text rendering is slow. Info will be added to window title instead for now.
"""

import numpy as np
from vispy import app, scene

import LFPVisual as lfpvis

from vispy.scene.visuals import Text

class visViewApp(scene.SceneCanvas):
    
    def __init__(self, nlData, structure, stimsegments):
        scene.SceneCanvas.__init__(self, title='visView: ' + structure.name + str(structure._cscValidArray), 
                                   size=(800,600), bgcolor="white", keys='interactive')
        self.unfreeze()
        
        self.nldata = nlData #better way to reduce mem print?
        self._structure = structure._cscValidArray
        self._stimSegs = stimsegments
        self.show()
        
        self._timeIndex = np.linspace(0, 1, len(self.nldata.f['csc'][0]))
        
        #test grids
        self.grid = self.central_widget.add_grid()
        self.myvis = scene.visuals.create_visual_node(lfpvis.LFP_Visual)   
        self._setupLfps()
             
        #need better management of these
        del self._timeIndex
        del self.nldata
        del self.lfpgrids
        
        self.freeze()
        app.run()
        
    #this event doesn't fire for some reason        
    def on_close(self, e):
        print "Exitting"
      
    def _setupLfps(self):
        #1-9 matlab comp?
        #adding  lfpvisuals, 8/window, can be more. Need to check performance
        self.lfpgrids = []
        self.textlist = []
        for i in range(0, len(self._structure)):
            self.lfpgrids.append(self.grid.add_view(row = i, col=0, 
                                                    name = 'lfp'+str(i), 
                                                    border_color='gray', 
                                                    bgcolor='white'))
                                                    
            self.lfpgrids[i].add(self.myvis(self.nldata, self._timeIndex, 
                                    self._structure[i], self._stimSegs, sample = 512))
                                    
            self.lfpgrids[i].camera = scene.PanZoomCamera(rect=(0, -1.1, 1, 2.5)) 
                                       
            Text('LFP Channel: '+str(self._structure[i]), parent = self.lfpgrids[i],
                                color='white', pos=(20, 10))
                                       
    
