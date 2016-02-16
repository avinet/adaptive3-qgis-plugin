# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from dlgProjectsBase import Ui_ProjectsDialog
import adaptive_data
import adaptiveUtils
from publishing import listProjectFiles, deleteProjectFile, readProjectFile

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
                item.object = project
                item.setText(0, project['name'])
                item.setText(1, project['filename'])

    def selectionChanged(self):
        isSelection = bool(self.treeProjects.selectedItems())
        self.buttonRemove.setEnabled( isSelection )
        self.buttonLoad.setEnabled( isSelection )



    def deleteProject(self):
        if not bool(self.treeProjects.selectedItems()):
            return
        fileName = self.treeProjects.selectedItems()[0].text(0)
        fileUuid = self.treeProjects.selectedItems()[0].object["uuid"]
        if QMessageBox.question(self, self.tr("Adaptive"), self.tr(u"Are you sure you want to remove service %s?\nOperation can not be reversed!") % fileName, QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:

            errorMessage = ""
            operationOk = False
            authOk = False
            askForCredentials = True
            while not authOk and askForCredentials:
                if adaptive_data.token:
                    QApplication.setOverrideCursor(Qt.WaitCursor)
                    authOk,operationOk,errorMessage = deleteProjectFile(unicode(fileUuid))
                    QApplication.restoreOverrideCursor()
                if not authOk:
                    askForCredentials = adaptiveUtils.authenticateUser(self)
                else:
                    askForCredentials = False
            if not operationOk:
                QMessageBox.critical(self, self.tr(u'Error!'), errorMessage)
                return
            authOk,operationOk,resp = listProjectFiles()
            if authOk and operationOk:
                self.projects = resp
            self.fillTree()



    def loadProject(self):
        if not bool(self.treeProjects.selectedItems()):
            return
        fileName = self.treeProjects.selectedItems()[0].object["filename"]
        fileUuid = self.treeProjects.selectedItems()[0].object["uuid"]

        xmlOrError = ""
        authOk = False
        operationOk = False
        askForCredentials = True
        while not authOk and askForCredentials:
            if adaptive_data.token:
                QApplication.setOverrideCursor(Qt.WaitCursor)
                authOk, operationOk, xmlOrError = readProjectFile(unicode(fileUuid))
                QApplication.restoreOverrideCursor()
            if not authOk:
                askForCredentials = adaptiveUtils.authenticateUser(self)
            else:
                askForCredentials = False
        if not operationOk:
            QMessageBox.critical(self, self.tr(u'Error!'), xmlOrError)
            return
        QApplication.setOverrideCursor(Qt.WaitCursor)
        QFile.remove(QDir.tempPath()+'/'+fileName)
        projectFile = QFile( QDir.tempPath()+'/'+fileName )
        projectFile.open(QIODevice.ReadWrite | QIODevice.Truncate)
        projectFile.write(xmlOrError)
        projectFile.flush()
        projectFile.close()
        proj = QgsProject.instance()
        proj.clear()
        proj.read(QFileInfo(projectFile.fileName()))
        QApplication.restoreOverrideCursor()
        self.close()