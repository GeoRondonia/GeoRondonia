# SELECIONAR PRÓXIMO
# import processing, os
# pasta = r'C:\Users\sazon\Downloads\GeoRondonia\ODS'

# Abrir camada vértice
vertice = QgsProject.instance().mapLayersByName('vertice')[0]
# Abrir camada limite
limite = QgsProject.instance().mapLayersByName('limite')[0]
# Abrir camada parcela
parcela = QgsProject.instance().mapLayersByName('parcela')[0]

# SELECIONAR PRÓXIMO
# import processing, os
# pasta = r'C:\Users\sazon\Downloads\GeoRondonia\ODS'

# Abrir camada vértice
vertice = QgsProject.instance().mapLayersByName('vertice')[0]
# Abrir camada limite
limite = QgsProject.instance().mapLayersByName('limite')[0]
# Abrir camada parcela
parcela = QgsProject.instance().mapLayersByName('parcela')[0]

# Iteração
feitos = []
def selecionar_proximo():
    # Obter os lotes
    lotes = [feat['denominacao'] for feat in parcela.getFeatures()]
    
    # Ordenar os lotes
    lotes_ordenados = sorted(lotes, key=lambda x: int(''.join(filter(str.isdigit, str(x)))) if ''.join(filter(str.isdigit, str(x))) else 0)
    
    # Imprimir os lotes ordenados
    for lote in lotes_ordenados:
        print(lote)