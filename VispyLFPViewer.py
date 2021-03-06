# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 16:56:26 2015

@author: Pomesh

Uses OpenGL to view the LFPs, much better performance than LFPViewer based on 
mpl. Add LOD to the data sets so all can be viewed at once. [7/11/15] Trying autoScaleTest, 
lots of lag. Need custom event maybe.

FILE STATUS: IC, some mem leak, might be buffers not being unbound? Fixed now, still
some extra usage though.

EXTRA: This file won't be used in the final app
"""
from __future__ import division


import math
import numpy as np

from vispy import app, gloo

#shaders, will be put in separate txt/glsl file. Different shaders to highlight...
vertex=""" 
uniform vec2 scale;
uniform vec2 pan;
attribute vec2 position;
attribute float timeIndex;
uniform float maxValue;

void main()
{
    vec2 p = scale * (position + pan);
    //float t = timeIndex + pan;
    gl_Position = vec4(p, 0.0, 1.0);
}

"""

frag = """ 

void main()
{
    gl_FragColor= vec4(0.5, 0.2, 0.3, 1.0);
}
"""

class LVispyviewer(app.Canvas):
    
    def __init__(self, nldata, sample = 32):
        app.Canvas.__init__(self,keys='interactive')
        
        #self._ts = nldata.mmapData['ts']
        self._s = sample
        self._csc = nldata.mmapData['csc']
        
        self.normData = self._csc[:,0][::self._s]/np.max(self._csc[:,0][::self._s])       
        self.timeIndexValues = np.linspace(-1, 1, len(self._csc[:,0]))[::self._s]
        
        self.prog = gloo.Program(vertex, frag)
        
        self.prog['position'] =  np.c_[self.timeIndexValues, self.normData].astype(np.float32)
       
        #self.prog['color'] = [ (1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1) ]       
        self.prog['scale'] = (0.5, 0.1)
        self.prog['pan'] = -0.5, 0.0
        self.prog['maxValue'] = np.max(self._csc[:,0][::self._s])
        #self.prog['position'] = self._csc[:,0][::self._s].astype(np.float32)
        #self.prog['timeIndex'] = self.timeIndexValues.astype(np.float32)
        self.show()
        app.run()
        
    def on_draw(self, e):
        gloo.clear((0.0, 0.1, 0.1, 1))
        self.prog.draw('line_strip')
        
    def on_resize(self, e):
        gloo.set_viewport(0, 0, *e.physical_size)
    
    def on_key_press(self, e):
        if(e.text == '2'):
            self._changeSamples(16)

        elif(e.text == '3'):
            self._changeSamples(32)

        elif(e.text=='1'):
            self._changeSamples(1)

        elif(e.text == '4'):
            self._changeSamples(64)
        elif(e.text == 'g'):
            print(self.prog['scale'])
#        
    def _changeSamples(self, sample):
        #self.prog['position'] = self._csc[:,0][::sample].astype(np.float32)
        
        #self.prog['timeIndex'] = self.timeIndexValues[::sample].astype(np.float32)
        self.prog['position'] =  np.c_[self.timeIndexValues[::sample],
                                          #self._csc[:,0][::sample]].astype(np.float32)
                                          

        #self.prog['position.x'] = self.timeIndexValues[::sample].astype(np.float32)
        #self.prog['position.y'] = self._csc[:,0][::sample].astype(np.float32)
        #self.prog['maxValue'] = np.max(self._csc[:,0][::sample])
        self.update()
                      

#    def autoScaleTest(self):
#        if(self.prog['scale'][0] < 5.0):
#            self._changeSamples(64)
#        elif(self.prog['scale'][0] < 10.0):
#            self._changeSamples(32)
#        elif(self.prog['scale'][0] < 50.0 ):
#            self._changeSamples(16)
#        else:
#            self._changeSamples(1)
            
    #code form the vispy examples, to test. For final, need to limit y movement
    #as it distorts the data
    
#    def on_mouse_move(self, e):
#        if e.is_dragging:
#            x0 = self._norm(e.press_event.pos[0])
#            x1 = self._norm(e.last_event.pos[0])
#            x = self._norm(e.pos[0])
#            
#            dx = x-x1
#            btn = e.press_event.button
#            pan_x = self.prog['pan']
#            if btn == 1:
#                self.prog['pan'] = pan_x + dx
#                self.update()
    
    #test code from vispy github
    def on_mouse_move(self, event):
        if event.is_dragging:
            x0, y0 = self._normalize(event.press_event.pos)
            x1, y1 = self._normalize(event.last_event.pos)
            x, y = self._normalize(event.pos)
            dx, dy = x - x1, -(y - y1)
            button = event.press_event.button

            pan_x, pan_y = self.prog['pan']
            scale_x, scale_y = self.prog['scale']

            if button == 1:
                self.prog['pan'] = (pan_x+dx/scale_x, pan_y+dy/scale_y)
            elif button == 2:
                self.scale_x_new, scale_y_new = (scale_x * math.exp(2.5*dx),
                                            scale_y * math.exp(2.5*dy))
                self.prog['scale'] = (self.scale_x_new, scale_y_new)
                self.prog['pan'] = (pan_x -
                                         x0 * (1./scale_x - 1./self.scale_x_new),
                                         pan_y +
                                         y0 * (1./scale_y - 1./scale_y_new))
            #self.autoScaleTest()
            self.update()
   
    def on_mouse_wheel(self, event):
        dx = np.sign(event.delta[1])*.05
        scale_x, scale_y = self.prog['scale']
        scale_x_new, scale_y_new = (scale_x * math.exp(2.5*dx),
                                    scale_y * math.exp(2.5*dx))
        self.prog['scale'] = (scale_x_new, scale_y_new)
        #self.autoScaleTest()
        self.update()
        
    def _normalize(self, x_y):
        x, y = x_y
        w, h = float(self.size[0]), float(self.size[1])
        return x/(w/2.)-1., y/(h/2.)-1
        
    def _norm(self,x):
        w = float(self.size[0])
        return x/(w/2.0) -1.0
        


