# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import QSettings
from dlgSettingBase import Ui_Dialog
import urllib
import urllib2
import json
from urlparse import urlparse

class SettingDialog(QDialog, Ui_Dialog):
  def __init__(self, parent):
    QDialog.__init__(self)
    self.setupUi(self)
    self.buttonBox.accepted.connect(self.saveSettings)
    self.loadSettings()
    
  def saveSettings(self):
    settings = QSettings()
    settings.setValue('a3_url', self.lineEdit.text());
    self.loadSetup()
    
  def loadSettings(self):
    settings = QSettings()
    if not settings.contains('a3_url'):
        settings.setValue('a3_url', '')
    
    servicePath = settings.value('a3_url', type=str)
    self.lineEdit.setText(servicePath)
  
  # Possibly check if site respons?
  def loadSetup(self):
    settings = QSettings()
    a3Path = settings.value('a3_url', type=str)
    
    url = "{0}/WebServices/client/qgis.asmx/GetQGisHost".format(a3Path)
    postdata = {'key':'value'}
    req = urllib2.Request(url)
    req.add_header('Content-Type','application/json')
    data = json.dumps(postdata)
    response = urllib2.urlopen(req,data)
    jsonResponse =  json.load(response)
    plugin_path =  jsonResponse['d']['data'][0]['value']
    
    o = urlparse(plugin_path)
    path = o.path
    if path.endswith("/"):
        path = path[:-1]
    if path.startswith("/"):
        path = path[1:]

    
    
    # Save settings
    settings.setValue('a3_host', o.netloc)
    settings.setValue('a3_selector', path)