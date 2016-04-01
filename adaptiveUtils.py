# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import adaptive_data
from dlgEnterPassword import EnterPasswordDialog
from publishing import authenticate

def authenticateUser(self):
        dlg = EnterPasswordDialog(self.iface.mainWindow())
        dlg.label_3.setText(QCoreApplication.translate('AdaptivePlugin', u"Please provide your Adaptive username and password"))
        dlg.labelError.hide()
        dlg.lineUser.setText(adaptive_data.token_username)
        dlg.linePass.setText(adaptive_data.token_password)
        if adaptive_data.token_username: dlg.linePass.setFocus()
        dlg.exec_()
        if dlg.result():
            adaptive_data.token_username = dlg.lineUser.text()
            adaptive_data.token_password = dlg.linePass.text()
            adaptive_data.token = authenticate(adaptive_data.token_username, adaptive_data.token_password)
            return True
        else:
            #user cancelled authentication
            QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('AdaptivePlugin', u"Adaptive information"), QCoreApplication.translate('AdaptivePlugin', u"Authentication is required in order to use Adaptive plugin."))
            return False