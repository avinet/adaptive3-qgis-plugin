# -*- coding: utf-8 -*-
#from PyQt4.QtCore import *
from PyQt4.QtGui import *
from dlgHasloPodajBase import Ui_PodajHasloDialogBase


class PodajHasloDialog(QDialog, Ui_PodajHasloDialogBase):
  def __init__(self, parent):
    QDialog.__init__(self)
    self.setupUi(self)
