# -*- coding: utf-8 -*-
#from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from PyQt4.QtCore import SIGNAL, QSettings, QUrl, QFile, QDir, QIODevice, QFileInfo
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
import json
from functools import partial
from dlgProjectsBase import Ui_ProjectsDialog
import adaptive_data
import adaptiveUtils
import time

host = "http://localhost/a_a3/"
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
        
        url = QUrl('{}/WebServices/administrator/modules/qgis/QgisProject.asmx/ReadExternal'.format(host))
        params = {}
        request = QNetworkRequest(url)
        request.setRawHeader('Content-Type', 'application/json')

        request.setRawHeader('gm_session_id', adaptive_data.token)
        request.setRawHeader('gm_lang_code', 'nb')
            
        reply = self.mgr.post(request, json.dumps(params))
        reply.connect(reply, SIGNAL("finished()"),  partial(self.fillTree, reply))

    def fillTree(self, response):
        error = response.error()

        if error != 0:
            return "An error occured"

        response = adaptiveUtils.fixResponse(response)

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
        url = QUrl('{}/WebServices/administrator/modules/qgis/QgisProject.asmx/Destroy'.format(host))
        params = {
            "uuids": [fileUuid], "extraParams": []
        }
        request = QNetworkRequest(url)
        request.setRawHeader('Content-Type', 'application/json')

        request.setRawHeader('gm_session_id', adaptive_data.token)
        request.setRawHeader('gm_lang_code', 'nb')

        reply = self.mgr.post(request, json.dumps(params))
        reply.connect(reply, SIGNAL("finished()"), partial(self.delete_project_callback, reply))

    def delete_project_callback(self, response):
        error = response.error()

        if error != 0:
            return "delete_project_callback - error != 0"

        response = adaptiveUtils.fixResponse(response)

        if not response["success"]:
            print "delete_project_callback - success false"

        self.listProjectFiles()

    def loadProject(self):
        proj = QgsProject.instance()
        filePath = proj.fileName()
        (operationOk, result) = utils.validateProject(self.iface, filePath)
        if not operationOk:
            QMessageBox.critical(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u'Error!'), result)
            return
        if not bool(self.treeProjects.selectedItems()):
            return
        fileName = self.treeProjects.selectedItems()[0].object["filename"]
        fileUuid = self.treeProjects.selectedItems()[0].object["uuid"]

        url = QUrl("{}/WebServices/administrator/modules/qgis/Downloader.ashx?gm_session_id={}&uuid={}".format(host, adaptive_data.token, fileUuid))

        request = QNetworkRequest(url)
        reply = self.mgr.get(request)
        reply.connect(reply, SIGNAL("finished()"),  partial(self.load_project_callback, reply, fileName))
    
    def load_project_callback(self, response, filename):
        error = response.error()

        if error != 0:
            print "An error occured"
            return "An error occured"

        response = str(response.readAll())
        QFile.remove(QDir.tempPath()+'/' + filename)
        tempFolder = int(time.time())
        dir = QDir()
        dir.mkpath('{}/{}'.format(QDir.tempPath(), tempFolder))
        projectFile = QFile("{}/{}/{}".format(QDir.tempPath(), tempFolder, filename))
        projectFile.open(QIODevice.ReadWrite | QIODevice.Truncate)
        projectFile.write(response)
        projectFile.flush()
        projectFile.close()
        proj = QgsProject.instance()
        proj.clear()
        proj.read(QFileInfo(projectFile.fileName()))
        QApplication.restoreOverrideCursor()
        self.close()