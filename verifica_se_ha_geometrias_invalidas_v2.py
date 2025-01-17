from qgis.core import QgsProject, QgsFeature, QgsGeometry
import traceback

# Nome da camada
layer_name = 'parcela'  # Substitua pelo nome da sua camada

# Obtenha a camada pelo nome
layer = QgsProject.instance().mapLayersByName(layer_name)[0]

# Lista para armazenar os IDs das feições com erro
invalid_features = []

# Itere sobre as feições da camada
for feature in layer.getFeatures():
    geom = feature.geometry()
    
    try:
        # Verifique a validade da geometria
        if geom.isGeosValid():
            print(f"Feição ID {feature.id()} tem uma geometria válida.")
        else:
            print(f"Feição ID {feature.id()} tem uma geometria inválida.")
            invalid_features.append(feature.id())
            # Exibindo atributos adicionais (se necessário)
            print(f"Atributos da feição: {feature.attributes()}")
            print(f"Geometria: {geom.asWkt()}")  # Mostra a geometria em formato WKT
    except (AttributeError, TypeError, ValueError) as e:
        print(f"Erro ao processar a feição ID {feature.id()}: {e}")
        invalid_features.append(feature.id())
    except Exception as e:
        print(f"Erro inesperado ao processar a feição ID {feature.id()}: {e}")
        traceback.print_exc()
        invalid_features.append(feature.id())

# Seleciona todas as feições com erro na tabela de atributos
if invalid_features:
    layer.selectByIds(invalid_features)
    print(f"\nTotal de feições com erro: {len(invalid_features)}")
    print("Feições com erro foram selecionadas na tabela de atributos.")
else:
    print("\nNenhuma feição com erro foi encontrada.")