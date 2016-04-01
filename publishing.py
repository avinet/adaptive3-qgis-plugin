# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from PyQt4.QtCore import QSettings
import adaptive_data

import json
import urllib2, cookielib
from multipartposthandler import MultipartPostHandler

import hashlib
import sys, traceback

settings = QSettings()

if not settings.contains('a3_url'):
    settings.setValue('a3_url', '')

# Configuration: adaptive 3 url
host = settings.value('a3_url', type=str)


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

    params = { "email": username,
               "pass": hashlib.sha512(password).hexdigest() }

    req = urllib2.Request('{}/WebServices/generic/Authentication.asmx/Authenticate'.format(host))
    req.add_header('Content-Type', 'application/json')

    try:
        f = urllib2.urlopen(req, json.dumps(params))
        result = json.loads(f.read())
        result = result["d"]

        if not result["success"]:
            return ""

        for d in result["data"]:
            if d["key"] == "gm_session_id":
                return str(d["value"])
            else:
                return ""
    except:
        return ""


def uploadProjectFile(iface, filePath, projectName, uuid = None):
    ''' Uploads project file to the Adaptive service
        params: QgsInterface QGIS interface instance, unicode project file path
        returns: bool AuthenticationOk, bool OperationOk, unicode file path (if ok) or error message (if not ok)
    '''

    success, result = uploadFile(filePath)

    if success:

        fileName = result["fileNames"][0]

        if uuid:
            return updateQgisProject(uuid, fileName, projectName)
        else:
            return createQgisProject(result["originalFileNames"][0], fileName, projectName)
    else:
        return ( False, False, QCoreApplication.translate('publishing', u'Error while writing data to Adaptive!') )

def createQgisProject(name, filename, projectName):

    params = {
            "name":projectName,
            "filename":name,
            "projectfile":filename
    }

    req = urllib2.Request('{}/WebServices/administrator/modules/qgis/QgisProject.asmx/ExternalCreate'.format(host))
    req.add_header('Content-Type', 'application/json')
    req.add_header('gm_session_id', adaptive_data.token)
    req.add_header('gm_lang_code', 'nb')

    try:
        f = urllib2.urlopen(req, json.dumps(params))
        result = json.loads(f.read())
        result = result["d"]

        if not result["success"]:
            return ( True, False, formatExceptions(result))

        return (True, True, '%s' % (projectName))



    except urllib2.HTTPError, e:
        if e.code == 401:
            return ( False, False, None )
        else:
            result = json.loads(e.read())
            return ( True, False, unicode(result['Message']) )
    except:
        return ( False, False, None )

def updateQgisProject(uuid, projectfile, projectName):
    params = {
            "uuid":uuid,
            "projectfile":projectfile
    }

    req = urllib2.Request('{}/WebServices/administrator/modules/qgis/QgisProject.asmx/UpdateExternal'.format(host))
    req.add_header('Content-Type', 'application/json')
    req.add_header('gm_session_id', adaptive_data.token)
    req.add_header('gm_lang_code', 'nb')

    try:
        f = urllib2.urlopen(req, json.dumps(params))
        result = json.loads(f.read())
        result = result["d"]

        if not result["success"]:
            return ( True, False, formatExceptions(result))

        return ( True,True,'%s' % (projectName) )

    except:
        return ( True, False, None)


def listProjectFiles():
    ''' Lists project files in the Adaptive service
        params:
        returns: bool AuthenticationOk, bool OperationOk, list of dicts: projects information (if ok) or error message (if not ok)
    '''

    req = urllib2.Request('{}/WebServices/administrator/modules/qgis/QgisProject.asmx/ReadExternal'.format(host))
    req.add_header('Content-Type', 'application/json')
    req.add_header('gm_lang_code', 'nb')
    req.add_header('gm_session_id', adaptive_data.token)

    try:
        f = urllib2.urlopen(req, json.dumps({}))
        result = json.loads(f.read())
        result = result["d"]
        if not result["success"]:
            return ( False, False, QCoreApplication.translate('publishing', u'Error while reading data from Adaptive!') )

        return (True, True, result["records"])

    except:
        return ( False, False, QCoreApplication.translate('publishing', u'Error while reading data from Adaptive!') )


def deleteProjectFile(fileUuid):
    ''' Deletes a project file from the Adaptive service
        params: unicode project file name
        returns: bool AuthenticationOk, bool OperationOk, unicode error message
    '''

    params = {
        "uuids":[fileUuid],"extraParams":[]}

    req = urllib2.Request('{}/WebServices/administrator/modules/qgis/QgisProject.asmx/Destroy'.format(host))
    req.add_header('Content-Type', 'application/json')
    req.add_header('gm_lang_code', 'nb')
    req.add_header('gm_session_id', adaptive_data.token)

    try:
         f = urllib2.urlopen(req, json.dumps(params))
         result = json.loads(f.read())
         result = result["d"]

         if not result["success"]:
             return ( True, False, formatExceptions(result) )

         return ( True, True, None )
    except urllib2.HTTPError, e:
        if e.code == 401:
            return ( False, False, None )
        else:
            result = json.loads(e.read())
            return ( True, False, unicode(result['Message']) )
    except:
        return ( False, False, None )

def readProjectFile(fileUuid):
    ''' Reads a project file from the Adaptive service
        params: unicode project file name
        returns: bool AuthenticationOk, bool OperationOk, unicode file content (if ok) or error message (if not ok)
    '''

    try:
        f = urllib2.urlopen("{}/WebServices/administrator/modules/qgis/Downloader.ashx?gm_session_id={}&uuid={}".format(host, adaptive_data.token, fileUuid))
        return (True, True, f.read())
    except urllib2.HTTPError, e:
        if e.code == 401:
            return ( False, False, None )
        else:
            return ( True, False, "Error" )
    except:
        return ( False, False, QCoreApplication.translate('publishing', u'Error while reading data from Adaptive!') )

def uploadFile(filePath):
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

    request = urllib2.Request("{}/WebServices/administrator/modules/qgis/Uploader.ashx".format(host), params)
    request.add_header('gm_session_id', adaptive_data.token)

    try:
        f = opener.open(request)
        result = json.loads(f.read())

        if result["success"] == True:
           return True, result
        else:
            return False, None

    except urllib2.HTTPError, e:
        return False, None

def formatExceptions(result):

    if not result['exceptions']:
        return None

    exceptions = result['exceptions']

    if hasattr(exceptions, '__len__') and (not isinstance(exceptions, str)):
        if len(exceptions) > 0:
            return exceptions[0]['msg']