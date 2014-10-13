# -*- coding: utf-8 -*-

def classFactory(iface):
  from adaptive_plugin import AdaptivePlugin
  return AdaptivePlugin(iface)
