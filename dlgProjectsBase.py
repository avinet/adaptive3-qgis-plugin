# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlgProjectsBase.ui'
#
# Created: Sun Oct 19 23:16:27 2014
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

class Ui_ProjectsDialog(object):
    def setupUi(self, ProjectsDialog):
        ProjectsDialog.setObjectName(_fromUtf8("ProjectsDialog"))
        ProjectsDialog.setWindowModality(QtCore.Qt.NonModal)
        ProjectsDialog.resize(500, 388)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProjectsDialog.sizePolicy().hasHeightForWidth())
        ProjectsDialog.setSizePolicy(sizePolicy)
        ProjectsDialog.setMinimumSize(QtCore.QSize(500, 80))
        ProjectsDialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.gridLayout = QtGui.QGridLayout(ProjectsDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.treeProjects = QtGui.QTreeWidget(ProjectsDialog)
        self.treeProjects.setRootIsDecorated(False)
        self.treeProjects.setItemsExpandable(False)
        self.treeProjects.setObjectName(_fromUtf8("treeProjects"))
        self.treeProjects.header().setVisible(False)
        self.gridLayout.addWidget(self.treeProjects, 0, 0, 1, 4)
        self.buttonRemove = QtGui.QPushButton(ProjectsDialog)
        self.buttonRemove.setObjectName(_fromUtf8("buttonRemove"))
        self.gridLayout.addWidget(self.buttonRemove, 1, 1, 1, 1)
        self.buttonLoad = QtGui.QPushButton(ProjectsDialog)
        self.buttonLoad.setObjectName(_fromUtf8("buttonLoad"))
        self.gridLayout.addWidget(self.buttonLoad, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ProjectsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setAutoFillBackground(False)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 2, 1, 2)

        self.retranslateUi(ProjectsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("clicked(QAbstractButton*)")), ProjectsDialog.close)
        QtCore.QMetaObject.connectSlotsByName(ProjectsDialog)
        ProjectsDialog.setTabOrder(self.treeProjects, self.buttonLoad)
        ProjectsDialog.setTabOrder(self.buttonLoad, self.buttonBox)
        ProjectsDialog.setTabOrder(self.buttonBox, self.buttonRemove)

    def retranslateUi(self, ProjectsDialog):
        ProjectsDialog.setWindowTitle(_translate("ProjectsDialog", "Adaptive services", None))
        self.treeProjects.headerItem().setText(0, _translate("ProjectsDialog", "file", None))
        self.buttonRemove.setText(_translate("ProjectsDialog", "Delete", None))
        self.buttonLoad.setText(_translate("ProjectsDialog", "Load", None))

import resources_rc
