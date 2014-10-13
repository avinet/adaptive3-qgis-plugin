# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlgPublicznyWewnetrznyBase.ui'
#
# Created: Fri Mar 28 16:42:34 2014
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

class Ui_PublicznyWewnetrznyDialogBase(object):
    def setupUi(self, PublicznyWewnetrznyDialogBase):
        PublicznyWewnetrznyDialogBase.setObjectName(_fromUtf8("PublicznyWewnetrznyDialogBase"))
        PublicznyWewnetrznyDialogBase.resize(522, 188)
        self.gridLayout = QtGui.QGridLayout(PublicznyWewnetrznyDialogBase)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 2)
        self.buttonWewnetrzna = QtGui.QPushButton(PublicznyWewnetrznyDialogBase)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(145, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(155, 155, 154))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.buttonWewnetrzna.setPalette(palette)
        self.buttonWewnetrzna.setObjectName(_fromUtf8("buttonWewnetrzna"))
        self.gridLayout.addWidget(self.buttonWewnetrzna, 1, 0, 1, 1)
        self.buttonPubliczna = QtGui.QPushButton(PublicznyWewnetrznyDialogBase)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 128, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 128, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(155, 155, 154))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.buttonPubliczna.setPalette(palette)
        self.buttonPubliczna.setObjectName(_fromUtf8("buttonPubliczna"))
        self.gridLayout.addWidget(self.buttonPubliczna, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(458, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 5, 0, 1, 2)
        self.label_3 = QtGui.QLabel(PublicznyWewnetrznyDialogBase)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)
        self.labelInfo = QtGui.QLabel(PublicznyWewnetrznyDialogBase)
        self.labelInfo.setTextFormat(QtCore.Qt.RichText)
        self.labelInfo.setWordWrap(True)
        self.labelInfo.setObjectName(_fromUtf8("labelInfo"))
        self.gridLayout.addWidget(self.labelInfo, 4, 0, 1, 2)

        self.retranslateUi(PublicznyWewnetrznyDialogBase)
        QtCore.QMetaObject.connectSlotsByName(PublicznyWewnetrznyDialogBase)

    def retranslateUi(self, PublicznyWewnetrznyDialogBase):
        PublicznyWewnetrznyDialogBase.setWindowTitle(_translate("PublicznyWewnetrznyDialogBase", "Publish WMS", None))
        self.buttonWewnetrzna.setText(_translate("PublicznyWewnetrznyDialogBase", "Private", None))
        self.buttonPubliczna.setText(_translate("PublicznyWewnetrznyDialogBase", "Public", None))
        self.label_3.setText(_translate("PublicznyWewnetrznyDialogBase", "WMS service will be published as:", None))
        self.labelInfo.setText(_translate("PublicznyWewnetrznyDialogBase", "<html><head/><body><p>If you publish this service as private it won\'t be available to guest Adaptive users.</p></body></html>", None))

