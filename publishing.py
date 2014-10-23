# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *

import adaptive_data

import json
import urllib2, cookielib
from multipartposthandler import MultipartPostHandler


# Configuration: PluginService hostname and port number. No trailing slash or protocol scheme.
# Example: 'pluginservice.utvikling.avinet.no'
host = 'localhost'
# Configuration: PluginService relative path, without trailing or leading slash.
# Example (for pluginservice as separate site): 'api/qgis'
selector = 'a_a3_pluginservice/api/qgis'

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


def authenticate(username, password):
    ''' Authenticates the user in the Adaptive service
        params: string username, string password
        returns: string token
    '''

    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler) #zwraca OpenerDirector

    params = { "username": username,
               "password": password }

    try:
        f = opener.open("http://%s/%s/authenticate" % (host,selector), params)
        result = json.loads(f.read())
        return result["Token"]
    except:
        return ""


def uploadProjectFile(iface, filePath):
    ''' Uploads project file to the Adaptive service
        params: QgsInterface QGIS interface instance, unicode project file path
        returns: bool AuthenticationOk, bool OperationOk, unicode file path (if ok) or error message (if not ok)
    '''

    fileName = QFileInfo(filePath).fileName()
    fileName = unicode(fileName) # for compatibility with post_multipart
    filePath = unicode(filePath) # for compatibility with post_multipart
    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler) #returns OpenerDirector instance

    params = { "filename": fileName,
               "file" : open(filePath, "rb") }

    request = urllib2.Request("http://%s/%s" % (host,selector), params)
    request.add_header('X-Adaptive-AuthToken', adaptive_data.token)

    try:
        opener.open(request)
    except urllib2.HTTPError, e:
        if e.code == 401:
            return ( False, False, None )
        else:
            result = json.loads(e.read())
            return ( True, False, unicode(result['Message']) )
    except:
        return ( False, False, QCoreApplication.translate('publishing', u'Error while writing data to Adaptive!') )
    return (True, True, '%s' % (fileName))


def listProjectFiles():
    ''' Lists project files in the Adaptive service
        params:
        returns: bool AuthenticationOk, bool OperationOk, list of dicts: projects information (if ok) or error message (if not ok)
    '''

    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler) #zwraca OpenerDirector
    request = urllib2.Request("http://%s/%s" % (host,selector))
    request.add_header('X-Adaptive-AuthToken', adaptive_data.token)

    try:
        f = opener.open(request)
    except urllib2.HTTPError, e:
        if e.code == 401:
            return ( False, False, None )
        else:
            result = json.loads(e.read())
            return ( True, False, unicode(result['Message']) )
    except:
        return ( False, False, QCoreApplication.translate('publishing', u'Error while reading data from Adaptive!') )

    return (True, True, json.loads(f.read()))


def deleteProjectFile(fileName):
    ''' Deletes a project file from the Adaptive service
        params: unicode project file name
        returns: bool AuthenticationOk, bool OperationOk, unicode error message
    '''

    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request("http://%s/%s/%s" % (host,selector,fileName))
    request.add_header('X-Adaptive-AuthToken', adaptive_data.token)
    request.get_method = lambda: 'DELETE'

    try:
        f = opener.open(request)
    except urllib2.HTTPError, e:
        if e.code == 401:
            return ( False, False, None )
        else:
            result = json.loads(e.read())
            return ( True, False, unicode(result['Message']) )
    except:
        return ( False, False, None )
    return ( True, True, None )


def readProjectFile(fileName):
    ''' Reads a project file from the Adaptive service
        params: unicode project file name
        returns: bool AuthenticationOk, bool OperationOk, unicode file content (if ok) or error message (if not ok)
    '''

    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler) #zwraca OpenerDirector
    request = urllib2.Request("http://%s/%s/%s" % (host,selector,fileName))
    request.add_header('X-Adaptive-AuthToken', adaptive_data.token)

    try:
        f = opener.open(request)
    except urllib2.HTTPError, e:
        if e.code == 401:
            return ( False, False, None )
        else:
            result = json.loads(e.read())
            return ( True, False, unicode(result['Message']) )
    except:
        return ( False, False, QCoreApplication.translate('publishing', u'Error while reading data from Adaptive!') )
    return (True, True, f.read())
