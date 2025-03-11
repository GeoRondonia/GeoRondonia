"""
car_PrepareCarKml
***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************
"""
__author__ = 'Maik Rodrigues'
__date__ = '2025-02-27'
__copyright__ = '(C) 2025 by Maik Rodrigues'
__revision__ = '$Format:%H$'


from qgis.PyQt.QtCore import QCoreApplication
from ..geocapt.imgs import Imgs
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsProcessingException,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFolderDestination,
    QgsCoordinateReferenceSystem,
    QgsWkbTypes,
    QgsProcessing,
    QgsVectorFileWriter,
    QgsFeatureRequest
)

from qgis.PyQt.QtGui import QIcon
from qgis import processing
import os

class prepareCAR(QgsProcessingAlgorithm):
    INPUT_LAYER = 'INPUT_LAYER'
    OUTPUT_FOLDER = 'OUTPUT_FOLDER'

    def tr(self, string, string_pt=None):
        if string_pt:
            return QCoreApplication.translate('Processing', string_pt)  # Return the Portuguese translation
        return QCoreApplication.translate('Processing', string)  # Default to English

    def createInstance(self):
        return prepareCAR()

    def name(self):
        return 'preparaCAR'

    def displayName(self):
        return self.tr('Prepara KML para o CAR')
    
    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return ''
    
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images/geocar.png'))
    txt_en = '''Export vector layers that are selected from the QGIS project to KML files in a destination folder.'''
    txt_pt = '''Esta ferramenta exporta feições selecionadas de camadas vetoriais do projeto QGIS para arquivos KML. Suporta diferentes tipos de geometria (ponto, linha, polígono) e garante que apenas as feições dentro do perímetro da máscara sejam incluídas no arquivo KML.
    <h3>Exemplo de Uso:</h3>
    1. Selecione a camada de entrada (máscara) e Selecione uma feição no prejeto.
    2. Escolha as camadas de sobreposição no "Painel de Camadas" no QGIS e marque um ✅ na camada.
    3. Defina a pasta de destino.
    4. Execute a ferramenta.
    '''

    figure1 = 'images\illustration\PrepareCAR.png'
    figure2 = 'images\modelo-logos-parcerias-geo.png'
	
    def shortHelpString(self):
        
        social_BW = Imgs().social_BW
        footer = '''<div style="text-align: right;">
                      <img src="'''+ os.path.join(os.path.dirname(os.path.dirname(__file__)),self.figure1) +'''"><br>
                      <img src="'''+ os.path.join(os.path.dirname(os.path.dirname(__file__)),self.figure2) +'''">
                      </div>
                      <div align="right">
                      <p align="right">
                      <b>'''+self.tr('Author: Maik Rodrigues, Prof Cazaroli, Leandro França, Valdir Moura, Ranieli dos Anjos, Ivan Chorobura, Isis Nascimento, João Vitor Ebeling, Rafaela Braga and Alisson Amorim', 'Autor: Maik Rodrigues, Prof Cazaroli, Leandro Franca, Valdir Moura, Ranieli dos Anjos, Ivan Chorobura, Isis Nascimento, João Vitor Ebeling, Rafaela Braga e Alisson Amorim')+'''</b>
                      </p>'''+ social_BW + '''</div>
                    </div>'''
        return self.tr(self.txt_en, self.txt_pt) + footer

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LAYER,
                self.tr('Camada de Entrada (Máscara)'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT_FOLDER,
                self.tr('Pasta de Destino'),
                defaultValue=r"C:\Projetos CAR KML"
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        output_folder = self.parameterAsString(parameters, self.OUTPUT_FOLDER, context)

        # Validação de geometria
        if QgsWkbTypes.flatType(input_layer.wkbType()) not in [QgsWkbTypes.Polygon, QgsWkbTypes.MultiPolygon]:
            raise QgsProcessingException(self.tr('A camada de entrada deve ser do tipo polígono ou multipolígono'))

        os.makedirs(output_folder, exist_ok=True)
        feedback.pushInfo(self.tr(f'Processando camadas de sobreposição...'))

        # Coleta camadas de sobreposição visíveis
        project = QgsProject.instance()
        overlay_layers = [
            l for l in project.mapLayers().values()
            if isinstance(l, QgsVectorLayer)
            and l != input_layer
            and project.layerTreeRoot().findLayer(l).isVisible()
        ]

        if not overlay_layers:
            raise QgsProcessingException(self.tr('Nenhuma camada de sobreposição selecionada'))

        resultados = []
        total = 100.0 / len(overlay_layers)

        # Filtra as feições selecionadas da camada de entrada
        selected_features = input_layer.selectedFeatures()
        if not selected_features:
            raise QgsProcessingException(self.tr('Selecione pelo menos uma feição na camada de entrada'))

        # Verificar se o campo 'layer' existe
        if 'layer' not in selected_features[0].fields().names():
            raise QgsProcessingException(self.tr('O campo "layer" não existe na camada de entrada'))
        
        # Cria uma camada temporária com as feições selecionadas
        temp_input_layer = QgsVectorLayer("MultiPolygon?crs={}".format(input_layer.crs().authid()), "temp_input", "memory")
        temp_input_layer.dataProvider().addAttributes(input_layer.fields())
        temp_input_layer.updateFields()
        temp_input_layer.dataProvider().addFeatures(selected_features)
        
        # Obtém o valor do campo 'layer' da feição selecionada
        layer_value = str(selected_features[0]['layer']).replace(" ", "_")

        
        for i, overlay in enumerate(overlay_layers):
            if feedback.isCanceled():
                break

            try:
                # Verifica se a camada de sobreposição tem feições
                if overlay.featureCount() == 0:
                    feedback.reportError(self.tr(f'Camada {overlay.name()} não contém feições. Ignorando...'))
                    continue

                # Seleciona as feições que estão dentro da camada de entrada usando o algoritmo selectByLocation
                params_select = {
                    'INPUT': overlay,
                    'PREDICATE': [0],  # 0 significa "contains"
                    'INTERSECT': temp_input_layer,
                    'METHOD': 0  # 0 significa "create new selection"
                }
                processing.run('native:selectbylocation', params_select, context=context)

                # Obtém as feições selecionadas
                selected_overlay_features = overlay.selectedFeatures()
                if not selected_overlay_features:
                    feedback.pushInfo(self.tr(f'Nenhuma feição da camada {overlay.name()} está dentro da máscara. Ignorando...'))
                    continue

                # Cria uma camada temporária com as feições selecionadas, considerando o tipo de geometria
                geom_type = overlay.geometryType()
                if geom_type == QgsWkbTypes.PointGeometry:
                    temp_overlay_layer = QgsVectorLayer("Point?crs={}".format(overlay.crs().authid()), "temp_overlay", "memory")
                elif geom_type == QgsWkbTypes.LineGeometry:
                    temp_overlay_layer = QgsVectorLayer("LineString?crs={}".format(overlay.crs().authid()), "temp_overlay", "memory")
                else:
                    temp_overlay_layer = QgsVectorLayer("MultiPolygon?crs={}".format(overlay.crs().authid()), "temp_overlay", "memory")

                temp_overlay_layer.dataProvider().addAttributes(overlay.fields())
                temp_overlay_layer.updateFields()
                temp_overlay_layer.dataProvider().addFeatures(selected_overlay_features)

                # Reprojeta para WGS84 se necessário
                if temp_overlay_layer.crs().authid() != 'EPSG:4326':
                    params_reproj = {
                        'INPUT': temp_overlay_layer,
                        'TARGET_CRS': 'EPSG:4326',
                        'OUTPUT': 'TEMPORARY_OUTPUT'
                    }
                    temp_overlay_layer = processing.run('native:reprojectlayer', params_reproj, context=context)['OUTPUT']

                # Exporta para KML
                nome_saida = f"{overlay.name()}_{layer_value}.kml"
                caminho_saida = os.path.join(output_folder, nome_saida)
                
                error = QgsVectorFileWriter.writeAsVectorFormat(
                    temp_overlay_layer,
                    caminho_saida,
                    'UTF-8',
                    temp_overlay_layer.crs(),
                    'KML'
                )

                if error[0] == QgsVectorFileWriter.NoError:
                    resultados.append(nome_saida)
                    feedback.pushInfo(self.tr(f'Exportado: {nome_saida}'))
                else:
                    feedback.reportError(self.tr(f'Erro ao exportar {nome_saida}'))

            except Exception as e:
                feedback.reportError(self.tr(f'Falha ao processar {overlay.name()}: {str(e)}'))

            feedback.setProgress(int(i * total))

        if resultados:
            feedback.pushInfo(self.tr(f'\n\n Arquivos salvos em: {output_folder}'))
            feedback.reportError(f"\n__________________\n\n>----FIM DO JOB!!----<\n__________________\n\n")
        else:
            feedback.reportError(self.tr('Nenhum resultado gerado'))

        return {'RESULTADOS': resultados}
    def print_layer_value():
        from qgis.utils import iface
        
        # Acessar a camada ativa
        layer = iface.activeLayer()
        
        # Verificar se há feições selecionadas
        if layer.selectedFeatureCount() > 0:
            # Iterar sobre as feições selecionadas
            for feature in layer.selectedFeatures():
                # Acessar o atributo da coluna "layer"
                layer_value = feature['layer']
                
                # Imprimir o valor
                print(f"{layer_value}")
        else:
            print("Nenhuma feição selecionada.")

