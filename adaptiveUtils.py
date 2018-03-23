# -*- coding: utf-8 -*-
from PyQt4.QtCore import QCoreApplication, QUrl, SIGNAL
from qgis.core import QgsNetworkAccessManager
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt4.QtGui import QMessageBox
from functools import partial
import adaptive_data
import json

def fixResponse(response):
    response = str(response.readAll())
    if response:
        response = json.loads(response)

    if 'd' in response:
        response = response['d']

    return response

def validateServiceOutput(operation):
    def validateServiceOutputWrapper(func):
        def func_wrapper(self, response):
            error = response.error()
            if error != 0:
                QMessageBox.critical(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u'Error!'), "Fix me: Server error")
                return
            response = fixResponse(response)
            if(response['success'] != True):
                errorMsg = 'Error'
                if 'exception' in response:
                    errorMsg = response['exception']['msg']
                QMessageBox.critical(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u'Error!'), errorMsg)
            else:
                func(self, response)
        return func_wrapper
    return validateServiceOutputWrapper

def validateUploadServiceOutput(func):
    def func_wrapper(self, response):
        if not len(response["originalFileNames"]) == 1 and len(response["fileNames"]) == 1:
            QMessageBox.critical(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u'Error!'), "Fix me: Upload error")
        else:
            func(self, response)
    return func_wrapper

def verifySession(cb):
    mgr = QgsNetworkAccessManager.instance()
    url = QUrl('{}/WebServices/generic/Authentication.asmx/VerifySession'.format(adaptive_data.getHost()))
    request = QNetworkRequest(url)
    request.setRawHeader('Content-Type', 'application/json')
    request.setRawHeader('gm_session_id', adaptive_data.token)
    request.setRawHeader('gm_lang_code', 'nb')
    reply = mgr.post(request, json.dumps({}))
    reply.connect(reply, SIGNAL("finished()"), partial(validateTokenCallback, reply, cb))


def validateTokenCallback(reply, cb):
    try:
        response = fixResponse(reply)
        cb(response['success'] == True)
    except:
        cb(False)