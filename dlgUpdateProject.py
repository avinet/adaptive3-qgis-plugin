# -*- coding: utf-8 -*-
from PyQt4.QtGui import QDialog
from dlgUpdateProjectBase import Ui_UpdateProjectDialogBase
from qgis.core import QgsNetworkAccessManager
from PyQt4.QtCore import SIGNAL, QSettings, QUrl, QFile
from PyQt4.QtNetwork import QNetworkRequest
import utils
import json
import hashlib
from functools import partial
import adaptive_data
import adaptiveUtils

class UpdateProjectDialog(QDialog, Ui_UpdateProjectDialogBase):
    def __init__(self, parent, filePath):
        QDialog.__init__(self)
        self.filePath = filePath
        self.mgr = QgsNetworkAccessManager.instance()
        self.setupUi(self)
        self.listProjectFiles()

    def accept(self):
        currentIndex = self.existingProjectsCombo.currentIndex()
        self.existingProject = self.existingProjectsCombo.itemData(currentIndex)
        file1 = QFile(self.filePath)
        file1.open(QFile.ReadOnly)
        files = {'file1': file1}
        self.upload_project(files)

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
        reply.connect(reply, SIGNAL("finished()"), partial(self.fillCombo, reply))

    @adaptiveUtils.validateServiceOutput("loading")
    def fillCombo(self, response):
        for project in response["records"]:
            self.existingProjectsCombo.addItem(project['name'], project)

    def updateProject(self):
        currentIndex = self.existingProjectsCombo.currentIndex()
        self.project = self.existingProjectsCombo.itemData(currentIndex)

    def upload_project(self, files):
        multipart = utils.construct_multipart(files)
        url = QUrl("{}WebServices/administrator/modules/qgis/Uploader.ashx".format(adaptive_data.getHost()))
        request = QNetworkRequest(url)
        request.setRawHeader('gm_session_id', adaptive_data.token)
        request.setHeader(
            QNetworkRequest.ContentTypeHeader,
            'multipart/form-data; boundary=%s' % multipart.boundary()
            )
        reply = self.mgr.post(request, multipart)
        multipart.setParent(reply)
        reply.connect(reply, SIGNAL("finished()"), partial(self.upload_project_callback, reply))

    @adaptiveUtils.validateServiceOutput("uploadProject")
    @adaptiveUtils.validateUploadServiceOutput
    def upload_project_callback(self, response):
        self.update_project(response['fileNames'][0])
        self.done(1)
        return True

    def update_project(self, project_file):
        uuid = self.existingProject["uuid"]
        params = {
            "uuid": uuid,
            "projectfile": project_file
        }

        url = QUrl('{}/WebServices/administrator/modules/qgis/QgisProject.asmx/UpdateExternal'.format(adaptive_data.getHost()))

        request = QNetworkRequest(url)
        request.setRawHeader('Content-Type', 'application/json')

        request.setRawHeader('gm_session_id', adaptive_data.token)
        request.setRawHeader('gm_lang_code', 'nb')

        reply = self.mgr.post(request, json.dumps(params))
        reply.connect(reply, SIGNAL("finished()"), partial(self.update_project_callback, reply))

    @adaptiveUtils.validateServiceOutput("updateProject")
    def update_project_callback(self, response):
        self.done(1)