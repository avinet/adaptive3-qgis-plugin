# -*- coding: utf-8 -*-
#from PyQt4.QtCore import *
from PyQt4.QtGui import *
from dlgHasloPodajBase import Ui_PodajHasloDialogBase


class EnterPasswordDialog(QDialog, Ui_EnterPasswordDialogBase):
  def __init__(self, parent):
    QDialog.__init__(self)
    self.setupUi(self)
