# -*- coding: utf-8 -*-

def classFactory(iface):
  from mainPlugin import AdaptivePlugin
  return AdaptivePlugin(iface)
