# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import SIGNAL, QSettings, QUrl
from PyQt4.QtNetwork import *
from qgis.core import *
from dlgNewProjectBase import Ui_NewProjectDialogBase
import adaptive_data
import adaptiveUtils
import utils
import json
from functools import partial

class NewProjectDialog(QDialog, Ui_NewProjectDialogBase):
  def __init__(self, parent, filePath):
    QDialog.__init__(self)
    self.setupUi(self)
    self.mgr = QgsNetworkAccessManager.instance()
    self.filePath = filePath

  def accept(self):
      self.project_name = self.lineProjectName.text()
      file1 = QFile(self.filePath)
      file1.open(QFile.ReadOnly)
      files = {'file1': file1}
      self.upload_project(files)


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
      self.create_project(
          response["originalFileNames"][0],
          response["fileNames"][0])
      return

  def create_project(self, filename, projectfile):
      url = QUrl('{}/WebServices/administrator/modules/qgis/QgisProject.asmx/ExternalCreate'.format(adaptive_data.getHost()))
      params = {
          "name": self.project_name,
          "filename": filename,
          "projectfile": projectfile
      }
      request = QNetworkRequest(url)
      request.setRawHeader('Content-Type', 'application/json')

      request.setRawHeader('gm_session_id', adaptive_data.token)
      request.setRawHeader('gm_lang_code', 'nb')

      reply = self.mgr.post(request, json.dumps(params))
      reply.connect(reply, SIGNAL("finished()"), partial(self.create_project_callback, reply))

  @adaptiveUtils.validateServiceOutput("createProject")
  def create_project_callback(self, response):
      self.done(1)
