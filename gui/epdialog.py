# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ep.ui'
#
# Created: Thu Nov 26 17:41:46 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_EvokedPotentialDialog(object):
    def setupUi(self, EvokedPotentialDialog):
        EvokedPotentialDialog.setObjectName(_fromUtf8("EvokedPotentialDialog"))
        EvokedPotentialDialog.resize(400, 173)
        self.comboBox = QtGui.QComboBox(EvokedPotentialDialog)
        self.comboBox.setGeometry(QtCore.QRect(30, 30, 331, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.stimchannelbox = QtGui.QSpinBox(EvokedPotentialDialog)
        self.stimchannelbox.setGeometry(QtCore.QRect(320, 60, 42, 22))
        self.stimchannelbox.setMinimum(1)
        self.stimchannelbox.setMaximum(20)
        self.stimchannelbox.setObjectName(_fromUtf8("stimchannelbox"))
        self.label = QtGui.QLabel(EvokedPotentialDialog)
        self.label.setGeometry(QtCore.QRect(190, 60, 131, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.calculateButton = QtGui.QPushButton(EvokedPotentialDialog)
        self.calculateButton.setGeometry(QtCore.QRect(210, 130, 75, 23))
        self.calculateButton.setObjectName(_fromUtf8("calculateButton"))
        self.quitButton = QtGui.QPushButton(EvokedPotentialDialog)
        self.quitButton.setGeometry(QtCore.QRect(290, 130, 75, 23))
        self.quitButton.setObjectName(_fromUtf8("quitButton"))
        self.leftradio = QtGui.QRadioButton(EvokedPotentialDialog)
        self.leftradio.setGeometry(QtCore.QRect(30, 10, 82, 17))
        self.leftradio.setObjectName(_fromUtf8("leftradio"))
        self.rightradio = QtGui.QRadioButton(EvokedPotentialDialog)
        self.rightradio.setGeometry(QtCore.QRect(80, 10, 82, 17))
        self.rightradio.setObjectName(_fromUtf8("rightradio"))
        self.seg1 = QtGui.QCheckBox(EvokedPotentialDialog)
        self.seg1.setGeometry(QtCore.QRect(30, 80, 70, 17))
        self.seg1.setObjectName(_fromUtf8("seg1"))
        self.seg2 = QtGui.QCheckBox(EvokedPotentialDialog)
        self.seg2.setGeometry(QtCore.QRect(30, 100, 70, 17))
        self.seg2.setObjectName(_fromUtf8("seg2"))
        self.seg3 = QtGui.QCheckBox(EvokedPotentialDialog)
        self.seg3.setGeometry(QtCore.QRect(30, 120, 70, 17))
        self.seg3.setObjectName(_fromUtf8("seg3"))
        self.seg4 = QtGui.QCheckBox(EvokedPotentialDialog)
        self.seg4.setGeometry(QtCore.QRect(30, 140, 70, 17))
        self.seg4.setObjectName(_fromUtf8("seg4"))
        self.label_2 = QtGui.QLabel(EvokedPotentialDialog)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 47, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(EvokedPotentialDialog)
        QtCore.QMetaObject.connectSlotsByName(EvokedPotentialDialog)

    def retranslateUi(self, EvokedPotentialDialog):
        EvokedPotentialDialog.setWindowTitle(_translate("EvokedPotentialDialog", "EvokedPotentialDialog", None))
        self.comboBox.setItemText(0, _translate("EvokedPotentialDialog", "RFA", None))
        self.comboBox.setItemText(1, _translate("EvokedPotentialDialog", "M1", None))
        self.comboBox.setItemText(2, _translate("EvokedPotentialDialog", "DMS", None))
        self.comboBox.setItemText(3, _translate("EvokedPotentialDialog", "DLS", None))
        self.comboBox.setItemText(4, _translate("EvokedPotentialDialog", "GP", None))
        self.comboBox.setItemText(5, _translate("EvokedPotentialDialog", "Thal", None))
        self.comboBox.setItemText(6, _translate("EvokedPotentialDialog", "STN", None))
        self.comboBox.setItemText(7, _translate("EvokedPotentialDialog", "SNr", None))
        self.label.setText(_translate("EvokedPotentialDialog", "Main Stimulation Channel", None))
        self.calculateButton.setText(_translate("EvokedPotentialDialog", "Calculate EP", None))
        self.quitButton.setText(_translate("EvokedPotentialDialog", "Quit", None))
        self.leftradio.setText(_translate("EvokedPotentialDialog", "Left", None))
        self.rightradio.setText(_translate("EvokedPotentialDialog", "Right", None))
        self.seg1.setText(_translate("EvokedPotentialDialog", "1", None))
        self.seg2.setText(_translate("EvokedPotentialDialog", "2", None))
        self.seg3.setText(_translate("EvokedPotentialDialog", "3", None))
        self.seg4.setText(_translate("EvokedPotentialDialog", "4", None))
        self.label_2.setText(_translate("EvokedPotentialDialog", "Segment", None))

