# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Georondonia
                                 A QGIS plugin
 Georondonia
 Generated by Plugin Builder: -------------------
                              -------------------
        begin                : 2024-11-13
        copyright            : (C) 2024 by Georondonia
        email                : lab.georondonia@ifro.edu.br
 ***************************************************************************/
"""

__author__ = 'Maik Rodrigues'
__date__ = '2024-11-13'
__copyright__ = '(C) 2024 by Maik Rodrigues'

def classFactory(iface):
    from .GeoRondonia import GeorondoniaPlugin
    return GeorondoniaPlugin()
