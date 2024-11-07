"""
Este script é responsável por exportar camadas vetoriais do projeto QGIS para arquivos Shapefile e, em seguida, compactá-los em arquivos ZIP. 
"""

import os
import zipfile

# Defina o diretório de exportação, onde os arquivos zip serão criados
caminho = r"G:\Meu Drive\GEO_RO\Jandaira\Projeto Integrado"

caminho = caminho + "\Arquivos para o CAR"

# Defina as camadas que não serão ZIPADA
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
           # if "Geo" in c.name() or "CAR" in c.name() or "INCRA" in c.name():
            #    continue
            # Define o caminho+nome do Shapefile
            camArq = os.path.join(caminho, c.name())
            
            # Exporta a camada para Shapefile
            error = QgsVectorFileWriter.writeAsVectorFormat(
                c, camArq + ".shp", "UTF-8", c.crs(), "ESRI Shapefile"
            )
            
            if error[0] == QgsVectorFileWriter.NoError:
                print(f"Camada {c.name()} exportada com sucesso.")
                
                # Lista de extensões associadas ao Shapefile
                extensoes = [".shp", ".shx", ".dbf", ".prj", ".cpg"]
                
                # Caminhos completos para os arquivos gerados
                shapefile_files = [
                    camArq + ext for ext in extensoes if os.path.exists(camArq + ext)
                ]
                
                # Nome do arquivo ZIP para a camada
                nomeZip = os.path.join(caminho, c.name() + ".zip")
                
                # Compacta os arquivos da camada em um ZIP
                with zipfile.ZipFile(nomeZip, 'w') as zipf:
                    for f in shapefile_files:
                        zipf.write(f, os.path.basename(f))  # Adiciona o arquivo ao ZIP
                        
                print(f"Camada {c.name()} compactada em {nomeZip}.")
                
                # Apaga os arquivos Shapefile após compactar
                for f in shapefile_files:
                    try:
                        os.remove(f)
                        print(f"Arquivo {f} removido.")
                    except OSError as e:
                        print(f"Erro ao remover {f}: {e}")
            else:
                print(f"Erro ao exportar a camada {c.name()}: {error[0]}")
