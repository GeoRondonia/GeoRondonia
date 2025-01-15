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
    global feitos

    # Obter os lotes
    lotes = [feat for feat in parcela.getFeatures()]
    
    # Ordenar os lotes pelo campo 'denominacao'
    lotes_ordenados = sorted(lotes, key=lambda feat: int(''.join(filter(str.isdigit, feat['denominacao']))) if ''.join(filter(str.isdigit, feat['denominacao'])) else 0)

    # Identificar a seleção atual
    current_selection = parcela.selectedFeatures()
    current_lote = current_selection[0]['denominacao'] if current_selection else None

    # Encontrar o índice do lote atual
    if current_lote:
        current_index = next((i for i, feat in enumerate(lotes_ordenados) if feat['denominacao'] == current_lote), None)
    else:
        current_index = -1

    # Selecionar o próximo lote
    if current_index is not None and current_index + 1 < len(lotes_ordenados):
        next_feat = lotes_ordenados[current_index + 1]
        lote = next_feat['denominacao']
        feitos.append(lote)
        print(lote)
        
        # Selecionar a feição na camada parcela
        parcela.selectByIds([next_feat.id()])

        # Criar expressão para selecionar feições nas outras camadas
        expression = QgsExpression('"denominacao" = \'{}\''.format(lote))

        # Selecionar feições na camada vértice
        ids_selecionados_vertice = [f.id() for f in vertice.getFeatures(QgsFeatureRequest(expression))]
        vertice.selectByIds(ids_selecionados_vertice)

        # Selecionar feições na camada limite
        ids_selecionados_limite = [f.id() for f in limite.getFeatures(QgsFeatureRequest(expression))]
        limite.selectByIds(ids_selecionados_limite)