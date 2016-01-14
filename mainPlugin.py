# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os.path

import adaptive_data
import adaptiveUtils

from dlgEnterPassword import EnterPasswordDialog
from dlgProjects import ProjectsDialog
from dlgSetting import SettingDialog
from dlgNewProject import NewProjectDialog
from dlgUpdateProject import UpdateProjectDialog

from qgis.core import *

from publishing import  validateProject, uploadProjectFile, listProjectFiles


class AdaptivePlugin():
    # ----------------------------------------- #
    def __init__(self, iface):
        self.iface = iface
        #i18n
        pluginPath = QFileInfo(os.path.realpath(__file__)).path()
        localeName = QLocale.system().name()
        if QFileInfo(pluginPath).exists():
            self.localePath = pluginPath+"/i18n/adaptive_" + localeName + ".qm"
        if QFileInfo(self.localePath).exists():
            self.translator = QTranslator()
            self.translator.load(self.localePath)
            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)



    def initGui(self):
        self.action1 = QAction(QIcon(), QCoreApplication.translate('AdaptivePlugin', u'Projects'), self.iface.mainWindow())
        self.action2 = QAction(QIcon(), QCoreApplication.translate('AdaptivePlugin', u'Create project'), self.iface.mainWindow())
        self.action4 = QAction(QIcon(), QCoreApplication.translate('AdaptivePlugin', u'Update project'), self.iface.mainWindow())
        self.action3 = QAction(QIcon(), QCoreApplication.translate('AdaptivePlugin', u'Settings'), self.iface.mainWindow())
        
        self.action1.setToolTip(QCoreApplication.translate('AdaptivePlugin', u'Adaptive: Browse QGIS project on server'))
        self.action2.setToolTip(QCoreApplication.translate('AdaptivePlugin', u'Adaptive: Publish QGIS project to server'))

        self.action1.triggered.connect(self.runProjects)
        self.action2.triggered.connect(self.runPublish)
        self.action3.triggered.connect(self.runSettings)
        self.action4.triggered.connect(self.runUpdate)

        self.menu = QMenu()
        self.menu.setTitle(QCoreApplication.translate('AdaptivePlugin', "Adaptive"))
        menuBar = self.iface.mainWindow().menuBar()
        lastAction = menuBar.actions()[len(menuBar.actions()) - 1]
        menuBar.insertMenu(lastAction, self.menu)

        for i in [self.action1, self.action2, self.action4, self.action3]:
            self.menu.addAction(i)

    def unload(self):
        for i in [self.action1, self.action2, self.action3, self.action4]:
            self.iface.removePluginMenu(QCoreApplication.translate('AdaptivePlugin', 'Adaptive'), i)

    def runProjects(self):
        resp = ""
        authOk = False
        operationOk = False
        askForCredentials = True
        while not authOk and askForCredentials:
            if adaptive_data.token:
                QApplication.setOverrideCursor(Qt.WaitCursor)
                authOk,operationOk,resp = listProjectFiles()
                QApplication.restoreOverrideCursor()
            if not authOk:
                askForCredentials = adaptiveUtils.authenticateUser(self)
            else:
                askForCredentials = False
        if not operationOk:
            if not len(resp):
                resp = QCoreApplication.translate('AdaptivePlugin', u"Authentication failed")
            QMessageBox.critical(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u"Adaptive: Error"), resp)
            return
        if not len(resp):
            QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u"Adaptive: Error"), QCoreApplication.translate('AdaptivePlugin', u"No projects published."))
            return
        dialog = ProjectsDialog(self.iface, resp)
        dialog.exec_()

    def runPublish(self):
        proj = QgsProject.instance()
        filePath = proj.fileName()

        (operationOk, result) = validateProject(self.iface, filePath)
        if not operationOk:
            QMessageBox.critical(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u'Error!'), result)
            return

        result = ""
        authOk = False
        operationOk = False
        askForCredentials = True
        while not authOk and askForCredentials:
            if adaptive_data.token:
                dlg = NewProjectDialog(self.iface.mainWindow())
                dlg.exec_()
                if dlg.result():
                    fileName = dlg.lineProjectName.text()
                    QApplication.setOverrideCursor(Qt.WaitCursor)
                    (authOk,operationOk,result) = uploadProjectFile(self.iface, filePath, fileName)
                    QApplication.restoreOverrideCursor()
                else:
                    operationOk = True
                    break
            if not authOk:
                askForCredentials = adaptiveUtils.authenticateUser(self)
            else:
                askForCredentials = False

        if not operationOk:
            QMessageBox.critical(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u'Error!'), result)
            return

        QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u'Adaptive'), QCoreApplication.translate('AdaptivePlugin', u'Project has been published in Adaptive. You can now create a new Theme based on QGIS Project <b>%s</b>.') % result)

    def runUpdate(self):
        proj = QgsProject.instance()
        filePath = proj.fileName()

        (operationOk, result) = validateProject(self.iface, filePath)
        if not operationOk:
            QMessageBox.critical(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u'Error!'), result)
            return

        result = ""
        authOk = False
        operationOk = False
        askForCredentials = True
        while not authOk and askForCredentials:
            if adaptive_data.token:
                # Load current projects
                authOk,operationOk,result = listProjectFiles()
                dlg = UpdateProjectDialog(self.iface.mainWindow(), result)
                dlg.exec_()
                if dlg.result():
                    QApplication.setOverrideCursor(Qt.WaitCursor)
                    (authOk,operationOk,result) = uploadProjectFile(self.iface, filePath, dlg.project['name'], dlg.project['uuid'])
                    QApplication.restoreOverrideCursor()
            if not authOk:
                askForCredentials = adaptiveUtils.authenticateUser(self)
            else:
                askForCredentials = False
        if not operationOk:
            QMessageBox.critical(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u'Error!'), result)
            return

        QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u'Adaptive'), QCoreApplication.translate('AdaptivePlugin', u'Project <b>%s</b> has been updated.') % result)

    def runSettings(self):
        dialog = SettingDialog(self.iface)
        dialog.exec_()