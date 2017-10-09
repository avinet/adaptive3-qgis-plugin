# -*- coding: utf-8 -*-
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QMessageBox
import adaptive_data
from dlgEnterPassword import EnterPasswordDialog
import json

def authenticateUser(self, afterAuth):
        dlg = EnterPasswordDialog(self.iface.mainWindow())
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

def authenticate_callback(auth_reply, afterAuth):
    error = auth_reply.error()

    if(error != 0):
        return ""

    response = fixResponse(response)

    if not response["success"]:
        afterAuth()
        return False

    for d in response["data"]:
        if d["key"] == "gm_session_id":
            adaptive_data.token = str(d["value"])
            afterAuth()
            return True
        else:
            return False

def fixResponse(response):
    response = str(response.readAll())
    if response:
        response = json.loads(response)

    if response['d']:
        response = response['d']

    return response
