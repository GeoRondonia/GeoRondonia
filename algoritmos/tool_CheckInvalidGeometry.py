
"""
tool_CheckInvalidGeometry
***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************
"""

__author__ = 'Maik Rodrigues e Bárbara Laura'
__date__ = '2025-02-21'
__copyright__ = '(C) 2024 by Maik Rodrigues'
__revision__ = '$Format:%H$'

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
    txt_en = '''This plugin checks the validity of geometries in a vector layer, identifying features with invalid geometries and records without geometry (so-called "ghosts" 👻). 
                It automatically highlights problematic features in the         attribute table and generates a detailed report, facilitating the correction or removal of errors and ensuring data integrity'''
    txt_pt = '''Este plugin verifica a validade das geometrias em uma camada vetorial, identificando feições com geometrias inválidas e registros sem geometria (os chamados "fantasmas" 👻). 
                Ele destaca automaticamente as feições problemáticas na tabela de atributos e gera um relatório detalhado, facilitando a correção ou remoção dos erros e garantindo a integridade dos dados'''
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
                      <b>'''+self.tr('Author: Maik Rodrigues, Bárbara Laura, Valdir Moura, Ranieli dos Anjos, Mychelle Novais and Carolina Potratz', 'Autor: Maik Rodrigues, Bárbara Laura, Valdir Moura, Ranieli dos Anjos, Mychelle Novais e Carolina Potratz')+'''</b>
                      </p>'''+ social_BW + '''</div>
                    </div>'''
        return self.tr(self.txt_en, self.txt_pt) + footer

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
                [QgsProcessing.SourceType.TypeVectorAnyGeometry],
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
                    feedback.reportError(f"Feição ID {feature.id()} - Geometria inválida")
            except Exception as e:
                invalid_ids.append(feature.id())
                feedback.reportError(f"Erro na feição ID {feature.id()}: {str(e)}")
                traceback.print_exc()

            feedback.setProgress(int(current * step))

        if invalid_ids:
            try:
                input_layer.selectByIds(invalid_ids) # Seleciona as feições com geometria inválida 
                feedback.reportError(f"\nTotal de feições inválidas selecionadas na tabela de atributos: {len(invalid_ids)}") # Quantidade de feições com geometria inválida         
                feedback.reportError(f"\n__________________\n\n>----FIM DO JOB!!----<\n__________________\n\n") 
            except Exception as e:
                feedback.reportError(f"Erro ao selecionar feições: {str(e)}")
                feedback.pushInfo("IDs das feições inválidas: " + ", ".join(map(str, invalid_ids)))
                
                
        else:
            raise QgsProcessingException("\nNenhuma feição com erro foi encontrada.")


        return {}

    