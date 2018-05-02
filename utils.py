# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from PyQt4.QtCore import SIGNAL, QSettings, QUrl
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest, QHttpMultiPart, QHttpPart
import adaptive_data
import json
import urllib2, cookielib
import hashlib
import sys, traceback

def construct_multipart(files, data = {}):
    multiPart = QHttpMultiPart(QHttpMultiPart.FormDataType)
    for key, value in data.items():
        textPart = QHttpPart()
        textPart.setHeader(
            QNetworkRequest.ContentDispositionHeader,
            "form-data; name=\"%s\"" % key
            )
        textPart.setBody(value)
        multiPart.append(textPart)

    for key, file in files.items():
        imagePart = QHttpPart()
        fileName = QFileInfo(file.fileName()).fileName()
        imagePart.setHeader(
            QNetworkRequest.ContentDispositionHeader,
            "form-data; name=\"%s\"; filename=\"%s\"" % (key, fileName)
            )
        imagePart.setBodyDevice(file)
        file.setParent(multiPart)
        multiPart.append(imagePart)
    return multiPart

def validateProject(iface, filePath):
    ''' Validates if the project file meets Adaptive's requirements
        params: QgsInterface QGIS interface instance, unicode project file path
        returns: bool projectOk, unicode error message
    '''

    if not len(iface.mapCanvas().layers()):
        return ( False, QCoreApplication.translate('publishing', u'There are no layers in this project.') )

    for layer in iface.mapCanvas().layers():
        p = layer.dataProvider()
        if not p or not p.name() in ( 'postgres', 'gdal', 'wms' ):
            return ( False, QCoreApplication.translate('publishing', u'Project can not be published because it has layers based on unsupported sources:') + ' ' + layer.name())

    proj = QgsProject.instance()
    if proj.isDirty() or not filePath:
        return ( False, QCoreApplication.translate('publishing', u'You have unsaved changes. Please save before publishing.') )

    return ( True, None )

def validateBeforeLoad(iface):
    proj = QgsProject.instance()
    if proj.isDirty():
        reply = QMessageBox.question(
            iface.mainWindow(),
            'Unsaved changes',
            QCoreApplication.translate('publishing', u'Your current project contains unsaved changes. Press OK to continue without saving'),
            QMessageBox.Ok, QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            proj.clear()
            return ( True, None )
        else:
            return ( False, None )
    return ( True, None )
