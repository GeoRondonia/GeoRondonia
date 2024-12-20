# Autor: Maik Rodrigues de Souza
# Data: 20-12-2024
# Descrição: Modifica arquivos ODS, atualizando células específicas em planilhas nas celulas donominação e Parcela número. É necessário instalar a biblioteca ezodf pelo terminal do QGIS. Para isso, acesse o OSGeo4W no Windows e digite o seguinte comando: pip install ezodf


import ezodf
import os 
# Diretório onde os arquivos ODS estão localizados
# Apague o que está entre " " e cole o seu caminho aqui.
diretorio_ods = r"G:\Meu Drive\GEO_RO\PAs para teste"

# Iterar sobre todos os arquivos no diretório
for arquivo in os.listdir(diretorio_ods):
    if arquivo.endswith(".ods"):  # Verificar se é um arquivo .ods
        caminho_arquivo = os.path.join(diretorio_ods, arquivo)
        
        # Carregar o arquivo ODS
        planilha = ezodf.opendoc(caminho_arquivo)

        # Imprimir os nomes de todas as planilhas
        print(f"Nomes das planilhas em {arquivo}:")
        for sheet in planilha.sheets:
            if "perimetro_" in sheet.name:
                # Celuna denominação
                celula_b3 = sheet['B3']
                celula_b3.set_value("Part "+sheet.name[-1])
                # Celula Parcela número
                celula_b4 = sheet['B4'] 
                celula_b4.set_value("00"+sheet.name[-1])
            
        sheet = planilha.sheets[0]  # Selecionar a primeira planilha
        
        # Acessar as células B17 e A17
        celula_b17 = sheet['B17']
        celula_a17 = sheet['A17']
        
        # Verificar se o valor de B17 é uma string e contém ';'
        valor_a17 = celula_a17.value
        if isinstance(valor_a17, str) and ';' in valor_a17:
            # Substituir o valor de A17 com o conteúdo antes do ';'
            novo_valor_a17 = valor_a17.split(';')[0]
            celula_a17.set_value(novo_valor_a17)
        
        # Salvar as alterações no mesmo arquivo
        planilha.save()

        print(f"Processado: {arquivo}")
print("|=====================|")
print("|---------------------|")
print("|---------------------|")
print("|-----Finalizado!-----|")
print("|---------------------|")
print("|---------------------|")
print("|=====================|")