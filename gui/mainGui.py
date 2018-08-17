from PyQt4 import QtGui
import sys

import epdialog
from neuralpanda import pStructure, pStimSegment, pEvokedPotential
from neuralpanda.analyser import aEvokedPotential
import Utils.channelInfoParser as cip
import visView.visViewApp as vspa

class Example(QtGui.QWidget, epdialog.Ui_EvokedPotentialDialog):
    
    def __init__(self, nldata, nlevents, pseg):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setupChannelInfo()
        self.nd = nldata
        self.ne = nlevents
        self.pSeg = pseg
        
        self.calculateButton.clicked.connect(self.calculateEp)
        self.quitButton.clicked.connect(self.showvsp)
        
    def showvsp(self):
        vspa.visViewApp(self.nd, self._genStructure(), self.pSeg)
        
    def calculateEp(self):
        aEvokedPotential.aEvokedPotential(*self._genPep())
        
    def _genPep(self):
        if self.seg1.isChecked():
            a = pEvokedPotential.pEvokedPotential(self.nd, self.ne, self._genStructure(), 0)
                                                     
        if self.seg2.isChecked():
            b = pEvokedPotential.pEvokedPotential(self.nd, self.ne, self._genStructure(), 1)
                                                
        if self.seg3.isChecked():
            c = pEvokedPotential.pEvokedPotential(self.nd, self.ne, self._genStructure(), 2)

        if self.seg4.isChecked():
            d = pEvokedPotential.pEvokedPotential(self.nd, self.ne, self._genStructure(), 3)
        
        return a,b,c,d
        
    def _genStructure(self):
        sname = str(self.comboBox.currentText())
        mainStim = self.stimchannelbox.value()
        d =""
        _a=""

        if self.leftradio.isChecked():
            d = "Left "
            _a = "self.chninfo.l_"+sname.lower()
            
        if self.rightradio.isChecked():
            d = "Right "
            _a = "self.chninfo.r_"+sname.lower()
        
        print _a
        return pStructure.pStructure(d + sname, eval(_a), mainStim)
        
        
    def setupChannelInfo(self):
         #setup channel info
        self.chninfo = cip.ChannelInfoParser()
#        
#        #left channels for Stim3
#        self.chninfo.l_rfa = self.chninfo.excludeChannels(self.chninfo.l_rfa, [6,7])
#        self.chninfo.l_m1 = self.chninfo.excludeChannels(self.chninfo.l_m1, [11,12])
#        self.chninfo.l_dls = self.chninfo.excludeChannels(self.chninfo.l_dls, [16,22])
#        self.chninfo.l_gp = self.chninfo.excludeChannels(self.chninfo.l_gp, [34,35,65])
#        self.chninfo.l_snr = self.chninfo.excludeChannels(self.chninfo.l_snr, [56,57])
#        self.chninfo.l_dms = self.chninfo.excludeChannels(self.chninfo.l_dms, [27,28])
#        self.chninfo.l_stn = self.chninfo.excludeChannels(self.chninfo.l_stn, [47])
#        self.chninfo.l_thal = self.chninfo.excludeChannels(self.chninfo.l_thal, [42,44])
#        
#        #right channels
#        self.chninfo.r_rfa = self.chninfo.excludeChannels(self.chninfo.r_rfa, [97,98,100])
#        self.chninfo.r_m1 = self.chninfo.excludeChannels(self.chninfo.r_m1, [105,106,108,110,111])
#        self.chninfo.r_dls = self.chninfo.excludeChannels(self.chninfo.r_dls, [112])
#        self.chninfo.r_gp = self.chninfo.excludeChannels(self.chninfo.r_gp, [66,68,69,70])
#        self.chninfo.r_snr = self.chninfo.excludeChannels(self.chninfo.r_snr, [87])
#        self.chninfo.r_dms = self.chninfo.excludeChannels(self.chninfo.r_dms, [121,122])
#        self.chninfo.r_stn = self.chninfo.excludeChannels(self.chninfo.r_stn, [])
#        self.chninfo.r_thal = self.chninfo.excludeChannels(self.chninfo.r_thal, [72,74,75,76,77])
#        
        #left channels for Stim4
        self.chninfo.l_rfa = self.chninfo.excludeChannels(self.chninfo.l_rfa, [6,7])
        self.chninfo.l_m1 = self.chninfo.excludeChannels(self.chninfo.l_m1, [])
        self.chninfo.l_dls = self.chninfo.excludeChannels(self.chninfo.l_dls, [])
        self.chninfo.l_gp = self.chninfo.excludeChannels(self.chninfo.l_gp, [])
        self.chninfo.l_snr = self.chninfo.excludeChannels(self.chninfo.l_snr, [])
        self.chninfo.l_dms = self.chninfo.excludeChannels(self.chninfo.l_dms, [28])
        self.chninfo.l_stn = self.chninfo.excludeChannels(self.chninfo.l_stn, [])
        self.chninfo.l_thal = self.chninfo.excludeChannels(self.chninfo.l_thal, [])
        
        #right channels
        self.chninfo.r_rfa = self.chninfo.excludeChannels(self.chninfo.r_rfa, [99])
        self.chninfo.r_m1 = self.chninfo.excludeChannels(self.chninfo.r_m1, [107,112,111])
        self.chninfo.r_dls = self.chninfo.excludeChannels(self.chninfo.r_dls, [])
        self.chninfo.r_gp = self.chninfo.excludeChannels(self.chninfo.r_gp, [])
        self.chninfo.r_snr = self.chninfo.excludeChannels(self.chninfo.r_snr, [])
        self.chninfo.r_dms = self.chninfo.excludeChannels(self.chninfo.r_dms, [])
        self.chninfo.r_stn = self.chninfo.excludeChannels(self.chninfo.r_stn, [])
        self.chninfo.r_thal = self.chninfo.excludeChannels(self.chninfo.r_thal, [76])
#        