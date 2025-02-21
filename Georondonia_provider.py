# -*- coding: utf-8 -*-
__author__ = 'Maik Rodrigues de Souza'
__date__ = '2024-11-13'
__copyright__ = '(C) 2024 by Maik Rodrigues de Souza'
__revision__ = '$Format:%H$'

from qgis.core import QgsProcessingProvider
from .algoritmos.georural_Geradordeods import geradordeods
from .algoritmos.tool_CheckInvalidGeometry import CheckInvalidGeometry
from qgis.PyQt.QtGui import QIcon
import os

class GeorondoniaProvider(QgsProcessingProvider):
    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        pass

    def loadAlgorithms(self):
        self.addAlgorithm(geradordeods())
        self.addAlgorithm(CheckInvalidGeometry())
        

    def id(self):
        return 'GeoRondônia'

    def name(self):
        return self.tr('GeoRondônia')

    def icon(self):
        return QIcon(os.path.dirname(__file__) + '/images/georo_icone.png')

    def longName(self):
        return self.name()


