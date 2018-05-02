# -*- coding: utf-8 -*-
#from PyQt4.QtCore import *
from PyQt4.QtGui import QDialog, QTreeWidgetItem, QMessageBox, QApplication
from qgis.core import QgsNetworkAccessManager, QgsProject, QCoreApplication
from PyQt4.QtCore import SIGNAL, QSettings, QUrl, QFile, QDir, QIODevice, QFileInfo
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
import json
from functools import partial
from dlgProjectsBase import Ui_ProjectsDialog
import adaptive_data
import adaptiveUtils
import time
import utils

class ProjectsDialog(QDialog, Ui_ProjectsDialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.projects = []
        self.buttonLoad.setEnabled(False)
        self.buttonRemove.setEnabled(False)
        self.buttonRemove.released.connect(self.deleteProject)
        self.buttonLoad.released.connect(self.loadProject)
        self.treeProjects.itemSelectionChanged.connect(self.selectionChanged)
        self.mgr = QgsNetworkAccessManager.instance()
        self.listProjectFiles()

    def listProjectFiles(self):
        ''' Lists project files in the Adaptive service
            params:
            returns: bool AuthenticationOk, bool OperationOk, list of dicts: projects information (if ok) or error message (if not ok)
        '''
        
        url = QUrl('{}/WebServices/administrator/modules/qgis/QgisProject.asmx/ReadExternal'.format(adaptive_data.getHost()))
        params = {}
        request = QNetworkRequest(url)
        request.setRawHeader('Content-Type', 'application/json')

        request.setRawHeader('gm_session_id', adaptive_data.token)
        request.setRawHeader('gm_lang_code', 'nb')
            
        reply = self.mgr.post(request, json.dumps(params))
        reply.connect(reply, SIGNAL("finished()"),  partial(self.fillTree, reply))

    @adaptiveUtils.validateServiceOutput("loading")
    def fillTree(self, response):
        self.treeProjects.clear()
        for project in response["records"]:
                item = QTreeWidgetItem(self.treeProjects)
                item.object = project
                item.setText(0, project['name'])
                item.setText(1, project['filename'])

    def selectionChanged(self):
        is_selection = bool(self.treeProjects.selectedItems())
        self.buttonRemove.setEnabled( is_selection )
        self.buttonLoad.setEnabled( is_selection )

    def deleteProject(self):
        if not bool(self.treeProjects.selectedItems()):
            return

        fileUuid = self.treeProjects.selectedItems()[0].object["uuid"]
        url = QUrl('{}/WebServices/administrator/modules/qgis/QgisProject.asmx/Destroy'.format(adaptive_data.getHost()))
        params = {
            "uuids": [fileUuid], "extraParams": []
        }
        request = QNetworkRequest(url)
        request.setRawHeader('Content-Type', 'application/json')

        request.setRawHeader('gm_session_id', adaptive_data.token)
        request.setRawHeader('gm_lang_code', 'nb')

        reply = self.mgr.post(request, json.dumps(params))
        reply.connect(reply, SIGNAL("finished()"), partial(self.delete_project_callback, reply))

    @adaptiveUtils.validateServiceOutput("loading")
    def delete_project_callback(self, response):
        self.listProjectFiles()

    def loadProject(self):
        proj = QgsProject.instance()
        filePath = proj.fileName()
        (operationOk, result) = utils.validateBeforeLoad(self.iface)
        if not operationOk:
            return
        if not bool(self.treeProjects.selectedItems()):
            QMessageBox.information(self.iface.mainWindow(), 'Information', 'No project selected')
            return
        fileName = self.treeProjects.selectedItems()[0].object["filename"]
        fileUuid = self.treeProjects.selectedItems()[0].object["uuid"]

        url = QUrl("{}/WebServices/administrator/modules/qgis/Downloader.ashx?gm_session_id={}&uuid={}".format(adaptive_data.getHost(), adaptive_data.token, fileUuid))
        request = QNetworkRequest(url)
        reply = self.mgr.get(request)
        reply.connect(reply, SIGNAL("finished()"),  partial(self.load_project_callback, reply, fileName))
    
    def load_project_callback(self, response, filename):
        error = response.error()

        if error != 0:
            QMessageBox.critical(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u'Error!'), 'Could not load project')

        proj = QgsProject.instance()
        proj.clear()

        response = str(response.readAll())
        tempFolder = int(time.time())
        fileDir = QDir()
        fileDir.mkpath('{}/{}'.format(QDir.tempPath(), tempFolder))
        projectFile = QFile("{}/{}/{}".format(QDir.tempPath(), tempFolder, filename))
        projectFile.open(QIODevice.ReadWrite | QIODevice.Truncate)
        projectFile.write(response)
        projectFile.close()

        time.sleep(1)

        proj.setFileName(projectFile.fileName())
        proj.read()

        cachingEnabled = self.iface.mapCanvas().isCachingEnabled()
        for layer in self.iface.mapCanvas().layers():
            if cachingEnabled:
                layer.setCacheImage(None)
            layer.triggerRepaint()

        self.iface.mapCanvas().refresh()
        QApplication.restoreOverrideCursor()
        self.close()