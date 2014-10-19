# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlgEnterPasswordBase.ui'
#
# Created: Sun Oct 19 23:09:48 2014
#      by: PyQt4 UI code generator 4.11.2
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

class Ui_EnterPasswordDialogBase(object):
    def setupUi(self, EnterPasswordDialogBase):
        EnterPasswordDialogBase.setObjectName(_fromUtf8("EnterPasswordDialogBase"))
        EnterPasswordDialogBase.resize(440, 125)
        self.gridLayout = QtGui.QGridLayout(EnterPasswordDialogBase)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(EnterPasswordDialogBase)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)
        self.label = QtGui.QLabel(EnterPasswordDialogBase)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.lineUser = QtGui.QLineEdit(EnterPasswordDialogBase)
        self.lineUser.setObjectName(_fromUtf8("lineUser"))
        self.gridLayout.addWidget(self.lineUser, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(EnterPasswordDialogBase)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.linePass = QtGui.QLineEdit(EnterPasswordDialogBase)
        self.linePass.setEchoMode(QtGui.QLineEdit.Password)
        self.linePass.setObjectName(_fromUtf8("linePass"))
        self.gridLayout.addWidget(self.linePass, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(EnterPasswordDialogBase)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.labelError = QtGui.QLabel(EnterPasswordDialogBase)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 95))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(118, 117, 115))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.labelError.setPalette(palette)
        self.labelError.setObjectName(_fromUtf8("labelError"))
        self.gridLayout.addWidget(self.labelError, 3, 1, 1, 1)
        self.label.setBuddy(self.lineUser)
        self.label_2.setBuddy(self.linePass)

        self.retranslateUi(EnterPasswordDialogBase)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EnterPasswordDialogBase.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EnterPasswordDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(EnterPasswordDialogBase)

    def retranslateUi(self, EnterPasswordDialogBase):
        EnterPasswordDialogBase.setWindowTitle(_translate("EnterPasswordDialogBase", "Log in", None))
        self.label_3.setText(_translate("EnterPasswordDialogBase", "Please enter your credentials to the Adaptive service", None))
        self.label.setText(_translate("EnterPasswordDialogBase", "Login", None))
        self.label_2.setText(_translate("EnterPasswordDialogBase", "Password", None))
        self.labelError.setText(_translate("EnterPasswordDialogBase", "ERROR", None))

