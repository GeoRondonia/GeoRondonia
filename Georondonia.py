# -*- coding: utf-8 -*-
__author__ = 'Maik Rodrigues de Souza'
__date__ = '2024-11-13'
__copyright__ = '(C) 2024 by Maik Rodrigues de Souza'
__revision__ = '$Format:%H$'

import os
import sys
import inspect
from qgis.core import QgsApplication
from .GeoRondonia_provider import GeorondoniaProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

class GeorondoniaPlugin(object):
    def __init__(self):
        self.provider = None

    def initProcessing(self):
        self.provider = GeorondoniaProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self): # Código para inicializar a interface gráfica do plugin
        self.initProcessing()

    def unload(self):  # Código para limpar/descarregar o plugin
        QgsApplication.processingRegistry().removeProvider(self.provider) 
