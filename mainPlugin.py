# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import adaptive_data
from adaptive_data import *
from resources_rc import *

from dlgEnterPassword import EnterPasswordDialog
from dlgProjects import ProjectsDialog

from publishing import host, authenticate, validateProject, uploadProjectFile, listProjectFiles



class AdaptivePlugin():
    # ----------------------------------------- #
    def __init__(self, iface):
        self.iface = iface



    def initGui(self):

        self.action6 = QAction(QIcon(), u'Projects', self.iface.mainWindow())
        self.action7 = QAction(QIcon(), u'Publish project', self.iface.mainWindow())

        self.action6.setToolTip(u'Adaptive: Browse QGIS project on server')
        self.action7.setToolTip(u'Adaptive: Publish QGIS project to server')

        self.action6.triggered.connect(self.runProjects)
        self.action7.triggered.connect(self.runPublikuj)

        self.toolBar = self.iface.addToolBar("Adaptive")
        self.toolBar.setObjectName('Adaptive')

        self.menu = QMenu()
        self.menu.setTitle("Adaptive")
        menuBar = self.iface.mainWindow().menuBar()
        lastAction = menuBar.actions()[len(menuBar.actions()) - 1]
        menuBar.insertMenu(lastAction, self.menu)

        for i in [self.action6, self.action7]:
            #self.iface.addPluginToMenu('Adaptive', i)
            self.menu.addAction(i)
            self.toolBar.addAction(i)



    def unload(self):
        for i in [self.action6, self.action7]:
            self.iface.removePluginMenu('Adaptive', i)
            self.toolBar.removeAction(i)
        del self.toolBar



    def runProjects(self):
        resp = ""
        ok = False
        pytaj = True
        while not ok and pytaj:
            if adaptive_data.token:
                QApplication.setOverrideCursor(Qt.WaitCursor)
                ok,resp = listProjectFiles()
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
            QMessageBox.critical(self.iface.mainWindow(), u"Adaptive: Error", u"Unable to read project list")
            return
        if not len(resp):
            QMessageBox.information(self.iface.mainWindow(), u"Adaptive: Error", u"No projects published.")
            return
        dialog = ProjectsDialog(self.iface, resp)
        dialog.exec_()



    def runPublikuj(self):
        proj = QgsProject.instance()
        filePath = proj.fileName()
        fileName = QFileInfo(filePath).fileName()

        (ok, result) = validateProject(self.iface, filePath)
        if not ok:
            QMessageBox.critical(self.iface.mainWindow(), u'Błąd!', result)
            return

        wmsUrl = 'http://%s/%s/%s' % (host, serviceName, fileName)

        result = ""
        ok = False
        pytaj = True
        while not ok and pytaj:
            if adaptive_data.token:
                QApplication.setOverrideCursor(Qt.WaitCursor)
                (ok,result) = uploadProjectFile(self.iface, filePath)
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
            QMessageBox.critical(self.iface.mainWindow(), u'Error!', result)
            return

        QMessageBox.information(self.iface.mainWindow(), u'Adaptive', u'Project has been published in Adaptive. You can now create a new Theme based on QGIS Project <b>%s</b>.' % result)
