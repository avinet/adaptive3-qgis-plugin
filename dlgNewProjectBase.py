# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlgNewProject.ui'
#
# Created: Fri Apr 01 12:27:36 2016
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

class Ui_NewProjectDialogBase(object):
    def setupUi(self, NewProjectDialogBase):
        NewProjectDialogBase.setObjectName(_fromUtf8("NewProjectDialogBase"))
        NewProjectDialogBase.resize(228, 86)
        self.buttonBox = QtGui.QDialogButtonBox(NewProjectDialogBase)
        self.buttonBox.setGeometry(QtCore.QRect(20, 50, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.splitter = QtGui.QSplitter(NewProjectDialogBase)
        self.splitter.setGeometry(QtCore.QRect(20, 10, 196, 20))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.labelProjectName = QtGui.QLabel(self.splitter)
        self.labelProjectName.setEnabled(True)
        self.labelProjectName.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.labelProjectName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelProjectName.setObjectName(_fromUtf8("labelProjectName"))
        self.lineProjectName = QtGui.QLineEdit(self.splitter)
        self.lineProjectName.setObjectName(_fromUtf8("lineProjectName"))

        self.retranslateUi(NewProjectDialogBase)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NewProjectDialogBase.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NewProjectDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(NewProjectDialogBase)

    def retranslateUi(self, NewProjectDialogBase):
        NewProjectDialogBase.setWindowTitle(_translate("NewProjectDialogBase", "New project", None))
        self.labelProjectName.setText(_translate("NewProjectDialogBase", "Project name", None))

