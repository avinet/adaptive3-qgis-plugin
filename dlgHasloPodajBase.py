# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlgHasloPodajBase.ui'
#
# Created: Thu Dec 19 20:04:37 2013
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

class Ui_PodajHasloDialogBase(object):
    def setupUi(self, PodajHasloDialogBase):
        PodajHasloDialogBase.setObjectName(_fromUtf8("PodajHasloDialogBase"))
        PodajHasloDialogBase.resize(440, 121)
        self.gridLayout = QtGui.QGridLayout(PodajHasloDialogBase)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(PodajHasloDialogBase)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)
        self.label = QtGui.QLabel(PodajHasloDialogBase)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.lineUser = QtGui.QLineEdit(PodajHasloDialogBase)
        self.lineUser.setObjectName(_fromUtf8("lineUser"))
        self.gridLayout.addWidget(self.lineUser, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(PodajHasloDialogBase)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.linePass = QtGui.QLineEdit(PodajHasloDialogBase)
        self.linePass.setEchoMode(QtGui.QLineEdit.Password)
        self.linePass.setObjectName(_fromUtf8("linePass"))
        self.gridLayout.addWidget(self.linePass, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(PodajHasloDialogBase)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.labelError = QtGui.QLabel(PodajHasloDialogBase)
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

        self.retranslateUi(PodajHasloDialogBase)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PodajHasloDialogBase.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PodajHasloDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(PodajHasloDialogBase)

    def retranslateUi(self, PodajHasloDialogBase):
        PodajHasloDialogBase.setWindowTitle(_translate("PodajHasloDialogBase", "Password required", None))
        self.label_3.setText(_translate("PodajHasloDialogBase", "Please provide you Adaptive username and password", None))
        self.label.setText(_translate("PodajHasloDialogBase", "Username", None))
        self.label_2.setText(_translate("PodajHasloDialogBase", "Password", None))
        self.labelError.setText(_translate("PodajHasloDialogBase", "Error!", None))

