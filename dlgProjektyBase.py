# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlgProjektyBase.ui'
#
# Created: Fri Mar 28 16:40:59 2014
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

class Ui_ProjektyDialog(object):
    def setupUi(self, ProjektyDialog):
        ProjektyDialog.setObjectName(_fromUtf8("ProjektyDialog"))
        ProjektyDialog.setWindowModality(QtCore.Qt.NonModal)
        ProjektyDialog.resize(500, 388)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProjektyDialog.sizePolicy().hasHeightForWidth())
        ProjektyDialog.setSizePolicy(sizePolicy)
        ProjektyDialog.setMinimumSize(QtCore.QSize(500, 80))
        ProjektyDialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.gridLayout = QtGui.QGridLayout(ProjektyDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.treeProjekty = QtGui.QTreeWidget(ProjektyDialog)
        self.treeProjekty.setRootIsDecorated(False)
        self.treeProjekty.setItemsExpandable(False)
        self.treeProjekty.setObjectName(_fromUtf8("treeProjekty"))
        self.treeProjekty.headerItem().setTextAlignment(1, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.treeProjekty.header().setVisible(False)
        self.gridLayout.addWidget(self.treeProjekty, 0, 0, 1, 4)
        self.buttonUsun = QtGui.QPushButton(ProjektyDialog)
        self.buttonUsun.setObjectName(_fromUtf8("buttonUsun"))
        self.gridLayout.addWidget(self.buttonUsun, 1, 1, 1, 1)
        self.buttonWczytaj = QtGui.QPushButton(ProjektyDialog)
        self.buttonWczytaj.setObjectName(_fromUtf8("buttonWczytaj"))
        self.gridLayout.addWidget(self.buttonWczytaj, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ProjektyDialog)
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

        self.retranslateUi(ProjektyDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("clicked(QAbstractButton*)")), ProjektyDialog.close)
        QtCore.QMetaObject.connectSlotsByName(ProjektyDialog)
        ProjektyDialog.setTabOrder(self.treeProjekty, self.buttonWczytaj)
        ProjektyDialog.setTabOrder(self.buttonWczytaj, self.buttonBox)
        ProjektyDialog.setTabOrder(self.buttonBox, self.buttonUsun)

    def retranslateUi(self, ProjektyDialog):
        ProjektyDialog.setWindowTitle(_translate("ProjektyDialog", "Adaptive: QGIS services", None))
        self.treeProjekty.headerItem().setText(0, _translate("ProjektyDialog", "file", None))
        self.treeProjekty.headerItem().setText(1, _translate("ProjektyDialog", "description", None))
        self.buttonUsun.setText(_translate("ProjektyDialog", "Delete", None))
        self.buttonWczytaj.setText(_translate("ProjektyDialog", "Load", None))

import resources_rc
