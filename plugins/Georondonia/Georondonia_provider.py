# -*- coding: utf-8 -*-
__author__ = 'Maik Rodrigues'
__date__ = '2024-11-13'
__copyright__ = '(C) 2024 by Maik Rodrigues'
__revision__ = '$Format:%H$'

from qgis.core import QgsProcessingProvider
from .algoritmos.Divide_Lote_Buffer import divideLoteBufferAlgorithm
from .algoritmos.Angulos_Internos import AngulosInternosAlgorithm
from .algoritmos.Plano_de_Voo import PlanoVooAlgorithm
from .algoritmos.geradordeods import geradordeods
from .algoritmos.ajuste_poligono import AjustePoligonos
from qgis.PyQt.QtGui import QIcon
import os

class GeorondoniaProvider(QgsProcessingProvider):
    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        pass

    def loadAlgorithms(self):
        #self.addAlgorithm(divideLoteBufferAlgorithm())
        #self.addAlgorithm(AngulosInternosAlgorithm())
        #self.addAlgorithm(PlanoVooAlgorithm())
        #self.addAlgorithm(AjustePoligonos())
        self.addAlgorithm(geradordeods())

    def id(self):
        return 'GeoRondônia'

    def name(self):
        return self.tr('GeoRondônia')

    def icon(self):
        return QIcon(os.path.dirname(__file__) + '/images/georo_icone.png')

    def longName(self):
        return self.name()


