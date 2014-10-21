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
host = 'localhost:8080'
# Configuration: PluginService relative path, without trailing or leading slash.
# Example (for pluginservice as separate site): 'api/qgis'
selector = 'a_a3_pluginservice/api/qgis'

def validateProject(iface, filePath):
    ''' Sprawdza, czy projekt nadaje się do wysłania
        params: QgsInterface instancja interfejsu QGIS-a, unicode ścieżka do pliku projektu
        returns: bool wynik (True gdy ok), unicode komunikat błędu
    '''

    if not len(iface.mapCanvas().layers()):
        return ( False, u'There are no layers in this project.' )

    #if iface.mapCanvas().mapRenderer().destinationCrs().authid() != 'EPSG:2180':
            #return ( False, u'Usługa nie może zostać wyeksportowana, ponieważ jest w innym niż PUWG92 układzie współrzędnych.')

    for layer in iface.mapCanvas().layers():
        #if layer.type() != layer.VectorLayer:
        p = layer.dataProvider()
        if not p or not p.name() in ( 'postgres', 'gdal', 'wms' ):
            return ( False, u'Project can not be published because it has layers based on unsupported sources: %s' % layer.name())

    proj = QgsProject.instance()
    if proj.isDirty() or not filePath:
        return ( False, u'You have unsaved changes. Please save before publishing.' )

    return ( True, None )


def authenticate(username, password):
    ''' Uwierzytelnij w serwisie Adaptive
        params:
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
    ''' Uploaduj plik projektu na serwer
        params: QgsInterface instancja interfejsu QGIS-a, unicode ścieżka do pliku projektu
        returns: bool wynik (True gdy ok), unicode komunikat błędu
    '''

    fileName = QFileInfo(filePath).fileName()
    fileName = unicode(fileName) # dla zgodnosci z post_multipart
    filePath = unicode(filePath) # dla zgodnosci z post_multipart
    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler) #zwraca OpenerDirector

    params = { "filename": fileName,
               "file" : open(filePath, "rb") }

    request = urllib2.Request("http://%s/%s" % (host,selector), params)
    request.add_header('X-Adaptive-AuthToken', adaptive_data.token)

    try:
        opener.open(request)
    except:
        return ( False, u'Error while writing data to Adaptive!' )
    return (True, '%s' % (fileName))


def listProjectFiles():
    ''' Listuj pliki projektów na serwerze
        params:
        returns: bool wynik (True gdy ok), list of dicts: konfiguracja projektów
    '''

    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler) #zwraca OpenerDirector
    request = urllib2.Request("http://%s/%s" % (host,selector))
    request.add_header('X-Adaptive-AuthToken', adaptive_data.token)

    try:
        f = opener.open(request)
    except e:

        return ( False, None )
    return (True, json.loads(f.read()))


def deleteProjectFile(fileName):
    ''' usuń plik projektu z serwera
        params: unicode nazwa pliku projektu
        returns: bool wynik (True gdy ok), unicode komunikat błędu (akurat w tej funkcji zawsze None)
    '''

    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request("http://%s/%s/%s" % (host,selector,fileName))
    request.add_header('X-Adaptive-AuthToken', adaptive_data.token)
    request.get_method = lambda: 'DELETE'

    try:
        opener.open(request)
    except:
        return ( False, None )
    return ( True, None )


def readProjectFile(fileName):
    ''' czytaj plik projektu z serwera
        params: unicode nazwa pliku projektu
        returns: bool wynik (True gdy ok), unicode treść pliku projektu
    '''

    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler) #zwraca OpenerDirector
    request = urllib2.Request("http://%s/%s/%s" % (host,selector,fileName))
    request.add_header('X-Adaptive-AuthToken', adaptive_data.token)

    try:
        f = opener.open(request)
    except:
        return ( False, None )
    return (True, f.read())
