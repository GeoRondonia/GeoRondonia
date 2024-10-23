import ezodf
import os

# Diretório onde os arquivos ODS estão localizados
diretorio_ods = r"C:\Users\Maik\Documents\GitHub\GEO_GIT"

# Iterar sobre todos os arquivos no diretório
for arquivo in os.listdir(diretorio_ods):
    if arquivo.endswith(".ods"):  # Verificar se é um arquivo .ods
        caminho_arquivo = os.path.join(diretorio_ods, arquivo)
        
        # Carregar o arquivo ODS
        planilha = ezodf.opendoc(caminho_arquivo)
        sheet = planilha.sheets[0]  # Selecionar a primeira planilha
        
        # Acessar as células B17 e A17
        celula_b17 = sheet['B17']
        celula_a17 = sheet['A17']
        
        # Verificar se o valor de B17 é uma string e contém ';'
        valor_b17 = celula_b17.value
        if isinstance(valor_b17, str) and ';' in valor_b17:
            # Substituir o valor de A17 com o conteúdo antes do ';'
            novo_valor_a17 = valor_b17.split(';')[0]
            celula_a17.set_value(novo_valor_a17)
        
        # Salvar as alterações no mesmo arquivo
        planilha.save()

        print(f"Processado: {arquivo}")