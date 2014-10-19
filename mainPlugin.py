# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import adaptive_data
from adaptive_data import *     #db,ustawienia, tabele...
from resources_rc import *

from dlgEnterPassword import EnterPasswordDialog
from dlgProjects import ProjectsDialog
from dlgSettings import SettingsDialog

from publishing import host, authenticate, walidujProjekt, uploadProjectFile, listProjectFiles



class AdaptivePlugin():
    # ----------------------------------------- #
    def __init__(self, iface):
        self.iface = iface



    def initGui(self):

        self.action6 = QAction(QIcon(), u'Projects', self.iface.mainWindow())
        self.action7 = QAction(QIcon(), u'Publish project', self.iface.mainWindow())
        self.action8 = QAction(QIcon(), u'Settings', self.iface.mainWindow())

        self.action6.setToolTip(u'Adaptive: Browse QGIS project on server')
        self.action7.setToolTip(u'Adaptive: Publish QGIS project to server')
        self.action8.setToolTip(u'Adaptive: Settings')

        self.action6.triggered.connect(self.runProjects)
        self.action7.triggered.connect(self.runPublikuj)
        self.action8.triggered.connect(self.runSettings)

        self.toolBar = self.iface.addToolBar("Adaptive")
        self.toolBar.setObjectName('Adaptive')

        self.menu = QMenu()
        self.menu.setTitle("Adaptive")
        menuBar = self.iface.mainWindow().menuBar()
        lastAction = menuBar.actions()[len(menuBar.actions()) - 1]
        menuBar.insertMenu(lastAction, self.menu)

        for i in [self.action6, self.action7, self.action8]:
            #self.iface.addPluginToMenu('Adaptive', i)
            self.menu.addAction(i)
            self.toolBar.addAction(i)



    def connect(self, host, dbname, user, password, port):
        db.setHostName(host)
        db.setDatabaseName(dbname)
        db.setUserName(user)
        db.setPassword(password)
        if port: db.setPort(port)
        ok = db.open()
        if ok:
            return None
        else:
            return db.lastError().text()



    def initDatabase(self):
        settings = QSettings()
        selected = settings('bazaDanych')
        if not selected:
            QMessageBox.critical(self.iface.mainWindow(), u"Adaptive", u"No database connection defined. Please set one using Settings option.")
            return 1
        settings.beginGroup( u"/PostgreSQL/connections/" + selected )
        if not settings.contains("database"): # non-existent entry?
            QMessageBox.critical(self.iface.mainWindow(), u"Adaptive", u"Unable to connect to database: %s \n No connection parameters." % selected)
            return 1
        getValueAsQStr = lambda x: settings.value(x)
        host, dbname, username, password = map(getValueAsQStr, ["host", "database", "username", "password"])
        port = settings.value("port", type=int)
        # qgis1.5 use 'savePassword' instead of 'save' setting
        if settings.value("save", "f", type=unicode).upper()=='TRUE' or ( settings.value("savePassword", "f", type=unicode).upper()=='TRUE' and settings.value("saveUsername", "f", type=unicode).upper()=='TRUE' ):
            result = self.connect(host, dbname, username, password, port)
        else:
            result = None
            pytaj = True
            while pytaj:
                dlg = EnterPasswordDialog(self.iface.mainWindow())
                dlg.lineUser.setText(username)
                dlg.linePass.setText(password)
                if username: dlg.linePass.setFocus()
                if result: # pochodzi z poprzednich petli
                    dlg.labelError.setText(result)
                else:
                    dlg.labelError.hide()
                dlg.exec_()
                if dlg.result():
                    username = dlg.lineUser.text()
                    password = dlg.linePass.text()
                    result = self.connect(host, dbname, username, password, port)
                    if not result:
                        # sukces
                        pytaj = False
                else:
                    #zaniechano
                    pytaj = False
                    result = u"Cancelled by user"

        settings.endGroup()
        if result:
            if result.startswith("Driver not loaded"):
                result = u'No PostgreSQL driver!'
            QMessageBox.critical(self.iface.mainWindow(), u"Adaptive", u"Unable to connect to database:\n\"%s\"." % result)
            return 1
        return 0



    def unload(self):
        for i in [self.action6, self.action7, self.action8]:
            self.iface.removePluginMenu('Adaptive', i)
            self.toolBar.removeAction(i)
        del self.toolBar



    def runSettings(self):
        settings = QSettings()
        selected = settings.value("/PostgreSQL/connections/selected", "", type=unicode)
        if not selected:
            QMessageBox.critical(self.iface.mainWindow(), u"Adaptive", u"No database connections defined.")
        else:
            dialog = SettingsDialog(self.iface)
            dialog.exec_()



    def runProjects(self):
        if not db.isOpen(): self.initDatabase()
        if not db.isOpen(): return

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
        if not db.isOpen(): self.initDatabase()
        if not db.isOpen(): return

        proj = QgsProject.instance()
        filePath = proj.fileName()
        fileName = QFileInfo(filePath).fileName()

        (ok, result) = walidujProjekt(self.iface, filePath)
        if not ok:
            QMessageBox.critical(self.iface.mainWindow(), u'Błąd!', result)
            return

        wmsUrl = 'http://%s/%s/%s' % (host, db.databaseName(), fileName)

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
