# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from dlgPublicznyWewnetrznyBase import Ui_PublicznyWewnetrznyDialogBase


class PublicPrivateDialog(QDialog, Ui_PublicPrivateDialogBase):
    def __init__(self, parent, url):
        QDialog.__init__(self)
        self.setupUi(self)
        self.rezultat = 0
        self.labelInfo.setText(u'If you publish this service as private it won\'t be available to guest Adaptive users.' % url)
        self.buttonWewnetrzna.released.connect(self.publishPrivate)
        self.buttonPubliczna.released.connect(self.publishPublic)


    def publishPrivate(self):
        self.rezultat = 1
        self.close()


    def publishPublic(self):
        self.rezultat = 2
        self.close()
