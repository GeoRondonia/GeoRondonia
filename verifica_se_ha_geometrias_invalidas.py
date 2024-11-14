from qgis.core import QgsProject, QgsFeature, QgsGeometry
import traceback

# Nome da camada
layer_name = 'parcela'  # Substitua pelo nome da sua camada

# Obtenha a camada pelo nome
layer = QgsProject.instance().mapLayersByName(layer_name)[0]

# Itere sobre as feições da camada
for feature in layer.getFeatures():
    geom = feature.geometry()
    
    try:
        # Verifique a validade da geometria
        if geom.isGeosValid():
            print(f"Feição ID {feature.id()} tem uma geometria válida.")
        else:
            print(f"Feição ID {feature.id()} tem uma geometria inválida.")
            # Exibindo atributos adicionais (se necessário)
            print(f"Atributos da feição: {feature.attributes()}")
            print(f"Geometria: {geom.asWkt()}")  # Mostra a geometria em formato WKT (Well-Known Text)
    except AttributeError as e:
        print(f"Erro de atributo ao processar a feição ID {feature.id()}: {e}")
    except TypeError as e:
        print(f"Erro de tipo ao processar a feição ID {feature.id()}: {e}")
    except ValueError as e:
        print(f"Erro de valor ao processar a feição ID {feature.id()}: {e}")
    except Exception as e:
        print(f"Erro inesperado ao processar a feição ID {feature.id()}: {e}")
        traceback.print_exc()
