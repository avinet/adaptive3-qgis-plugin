# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *

import adaptive_data
from adaptive_data import db

import json
import urllib2, cookielib
from multipartposthandler import MultipartPostHandler


# adres serwera do downloadu i uploadu projektów. W kolejnych funkcjach zdefinio
host = 'localhost:82'
selector = 'pluginservice/api/qgis'

def connectionStringOk(conn):
    ''' sprawdza,czy conn string nie prowadzi do nieuprawnionej bazy danych
        params: unicode źródło danych warstwy (w wypadku bazy postgres jest to connection string)
        returns: bool wynik (True gdy ok)
    '''
    pairs=conn.split(' ')
    params = {}
    for pair in pairs:
        pair = pair.split('=')
        if len(pair)==2:
            params[pair[0]] = pair[1].replace("'","")
    if not params.has_key('dbname'):
        return False
    if params['dbname'] != db.databaseName():
        return False
    return True


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

    #for layer in iface.mapCanvas().layers():
        #if layer.dataProvider().name() == 'postgres' and layer.crs().authid() != 'EPSG:2180':
            #return ( False, u'Usługa nie może zostać wyeksportowana, ponieważ zawiera warstwę w układzie współrzędnych innym, niż PUWG92: %s' % layer.name())

    for layer in iface.mapCanvas().layers():
        if layer.dataProvider().name() == 'postgres' and not connectionStringOk( layer.source() ):
            return ( False, u'Project cannot be published, because at least one PostGIS layer is in wrong database: %s' % layer.name())

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


def uploadProjectFile(iface, filePath, publiczny):
    ''' Uploaduj plik projektu na serwer
        params: QgsInterface instancja interfejsu QGIS-a, unicode ścieżka do pliku projektu, bool publiczność projektu
        returns: bool wynik (True gdy ok), unicode komunikat błędu
    '''

    fileName = QFileInfo(filePath).fileName()
    fileName = unicode(fileName) # dla zgodnosci z post_multipart
    filePath = unicode(filePath) # dla zgodnosci z post_multipart
    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler) #zwraca OpenerDirector

    params = { "filename": fileName,
               "isPublic": str(publiczny),
               "file" : open(filePath, "rb") }

    try:
        opener.open("http://%s/%s?token=%s" % (host,selector,str(adaptive_data.token)), params)
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
    try:
        f = opener.open("http://%s/%s?token=%s" % (host,selector,adaptive_data.token))
    except:
        return ( False, None )
    return (True, json.loads(f.read()))


def deleteProjectFile(fileName):
    ''' usuń plik projektu z serwera
        params: unicode nazwa pliku projektu
        returns: bool wynik (True gdy ok), unicode komunikat błędu (akurat w tej funkcji zawsze None)
    '''

    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request("http://%s/%s/%s?token=%s" % (host,selector,fileName,adaptive_data.token))
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

    try:
        f = opener.open("http://%s/%s/%s?token=%s" % (host,selector,fileName,adaptive_data.token))
    except:
        return ( False, None )
    return (True, f.read())
