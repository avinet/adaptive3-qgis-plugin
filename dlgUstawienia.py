# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from dlgUstawieniaBase import Ui_UstawieniaDialog
from adaptive_data import *

#----------------------------------------------------------------------------


class UstawieniaDialog(QDialog, Ui_UstawieniaDialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.wypelnijBazeDanych()



    def wypelnijBazeDanych(self):
        settings = QSettings()
        selected = settings.value("/PostgreSQL/connections/selected", type=unicode)
        selected = ustawienia('bazaDanych', selected)
        settings.beginGroup("/PostgreSQL/connections")
        keys = settings.childGroups()
        currentIdx = 0
        for key in keys:
            self.comboUstawBaza.addItem(unicode(key))
            if unicode(key) == selected: currentIdx = self.comboUstawBaza.count()-1
        settings.endGroup()
        self.comboUstawBaza.setCurrentIndex(currentIdx)
        self.staraBaza = self.comboUstawBaza.currentText()



    def close(self):
        ustawUstawienia('bazaDanych', self.comboUstawBaza.currentText())
        if self.comboUstawBaza.currentText() != self.staraBaza:
            QMessageBox.warning(self.iface.mainWindow(), "Adaptive", u"Database has been changed. Please restart the application.")
        QDialog.close(self)