"""
Este script é responsável por exportar camadas vetoriais do projeto QGIS para arquivos KML.
"""

import os

# Defina o diretório de exportação, onde os projetos ficaram salvos
caminho = r"C:\Arquivos de projetos CAR"

# Defina o nome da pasta do seu projeto
caminho = caminho + r"\1_CAR_PA_NOME_DO_PROJETO"

# Defina as camadas que não serão exportadas
filtroCamadas = ["Geo", "CAR", "INcRA"]

# Cria o diretório se não existir
if not os.path.exists(caminho):
    os.makedirs(caminho)

# Itera sobre as camadas vetoriais no projeto
for c in QgsProject.instance().mapLayers().values():
    
    # Inicializa a variável que indica se a camada deve ser ignorada
    skip_layer = False

    # Itera sobre cada nome na lista de camadas a serem filtradas
    for nome in filtroCamadas:
        # Verifica se o nome da camada atual contém algum dos nomes da lista de filtro (ignorando maiúsculas/minúsculas)
        if nome.lower() in c.name().lower():
            # Se encontrar uma correspondência, marca a camada para ser ignorada
            skip_layer = True
            break # Sai do loop, pois já não precisamos verificar os outros nomes

    # Se a variável skip_layer for True, pula para a próxima iteração do loop principal
    if skip_layer:
        continue
            
    if c.type() == QgsMapLayer.VectorLayer:  # Verifica se é uma camada vetorial
        if c.featureCount() > 0:  # Verifica se a camada tem feições
            
            # Define o caminho+nome do arquivo KML
            camArq = os.path.join(caminho, c.name())
            
            # Exporta a camada para KML
            error = QgsVectorFileWriter.writeAsVectorFormat(
                c, camArq + ".kml", "UTF-8", c.crs(), "KML"
            )
            
            if error[0] == QgsVectorFileWriter.NoError:
                print(f"Camada {c.name()} exportada com sucesso para KML.")
            else:
                print(f"Erro ao exportar a camada {c.name()}: {error[0]}")