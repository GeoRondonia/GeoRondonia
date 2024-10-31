from qgis.core import QgsProject, QgsVectorLayer, QgsSpatialIndex, QgsFeature, QgsGeometry

# Ler camada de polígono da base do INCRA
nome = 'parcela'
pol = QgsProject.instance().mapLayersByName(nome)[0]

# Ler camada de vértices (pontos Levantados)
nome = 'vertice'
pnts = QgsProject.instance().mapLayersByName(nome)[0]

# Criar índice espacial
index = QgsSpatialIndex(pnts.getFeatures())
vertices = {}
for feat in pnts.getFeatures():
    pnt = feat.geometry().asPoint()
    vertices[feat.id()] = pnt

# Criar camada de saída
vl = QgsVectorLayer("PolygonZ", "poligono ajustado", "memory")
vl.setCrs(pnts.crs())
pr = vl.dataProvider()

# Gerar polígonos ajustados
for feat in pol.getFeatures():
    geom = feat.geometry()
    coords = geom.asMultiPolygon()[0][0] if geom.isMultipart() else geom.asMultiPolygon()[0]
    nova_lista = []
    
    # Para cada ponto achar o mais próximo
    for coord in coords:
        nearest = index.nearestNeighbor(coord, 1)
        if nearest:  # Verificar se há um ponto mais próximo
            nova_lista.append(vertices[nearest[0]])
    
    # Novo polígono
    fet = QgsFeature()
    if nova_lista:  # Verifique se a nova lista não está vazia
        # Criar a geometria do polígono a partir da nova lista de pontos
        newGeom = QgsGeometry.fromPolygonXY([nova_lista])  # Envolver nova_lista em outra lista
        fet.setGeometry(newGeom)
        pr.addFeature(fet)

# Adicionar a camada ao projeto
QgsProject.instance().addMapLayer(vl)