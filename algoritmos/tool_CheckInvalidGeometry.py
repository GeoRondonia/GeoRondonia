# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from ..geocapt.imgs import Imgs
from qgis.core import (QgsProcessing,
                      QgsProcessingAlgorithm,
                      QgsProcessingParameterVectorLayer,
                      QgsProcessingException,
                      QgsFeatureRequest,
                      QgsGeometry,
                      QgsProject)
import traceback, os

class CheckInvalidGeometry(QgsProcessingAlgorithm):
    INPUT_LAYER = 'INPUT_LAYER'

    def tr(self, string, string_pt=None):
        if string_pt:
            return QCoreApplication.translate('Processing', string_pt)  # Return the Portuguese translation
        return QCoreApplication.translate('Processing', string)  # Default to English
		    


    def createInstance(self):
        return CheckInvalidGeometry()

    def name(self):
        return 'CheckInvalidGeometry'

    def displayName(self):
        return self.tr('Validação de Geometrias')

    def group(self):
        return self.tr('')

    def groupId(self):
        return ''
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images/geometry.png'))
    txt_en = '''Checks the validity of geometries in a vector layer. Features with invalid geometries will be selected in the attribute table'''
    txt_pt = '''Verifica a validade das geometrias em uma camada vetorial. Feições com geometrias inválidas serão selecionadas na tabela de atributos.'''
    figure1 = 'images\illustration\CheckInvalidGeometry300x150.png'
    figure2 = 'images\modelo-logos-parcerias-geo.png'
	
    def shortHelpString(self):
        social_BW = Imgs().social_BW
        footer = '''<div style="text-align: right;">
                      <img src="'''+ os.path.join(os.path.dirname(os.path.dirname(__file__)),self.figure1) +'''"><br>
                      <img src="'''+ os.path.join(os.path.dirname(os.path.dirname(__file__)),self.figure2) +'''">
                      </div>
                      <div align="right">
                      <p align="right">
                      <b>'''+self.tr('Autor: Maik Rodrigues de Souza, Mychelle Novais Soares, Carolina Potratz Giraldello, Valdir Moura e Ranieli dos Anjos de Souza.')+'''</b>
                      </p>'''+ social_BW + '''</div>
                    </div>'''
        return self.tr(self.txt_en, self.txt_pt) + footer
    # def shortHelpString(self):
    #     return self.tr("""
    #     Verifica a validade das geometrias em uma camada vetorial.
    #     Feições com geometrias inválidas serão selecionadas na tabela de atributos.
    #     Autor: Maik Rodrigues de Souza
    #     Versão: 2.0
    #     """)

    def initAlgorithm(self, config=None):
        # Encontra automaticamente a camada 'parcela' se existir no projeto
        parcela_layer = next(
            (lyr for lyr in QgsProject.instance().mapLayers().values() 
             if lyr.name() == 'parcela'),
            None
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LAYER,
                self.tr('Selecione a camada vetorial'),
                [QgsProcessing.TypeVectorAnyGeometry],
                defaultValue=parcela_layer.source() if parcela_layer else None
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(
            parameters,
            self.INPUT_LAYER,
            context
        )
        
        if not input_layer:
            raise QgsProcessingException("Nenhuma camada válida selecionada")

        invalid_ids = []
        total_features = input_layer.featureCount()
        step = 100 / total_features if total_features > 0 else 1

        for current, feature in enumerate(input_layer.getFeatures()):
            if feedback.isCanceled():
                break

            try:
                geom = feature.geometry()
                if not geom.isGeosValid():
                    invalid_ids.append(feature.id())
                    feedback.pushInfo(f"Feição ID {feature.id()} - Geometria inválida")
            except Exception as e:
                invalid_ids.append(feature.id())
                feedback.reportError(f"Erro na feição ID {feature.id()}: {str(e)}")
                traceback.print_exc()

            feedback.setProgress(int(current * step))

        if invalid_ids:
            try:
                input_layer.selectByIds(invalid_ids)
                feedback.pushInfo(f"\nTotal de feições inválidas selecionadas: {len(invalid_ids)}")
                self.finish_job()
            except Exception as e:
                feedback.reportError(f"Erro ao selecionar feições: {str(e)}")
                feedback.pushInfo("IDs das feições inválidas: " + ", ".join(map(str, invalid_ids)))
                
                
        else:
            raise QgsProcessingException("\nNenhuma feição com erro foi encontrada.")


        return {}

    def finish_job(self):
        raise QgsProcessingException("\n>----- FIM DO JOB -----<")