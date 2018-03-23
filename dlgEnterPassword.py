# -*- coding: utf-8 -*-
from PyQt4.QtGui import QDialog
from dlgEnterPasswordBase import Ui_EnterPasswordDialogBase
from qgis.core import QgsNetworkAccessManager
from PyQt4.QtCore import SIGNAL, QSettings, QUrl
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
import json
import hashlib
import adaptive_data
import adaptiveUtils
from functools import partial

class EnterPasswordDialog(QDialog, Ui_EnterPasswordDialogBase):
  def __init__(self, iface):
    QDialog.__init__(self)
    self.iface = iface
    self.setupUi(self)
    self.mgr = QgsNetworkAccessManager.instance()
    
  def accept(self):
    username = self.lineUser.text()
    password = self.linePass.text()

    params = { 
      "email": username,
      "pass": hashlib.sha512(password).hexdigest()
      }
      
    url = QUrl('{}/WebServices/generic/Authentication.asmx/Authenticate'.format(adaptive_data.getHost()))
    request = QNetworkRequest(url)
    request.setRawHeader('Content-Type', 'application/json')
    reply = self.mgr.post(request, json.dumps(params))
    reply.connect(reply, SIGNAL("finished()"), partial(self.callback, reply))

  @adaptiveUtils.validateServiceOutput("authenticate")
  def callback(self, response):
    for d in response["data"]:
        if d["key"] == "gm_session_id":
            adaptive_data.token = str(d["value"])
            self.done(1)
        else:
            self.done(0)