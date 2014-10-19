# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from dlgEnterPasswordBase import Ui_EnterPasswordDialogBase


class EnterPasswordDialog(QDialog, Ui_EnterPasswordDialogBase):
  def __init__(self, parent):
    QDialog.__init__(self)
    self.setupUi(self)
