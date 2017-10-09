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

host = "http://localhost/a_a3/"

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
      url = QUrl("{}WebServices/administrator/modules/qgis/Uploader.ashx".format(host))
      request = QNetworkRequest(url)
      request.setRawHeader('gm_session_id', adaptive_data.token)
      request.setHeader(
          QNetworkRequest.ContentTypeHeader,
          'multipart/form-data; boundary=%s' % multipart.boundary()
          )
      reply = self.mgr.post(request, multipart)
      multipart.setParent(reply)
      reply.connect(reply, SIGNAL("finished()"), partial(self.upload_project_callback, reply))

  def upload_project_callback(self, response):
      error = response.error()

      if error != 0:
          print "An error occured {}".format(error)
          #self.done(0)

      response = str(response.readAll())
      response = json.loads(response)
      self.create_project(
          response["originalFileNames"][0],
          response["fileNames"][0])
      return True

  def create_project(self, filename, projectfile):
      url = QUrl('{}/WebServices/administrator/modules/qgis/QgisProject.asmx/ExternalCreate'.format(host))
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

  def create_project_callback(self, response):
    error = response.error()

    if error != 0:
        return "delete_project_callback - error != 0"

    response = adaptiveUtils.fixResponse(response)

    if not response["success"]:
        print "create_project_callback - success false"
    else:
        print "create_project_callback - success true"
