# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import QDomDocument
from qgis.core import *
from dlgProjectsBase import Ui_ProjectsDialog
from dlgEnterPassword import EnterPasswordDialog
import adaptive_data
from adaptive_data import *
from publishing import authenticate, listProjectFiles, deleteProjectFile, readProjectFile

#----------------------------------------------------------------------------


class ProjectsDialog(QDialog, Ui_ProjectsDialog):
    def __init__(self, iface, projekty):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.projekty = projekty
        self.buttonWczytaj.setEnabled(False)
        self.buttonUsun.setEnabled(False)
        self.buttonUsun.released.connect(self.deleteProject)
        self.buttonWczytaj.released.connect(self.loadProject)
        self.treeProjekty.itemSelectionChanged.connect(self.selectionChanged)
        self.fillTree()



    def fillTree(self):
        self.treeProjekty.clear()
        for projekt in self.projekty:
                item = QTreeWidgetItem(self.treeProjekty)
                item.setText(0, projekt['fileName'] )
        self.treeProjekty.resizeColumnToContents(0)



    def selectionChanged(self):
        cosWybrano = bool(self.treeProjekty.selectedItems())
        self.buttonUsun.setEnabled( cosWybrano )
        self.buttonWczytaj.setEnabled( cosWybrano )



    def deleteProject(self):
        if not bool(self.treeProjekty.selectedItems()):
            return
        fileName = self.treeProjekty.selectedItems()[0].text(0)
        if QMessageBox.question(self, "Adaptive", u"Are you sure you want to remove service %s?\nOperation can not be reversed!" % fileName, QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:

            result = ""
            ok = False
            pytaj = True
            while not ok and pytaj:
                if adaptive_data.token:
                    QApplication.setOverrideCursor(Qt.WaitCursor)
                    ok,result = deleteProjectFile(unicode(fileName))
                    QApplication.restoreOverrideCursor()
                if not ok:
                    dlg = EnterPasswordDialog(self.iface.mainWindow())
                    dlg.label_3.setText(u"Please provide your Adaptive username and password")
                    dlg.labelError.hide()
                    dlg.lineUser.setText(adaptive_data.token_username)
                    dlg.linePass.setText(adaptive_data.token_password)
                    if adaptive_data.token_username: dlg.linePass.setFocus()
                    dlg.exec_()
                    if dlg.result():
                        adaptive_data.token_username = dlg.lineUser.text()
                        adaptive_data.token_password = dlg.linePass.text()
                        adaptive_data.token = authenticate(adaptive_data.token_username, adaptive_data.token_password)
                    else:
                        #zaniechano
                        pytaj = False
            if not ok:
                QMessageBox.critical(self, u'Error!', u'Unable to write data to Adaptive')
                return
            ok,resp = listProjectFiles()
            if ok:
                self.projekty = resp
            self.fillTree()



    def loadProject(self):
        if not bool(self.treeProjekty.selectedItems()):
            return
        fileName = self.treeProjekty.selectedItems()[0].text(0)

        xml = ""
        ok = False
        pytaj = True
        while not ok and pytaj:
            if adaptive_data.token:
                QApplication.setOverrideCursor(Qt.WaitCursor)
                ok, xml = readProjectFile(unicode(fileName))
                QApplication.restoreOverrideCursor()
            if not ok:
                dlg = EnterPasswordDialog(self.iface.mainWindow())
                dlg.label_3.setText(u"Please provide you Adaptive username and password")
                dlg.labelError.hide()
                dlg.lineUser.setText(adaptive_data.token_username)
                dlg.linePass.setText(adaptive_data.token_password)
                if adaptive_data.token_username: dlg.linePass.setFocus()
                dlg.exec_()
                if dlg.result():
                    adaptive_data.token_username = dlg.lineUser.text()
                    adaptive_data.token_password = dlg.linePass.text()
                    adaptive_data.token = authenticate(adaptive_data.token_username, adaptive_data.token_password)
                else:
                    #zaniechano
                    pytaj = False
        if not ok:
            QMessageBox.critical(self, u'Error!', u'Unable to read data from Adaptive')
            return
        QApplication.setOverrideCursor(Qt.WaitCursor)
        projektPlik = QFile( QDir.tempPath()+'/'+fileName )
        projektPlik.open(QIODevice.ReadWrite)
        projektPlik.write(xml)
        projektPlik.close()
        proj = QgsProject.instance()
        proj.read(QFileInfo(projektPlik.fileName()))
        QApplication.restoreOverrideCursor()
        self.close()

