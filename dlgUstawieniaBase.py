# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlgUstawieniaBase.ui'
#
# Created: Tue Jan 14 16:05:44 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_UstawieniaDialog(object):
    def setupUi(self, UstawieniaDialog):
        UstawieniaDialog.setObjectName(_fromUtf8("UstawieniaDialog"))
        UstawieniaDialog.setWindowModality(QtCore.Qt.NonModal)
        UstawieniaDialog.resize(511, 84)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UstawieniaDialog.sizePolicy().hasHeightForWidth())
        UstawieniaDialog.setSizePolicy(sizePolicy)
        UstawieniaDialog.setMinimumSize(QtCore.QSize(500, 80))
        UstawieniaDialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.gridLayout = QtGui.QGridLayout(UstawieniaDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(UstawieniaDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(UstawieniaDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setAutoFillBackground(False)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 2)
        self.comboUstawBaza = QtGui.QComboBox(UstawieniaDialog)
        self.comboUstawBaza.setObjectName(_fromUtf8("comboUstawBaza"))
        self.gridLayout.addWidget(self.comboUstawBaza, 0, 1, 1, 2)
        self.label_2.setBuddy(self.comboUstawBaza)

        self.retranslateUi(UstawieniaDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("clicked(QAbstractButton*)")), UstawieniaDialog.close)
        QtCore.QMetaObject.connectSlotsByName(UstawieniaDialog)
        UstawieniaDialog.setTabOrder(self.comboUstawBaza, self.buttonBox)

    def retranslateUi(self, UstawieniaDialog):
        UstawieniaDialog.setWindowTitle(_translate("UstawieniaDialog", "Adaptive: Plugin settings", None))
        self.label_2.setText(_translate("UstawieniaDialog", "Database", None))

import resources_rc
