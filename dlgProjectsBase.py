# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlgProjectsBase.ui'
#
# Created: Sat Oct 18 21:21:26 2014
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
        self.treeProjekty = QtGui.QTreeWidget(ProjectsDialog)
        self.treeProjekty.setRootIsDecorated(False)
        self.treeProjekty.setItemsExpandable(False)
        self.treeProjekty.setObjectName(_fromUtf8("treeProjekty"))
        self.treeProjekty.headerItem().setTextAlignment(1, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.treeProjekty.header().setVisible(False)
        self.gridLayout.addWidget(self.treeProjekty, 0, 0, 1, 4)
        self.buttonUsun = QtGui.QPushButton(ProjectsDialog)
        self.buttonUsun.setObjectName(_fromUtf8("buttonUsun"))
        self.gridLayout.addWidget(self.buttonUsun, 1, 1, 1, 1)
        self.buttonWczytaj = QtGui.QPushButton(ProjectsDialog)
        self.buttonWczytaj.setObjectName(_fromUtf8("buttonWczytaj"))
        self.gridLayout.addWidget(self.buttonWczytaj, 1, 0, 1, 1)
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
        ProjectsDialog.setTabOrder(self.treeProjekty, self.buttonWczytaj)
        ProjectsDialog.setTabOrder(self.buttonWczytaj, self.buttonBox)
        ProjectsDialog.setTabOrder(self.buttonBox, self.buttonUsun)

    def retranslateUi(self, ProjectsDialog):
        ProjectsDialog.setWindowTitle(_translate("ProjectsDialog", "GEOPANEL: Usługi WMS", None))
        self.treeProjekty.headerItem().setText(0, _translate("ProjectsDialog", "plik", None))
        self.treeProjekty.headerItem().setText(1, _translate("ProjectsDialog", "opis", None))
        self.buttonUsun.setText(_translate("ProjectsDialog", "Usuń", None))
        self.buttonWczytaj.setText(_translate("ProjectsDialog", "Wczytaj", None))

import resources_rc
