# -*- coding: utf-8 -*-
from PyQt4.QtCore import QSettings

token = "" # global variable for authentication token
token_username = "" # global variable for authentication data
token_password = "" # global variable for authentication data

def getHost():
    settings = QSettings()
    return settings.value("a3_url")