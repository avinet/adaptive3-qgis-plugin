# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from qgis.core import *

token = "" # global variable for authentication token
token_username = "" # global variable for authentication data
token_password = "" # global variable for authentication data

db = QSqlDatabase.addDatabase("QPSQL")

def ustawienia(kontekst, domyslnie=None, format=unicode):
    if not domyslnie:
      domyslnie = ''
    settings = QSettings()
    if format == int:
        return settings.value('/GeoPanelAdmin/'+ kontekst, domyslnie, type=int)
    elif format == bool:
        return settings.value('/GeoPanelAdmin/'+ kontekst, domyslnie, type=unicode).upper() in ['TRUE', 'TAK']
    else:
        return settings.value('/GeoPanelAdmin/'+ kontekst, domyslnie, type=unicode)



def ustawUstawienia(kontekst, wartosc):
    settings = QSettings()
    return settings.setValue('/GeoPanelAdmin/'+ kontekst, wartosc)