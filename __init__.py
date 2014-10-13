# -*- coding: utf-8 -*-

def classFactory(iface):
  from geopanel_plugin import GeoPanelPlugin
  return GeoPanelPlugin(iface)
