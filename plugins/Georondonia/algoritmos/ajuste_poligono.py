# -*- coding: utf-8 -*-

"""
/***************************************************************************
 AjustePoligonos
                                 A QGIS plugin
 Ajusta uma camada de polígonos com base em uma camada de pontos.
 ***************************************************************************/
"""
__author__ = 'Seu Nome'
__date__ = '2024-03-07'
__copyright__ = '(C) 2024 by Seu Nome'

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingException,
                       QgsProject,
                       QgsSpatialIndex,
                       QgsFeature,
                       QgsGeometry)
from qgis.PyQt.QtGui import QIcon
import os

class AjustePoligonos(QgsProcessingAlgorithm):

    POLIGONO = 'POLIGONO'
    PONTOS = 'PONTOS'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return AjustePoligonos()

    def name(self):
        return 'ajuste_poligonos'

    def displayName(self):
        return self.tr('Ajuste de Polígonos')

    def group(self):
        #return self.tr('Ajustes Geométricos')
        return self.tr(self.groupId())

    def groupId(self):
        #return 'ajustes_geometricos'
        return self.tr(self.groupId())
    
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images/geoincra_pb.png'))

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.POLIGONO,
                self.tr('Camada de Polígonos'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.PONTOS,
                self.tr('Camada de Pontos'),
                [QgsProcessing.TypeVectorPoint]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Camada de Polígonos Ajustados')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        pol = self.parameterAsSource(parameters, self.POLIGONO, context)
        pnts = self.parameterAsSource(parameters, self.PONTOS, context)

        if pol is None or pnts is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.POLIGONO))

        # Criar índice espacial
        index = QgsSpatialIndex(pnts.getFeatures())
        vertices = {feat.id(): feat.geometry().asPoint() for feat in pnts.getFeatures()}

        layer = self.parameterAsSource(parameters, self.INPUT, context)
        if layer is not None:
            crs = layer.crs()  # Obtenha o CRS da camada   

        # Criar camada de saída
        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT, context, pol.fields(), pol.wkbType(),layer.crs())

        # Lista para armazenar geometrias problemáticas
        erros_geometria = []

        # Gerar polígonos ajustados
        for feat in pol.getFeatures():
            geom = feat.geometry()
            try:
                if geom.isEmpty():
                    feedback.pushInfo(f"Geometria vazia encontrada na Feição ID {feat.id()}.")
                    erros_geometria.append((feat.id(), "Geometria vazia"))
                    continue

                if not (geom.isMultipart() or geom.isPolygon()):
                    feedback.pushInfo(f"Geometria não é do tipo Polygon ou MultiPolygon na Feição ID {feat.id()}: {geom.asWkt()}")
                    erros_geometria.append((feat.id(), "Tipo de geometria inválido"))
                    continue

                coords = geom.asMultiPolygon()[0][0] if geom.isMultipart() else geom.asPolygon()[0]
                nova_lista = []

                for coord in coords:
                    nearest = index.nearestNeighbor(coord, 1)
                    if nearest:
                        nova_lista.append(vertices[nearest[0]])

                if nova_lista:
                    newGeom = QgsGeometry.fromPolygonXY([nova_lista])
                    new_feat = QgsFeature()
                    new_feat.setGeometry(newGeom)
                    sink.addFeature(new_feat, QgsFeatureSink.FastInsert)

            except Exception as e:
                feedback.pushInfo(f"Erro ao processar a Feição ID {feat.id()}: {str(e)}")
                erros_geometria.append((feat.id(), str(e)))

        # Exibir geometrias problemáticas
        if erros_geometria:
            feedback.pushInfo("Geometrias problemáticas encontradas:")
            for erro in erros_geometria:
                feedback.pushInfo(f"Feição ID: {erro[0]}, Erro: {erro[1]}")

        return {self.OUTPUT: dest_id}
