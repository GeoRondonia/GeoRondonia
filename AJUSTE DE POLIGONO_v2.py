"""
Script para ajustar uma camada de polígonos com base em uma camada de pontos.
Para cada ponto do polígono, encontra-se o ponto mais próximo na camada de vértices e gera um novo polígono ajustado.
Certifique-se de que as camadas 'poligono' e 'pontos' estão carregadas no projeto QGIS antes de executar.
"""

from qgis.core import QgsProject, QgsVectorLayer, QgsSpatialIndex, QgsFeature, QgsGeometry

# Ler camada de polígono da base do INCRA
nome = 'camada de poligono'
pol = QgsProject.instance().mapLayersByName(nome)[0]

# Ler camada de vértices (pontos Levantados)
nome = 'camada de ponto'
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

# Lista para armazenar geometrias problemáticas
erros_geometria = []

# Gerar polígonos ajustados
for feat in pol.getFeatures():
    geom = feat.geometry()
    
    try:
        # Verifique se a geometria é válida
        if geom.isEmpty():
            print(f"Geometria vazia encontrada na Feição ID {feat.id()}.")
            erros_geometria.append((feat.id(), "Geometria vazia"))
            continue
        
        # Verifique se a geometria é do tipo esperado
        if not (geom.isMultipart() or geom.isPolygon()):
            print(f"Geometria não é do tipo Polygon ou MultiPolygon na Feição ID {feat.id()}: {geom.asWkt()}")
            erros_geometria.append((feat.id(), "Tipo de geometria inválido"))
            continue

        # Obter coordenadas
        coords = geom.asMultiPolygon()[0][0] if geom.isMultipart() else geom.asPolygon()[0]

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

    except Exception as e:
        print(f"Erro ao processar a Feição ID {feat.id()}: {str(e)}")
        erros_geometria.append((feat.id(), str(e)))

# Adicionar a camada ao projeto
QgsProject.instance().addMapLayer(vl)

# Exibir geometrias problemáticas
if erros_geometria:
    print("Geometrias problemáticas encontradas:")
    for erro in erros_geometria:
        print(f"Feição ID: {erro[0]}, Erro: {erro[1]}")
        