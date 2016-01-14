# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from dlgNewProjectBase import Ui_NewProjectDialogBase


class NewProjectDialog(QDialog, Ui_NewProjectDialogBase):
  def __init__(self, parent):
    QDialog.__init__(self)
    self.setupUi(self)
