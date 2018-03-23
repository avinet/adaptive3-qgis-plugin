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
from functools import partial
import utils
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
    
    def _isAuthenticated(func):
        def func_wrapper(self):
            def cb(success):
                if success is True:
                    func(self)
                if success is False:
                    success = self.authenticateUser(partial(func, self))
                if(success is False):
                    func(self, True)

            adaptiveUtils.verifySession(cb)

        return func_wrapper

    @_isAuthenticated
    def runProjects(self, abort = False):
            if abort:
                return
            else:
                QApplication.setOverrideCursor(Qt.WaitCursor)
                QApplication.restoreOverrideCursor()

                dialog = ProjectsDialog(self.iface)
                dialog.exec_()

    @_isAuthenticated
    def runPublish(self, abort = False):
        if abort:
            return
        else:
            proj = QgsProject.instance()
            filePath = proj.fileName()

            (operationOk, result) = utils.validateProject(self.iface, filePath)

            if not operationOk:
                QMessageBox.critical(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u'Error!'), result)
                return

            dlg = NewProjectDialog(self.iface.mainWindow(), filePath)
            dlg.exec_()

    @_isAuthenticated
    def runUpdate(self, abort = False):
        if abort:
            return
        else:
            proj = QgsProject.instance()
            filePath = proj.fileName()

            (operationOk, result) = utils.validateProject(self.iface, filePath)

            if not operationOk:
                QMessageBox.critical(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u'Error!'), result)
                return

            dlg = UpdateProjectDialog(self.iface.mainWindow(), filePath)
            dlg.exec_()

    def runSettings(self):
        dialog = SettingDialog(self.iface)
        dialog.exec_()

    def authenticateUser(self, afterAuth):
        dlg = EnterPasswordDialog(self.iface)
        dlg.label_3.setText(QCoreApplication.translate('AdaptivePlugin', u"Please provide your Adaptive username and password"))
        dlg.labelError.hide()
        dlg.lineUser.setText(adaptive_data.token_username)
        dlg.linePass.setText(adaptive_data.token_password)
        if adaptive_data.token_username: dlg.linePass.setFocus()
        dlg.exec_()
        if dlg.result():
            afterAuth()
            return True
        else:
            QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u"Adaptive information"), QCoreApplication.translate('AdaptivePlugin', u"Authentication is required in order to use Adaptive plugin."))
            return False