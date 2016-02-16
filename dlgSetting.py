# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from dlgSettingBase import Ui_Dialog


class SettingDialog(QDialog, Ui_Dialog):
  def __init__(self, parent):
    QDialog.__init__(self)
    self.setupUi(self)
    self.buttonBox.accepted.connect(self.saveSettings)
    self.loadSettings()
    
  def saveSettings(self):
    settings = QSettings()
    settings.setValue('a3_url', self.lineEdit.text())
    
  def loadSettings(self):
    settings = QSettings()
    if not settings.contains('a3_url'):
        settings.setValue('a3_url', '')
    
    servicePath = settings.value('a3_url', type=str)
    self.lineEdit.setText(servicePath)