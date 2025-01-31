# -*- coding: utf-8 -*-
__author__ = 'Maik Rodrigues'
__date__ = '2024-11-13'
__copyright__ = '(C) 2024 by Maik Rodrigues'
__revision__ = '$Format:%H$'

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterVectorLayer)
from qgis.PyQt.QtGui import  QIcon
import processing
import os

class divideLoteBufferAlgorithm(QgsProcessingAlgorithm):
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('lotes', 'Lotes', types=[QgsProcessing.TypeVectorPolygon],
                                                            defaultValue='Lotes'))
        self.addParameter(
            QgsProcessingParameterVectorLayer('rio', 'Rio', types=[QgsProcessing.TypeVectorLine],
                                              defaultValue='Rio'))
        self.addParameter(QgsProcessingParameterFeatureSink('lotesD', 'Lotes Divididos'))

    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}
    
        parameters['lotesD'].destinationName = 'Lotes_Divididos'  

        alg_params = { # Buffer
            'DISSOLVE': False,
            'DISTANCE': 1.5,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['rio'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback,
                                            is_child_algorithm=True)
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        alg_params = {
            'INPUT': parameters['lotes'],
            'LINES': outputs['Buffer']['OUTPUT'],
            'OUTPUT': parameters['lotesD']
        }
        outputs['LinhasComQuebra'] = processing.run('native:splitwithlines', alg_params, context=context,
                                                    feedback=feedback, is_child_algorithm=True)
        results['LotesDivididos'] = outputs['LinhasComQuebra']['OUTPUT']
    
        return results

    def name(self):
        return 'Divide Lote(s) Buffer'

    def displayName(self):
        return 'Divide Lote(s) Buffer'

    def group(self):
        return 'Lotes'

    def groupId(self):
        return 'Lotes'

    def tr(self, texto):
        return QCoreApplication.translate('Processing', texto)

    def createInstance(self):
        return divideLoteBufferAlgorithm()
# ----------------------------------------------------------------------------

    def displayName(self):
        return self.tr('Divide Lote(s) Buffer')
    
    def tags(self):
        return self.tr('angle,angulos,medida,abertura,outer,inner,polygon,measure,topography,azimuth,\
                       extract,vertices,extrair,vértices').split(',')
    
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images/geoincra_pb'))
    
    
    
    texto = 'O Divide Lote(s) Buffer para QGIS divide lotes com base em uma camada de linhas (como rios) e uma camada de polígonos (lotes). Ele cria um buffer ao redor da linha de entrada e usa essa geometria para gerar uma nova camada de polígonos representando os Lotes Divididos.'
    

    figura = 'images/dividelotebuffer.png'

    def shortHelpString(self):
        corpo = '''<div align="center">
                      <img src="'''+ os.path.join(os.path.dirname(os.path.dirname(__file__)), self.figura) +'''">
                      </div>
                      <div align="right">
                      <p align="right">
                      <b>'Autor: Maik Rodrigues'</b>
                      </p>'Georondonia'</div>
                    </div>'''
        return self.tr(self.texto) + corpo