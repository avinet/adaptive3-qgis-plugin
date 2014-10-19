# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from qgis.core import *

token = "" # global variable for authentication token
token_username = "" # global variable for authentication data
token_password = "" # global variable for authentication data

serviceName = "adaptiveServiceName"

def settings(context, default=None, format=unicode):
    if not default:
      default = ''
    settings = QSettings()
    if format == int:
        return settings.value('/AdaptivePlugin/'+ context, default, type=int)
    elif format == bool:
        return settings.value('/AdaptivePlugin/'+ context, default, type=unicode).upper() in ['TRUE', 'TAK']
    else:
        return settings.value('/AdaptivePlugin/'+ context, default, type=unicode)
