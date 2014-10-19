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
    def __init__(self, iface, projects):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.projects = projects
        self.buttonLoad.setEnabled(False)
        self.buttonRemove.setEnabled(False)
        self.buttonRemove.released.connect(self.deleteProject)
        self.buttonLoad.released.connect(self.loadProject)
        self.treeProjects.itemSelectionChanged.connect(self.selectionChanged)
        self.fillTree()



    def fillTree(self):
        self.treeProjects.clear()
        for project in self.projects:
                item = QTreeWidgetItem(self.treeProjects)
                item.setText(0, project['fileName'] )
        self.treeProjects.resizeColumnToContents(0)



    def selectionChanged(self):
        isSelection = bool(self.treeProjects.selectedItems())
        self.buttonRemove.setEnabled( isSelection )
        self.buttonLoad.setEnabled( isSelection )



    def deleteProject(self):
        if not bool(self.treeProjects.selectedItems()):
            return
        fileName = self.treeProjects.selectedItems()[0].text(0)
        if QMessageBox.question(self, "Adaptive", u"Are you sure you want to remove service %s?\nOperation can not be reversed!" % fileName, QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:

            result = ""
            ok = False
            askForCredentials = True
            while not ok and askForCredentials:
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
                        askForCredentials = False
            if not ok:
                QMessageBox.critical(self, u'Error!', u'Unable to write data to Adaptive')
                return
            ok,resp = listProjectFiles()
            if ok:
                self.projects = resp
            self.fillTree()



    def loadProject(self):
        if not bool(self.treeProjects.selectedItems()):
            return
        fileName = self.treeProjects.selectedItems()[0].text(0)

        xml = ""
        ok = False
        askForCredentials = True
        while not ok and askForCredentials:
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
                    askForCredentials = False
        if not ok:
            QMessageBox.critical(self, u'Error!', u'Unable to read data from Adaptive')
            return
        QApplication.setOverrideCursor(Qt.WaitCursor)
        projectFile = QFile( QDir.tempPath()+'/'+fileName )
        projectFile.open(QIODevice.ReadWrite)
        projectFile.write(xml)
        projectFile.close()
        proj = QgsProject.instance()
        proj.read(QFileInfo(projectFile.fileName()))
        QApplication.restoreOverrideCursor()
        self.close()

