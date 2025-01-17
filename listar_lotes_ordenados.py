
"""
Script para listar lotes ordenados no QGIS
Autor: Maik Rodrigues de Souza
Data: 16/01/2025
"""

# Abrir camada vértice
vertice = QgsProject.instance().mapLayersByName('vertice')[0]
# Abrir camada limite
limite = QgsProject.instance().mapLayersByName('limite')[0]
# Abrir camada parcela
parcela = QgsProject.instance().mapLayersByName('parcela')[0]


def listar_todos_lotes():
    # Obter os lotes
    lotes = [feat for feat in parcela.getFeatures()]
    
    # Ordenar os lotes pelo campo 'denominacao'
    lotes_ordenados = sorted(lotes, key=lambda feat: int(''.join(filter(str.isdigit, feat['lote']))) if ''.join(filter(str.isdigit, feat['lote'])) else 0)
    
    print("=== Lista de Todos os Lotes Ordenados ===")
    print(f"Total de lotes: {len(lotes_ordenados)}")
    print("-" * 40)
    
    # Iterar sobre todos os lotes ordenados
    for i, lote in enumerate(lotes_ordenados, 1):
        denominacao = lote['lote']
        # Você pode adicionar mais campos aqui se desejar
        print(f"Lote {i}: {denominacao}")
        
    print("-" * 40)
    print("Fim da listagem")

# Para usar a função, basta chamar:
listar_todos_lotes()
