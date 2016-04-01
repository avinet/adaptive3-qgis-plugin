# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlgUpdateProject.ui'
#
# Created: Fri Apr 01 12:27:32 2016
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_UpdateProjectDialogBase(object):
    def setupUi(self, UpdateProjectDialogBase):
        UpdateProjectDialogBase.setObjectName(_fromUtf8("UpdateProjectDialogBase"))
        UpdateProjectDialogBase.resize(228, 86)
        self.buttonBox = QtGui.QDialogButtonBox(UpdateProjectDialogBase)
        self.buttonBox.setGeometry(QtCore.QRect(20, 50, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.splitter = QtGui.QSplitter(UpdateProjectDialogBase)
        self.splitter.setGeometry(QtCore.QRect(20, 10, 196, 20))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.existingProjectsCombo = QtGui.QComboBox(self.splitter)
        self.existingProjectsCombo.setObjectName(_fromUtf8("existingProjectsCombo"))

        self.retranslateUi(UpdateProjectDialogBase)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), UpdateProjectDialogBase.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), UpdateProjectDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(UpdateProjectDialogBase)

    def retranslateUi(self, UpdateProjectDialogBase):
        UpdateProjectDialogBase.setWindowTitle(_translate("UpdateProjectDialogBase", "Update project", None))

