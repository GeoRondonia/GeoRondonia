# -*- coding: utf-8 -*-

"""
georural_Geradordeods
***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************
"""

__author__ = 'Maik Rodrigues'
__date__ = '2024-11-13'
__copyright__ = '(C) 2024 by Maik Rodrigues'


from qgis.PyQt.QtCore import QCoreApplication, QVariant # Import QVariant
from ..geocapt.imgs import Imgs
from qgis.core import (QgsProcessing,
                       QgsProject,
                       QgsProcessingException,
                       QgsGeometry,
                       QgsProcessingParameterNumber,
                       QgsExpressionContextUtils,
                       QgsExpressionContext,
                       QgsProcessingParameterFeatureSource,
                       QgsFeatureRequest,
                       QgsProcessingAlgorithm,
                       QgsExpression,
                       QgsProcessingParameterFileDestination,
                       QgsMapLayer,
                       QgsVectorLayer
                       )
# Assuming geocapt.imgs is available in the environment
# from ..geocapt.imgs import Imgs # This might need adjustment based on package structure
import logging
from math import floor
from qgis.utils import iface
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import QgsMessageLog, Qgis
import subprocess
import os
from pathlib import Path
import shutil

def find_layer_by_name(layer_name):
    """
    Procura uma camada vetorial no projeto QGIS atual pelo nome (case-insensitive).
    Retorna o ID da camada se encontrada e for do tipo QgsVectorLayer,
    caso contrário, retorna None.
    """
    for layer_id, layer in QgsProject.instance().mapLayers().items():
        if isinstance(layer, QgsVectorLayer) and layer.name().lower() == layer_name.lower():
            return layer.id()
    return None

class GeneratorOds(QgsProcessingAlgorithm):

    VERTICE = 'VERTICE'
    LIMITE  = 'LIMITE'
    PARCELA  ='PARCELA'
    OUTPUT = 'OUTPUT'
    DEC_COORD = 'DEC_COORD'
    DEC_PREC = 'DEC_PREC'

    def tr(self, string, string_pt=None):
        if string_pt:
            return QCoreApplication.translate('Processing', string_pt)  # Return the Portuguese translation
        return QCoreApplication.translate('Processing', string)  # Default to English


    def createInstance(self):
        return GeneratorOds()

    def name(self):
        return 'georural_generatorOds'

    def displayName(self):
        return self.tr('Gerador de ODS (GODS)')
        return self.tr('ODS Generator (GODS)')

    def group(self):
        return self.tr('')

    def groupId(self):
        return ''
    def icon(self):
        # Adjusted path assuming images folder is parallel to the current script's parent folder
        return QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images/spreadsheet.png'))

    txt_en = '''Creates a SIGEF ODS spreadsheet, filling it directly through Macros, from the GeoRural database layers worked in QGIS'''
    txt_pt = '''Cria uma planilha ODS do SIGEF, preenchendo-a diretamente através de Macros, a partir das camadas do banco de dados GeoRural trabalhado no QGIS.'''

    figure1 =  'images\illustration\ods-gods.png'
    figure2 = 'images\modelo-logos-parcerias-geo.png'


    def shortHelpString(self):
        social_BW = Imgs().social_BW

        footer = '''<div style="text-align: right;">
                      
                      <img src="''' + os.path.join(os.path.dirname(os.path.dirname(__file__)), self.figure1) + '''"><br>
                      <img src="''' + os.path.join(os.path.dirname(os.path.dirname(__file__)), self.figure2) + '''">
                      </div>
                      <div align="right">
                      <p align="right">
                      <b>''' + self.tr('Autor: Maik Rodrigues, Valdir Moura, Ranieli dos Anjos, Mychelle Novais e Carolina Potratz.') + '''</b>
                      </p>''' + social_BW + '''</div>
                    </div>'''
        return self.tr(self.txt_en, self.txt_pt) + footer
        help_text = self.tr('''Creates a SIGEF ODS spreadsheet, filling it directly through Macros, from the GeoRural database layers worked in QGIS.''')
        return help_text + footer

    def initAlgorithm(self, config=None):
        vertice_default_id = find_layer_by_name("vertice")
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.VERTICE,
                self.tr('Camada Vertice'),
                [QgsProcessing.TypeVectorPoint], # Espera uma camada de ponto
                defaultValue=vertice_default_id # Define o valor padrão aqui!
            )
        )

        # --- Parâmetro Camada Limite ---
        limite_default_id = find_layer_by_name("limite")
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.LIMITE,
                self.tr('Camada Limite'),
                [QgsProcessing.TypeVectorLine], # Espera uma camada de linha
                defaultValue=limite_default_id # Define o valor padrão aqui!
            )
        )

        # --- Parâmetro Camada Parcela ---
        parcela_default_id = find_layer_by_name("parcela")
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.PARCELA,
                self.tr('Camada Parcela'),
                [QgsProcessing.TypeVectorPolygon], # Espera uma camada de polígono
                defaultValue=parcela_default_id # Define o valor padrão aqui!
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.DEC_COORD,
                self.tr('Casas decimais das coordenadas'),
                type = QgsProcessingParameterNumber.Type.Integer,
                defaultValue = 3,
                minValue = 3
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.DEC_PREC,
                self.tr('Casas decimais das precisões e altitude'),
                type = QgsProcessingParameterNumber.Type.Integer,
                defaultValue = 2,
                minValue = 2
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr('Planilha ODS'),
                self.tr('Planilha OpenDocument (*.ods)')
            )
        )
    
    # --- Funções auxiliares para extração segura de atributos ---
    def get_safe_string_attribute(self, feature, attr_name):
        """Extrai um atributo como string Python, tratando QVariant e tipos nativos."""
        value = feature[attr_name]
        # QVariant
        if isinstance(value, QVariant):
            try:
                if value.isValid() and not value.isNull():
                    s = value.toString()
                    if s is None:
                        return ''
                    return str(s).strip().replace('NULL', '').replace('\n', '')
                return ''
            except Exception:
                try:
                    return str(value).strip().replace('NULL', '').replace('\n', '')
                except Exception:
                    return ''
        # Tipo Python nativo
        if value is None:
            return ''
        return str(value).strip().replace('NULL', '').replace('\n', '')

    def get_safe_int_attribute(self, feature, attr_name):
        """Extrai um atributo como int Python, tratando QVariant e tipos nativos."""
        value = feature[attr_name]
        # QVariant
        if isinstance(value, QVariant):
            try:
                if value.isValid() and not value.isNull():
                    # tentar toInt primeiro
                    try:
                        ival = value.toInt()[0]
                        return int(ival)
                    except Exception:
                        pass
                    # tentar converter da string
                    try:
                        return int(value.toString())
                    except Exception:
                        return None
                return None
            except Exception:
                try:
                    return int(str(value))
                except Exception:
                    return None
        # Tipo Python nativo
        if value is None:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                return int(str(value))
            except Exception:
                return None

    def processAlgorithm(self, parameters, context, feedback):

        vertice = self.parameterAsSource(
            parameters,
            self.VERTICE,
            context
        )
        if vertice is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.VERTICE))
        limite = self.parameterAsSource(
            parameters,
            self.LIMITE,
            context
        )
        if limite is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.LIMITE))

        context.setInvalidGeometryCheck(QgsFeatureRequest.GeometryNoCheck)
        parcela = self.parameterAsSource(
            parameters,
            self.PARCELA,
            context
        )
        if parcela is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.PARCELA))

        output_path = self.parameterAsString(
            parameters,
            self.OUTPUT,
            context
        )
        if not output_path:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.OUTPUT))

        dec_coord = self.parameterAsInt(
            parameters,
            self.DEC_COORD,
            context
        )

        dec_prec = self.parameterAsInt(
            parameters,
            self.DEC_PREC,
            context
        )
        #path and create macro
        liboffice_path = "C:/Program Files/LibreOffice/program/"
        liboffice_exe = 'soffice.exe'
        path_libfile = os.path.join(liboffice_path, liboffice_exe)

        path_macro = os.path.join(Path.home(), "AppData/Roaming/LibreOffice/4/user/Scripts/python")
        if not os.path.isdir(path_macro): # verifica se diretorio ja existe
            os.makedirs(path_macro) # cria pasta caso nao exista
            feedback.pushInfo ('Pasta criada com sucesso para a macro!  {}'.format(path_macro))


        path_ods = os.path.join(Path.home(), "AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/Georondonia/algoritmos/shp/sigef_planilha_modelo_1.2_rc5.ods")
        shutil.copy(os.path.join(Path.home(),"AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/Georondonia/algoritmos/shp/macro.py"),os.path.join(path_macro,'qgis_macro.py'))

        # Validações

        # Checar preenchimento dos atributos da camada vértice
        self.vld_1(vertice)


        # Camada parcela deve ter apenas uma feição selecionada
        if parcela.featureCount() != 1:
            raise QgsProcessingException ('Camada parcela deve ter apenas uma feição selecionada!')
        else:
            feature = [feature for feature in parcela.getFeatures()][0]


        # Verificar se cada vértice da camada limite (linha) tem o correspondente da camada vétice (ponto)
        self.vld_2(limite,vertice)

        # Verificar se cada vértice da camada parcela (polígono) tem o correspondente da camada vétice (ponto)
        self.vld_3(parcela,vertice)
        
        # Construir macro - AQUI ESTÃO AS PRINCIPAIS MUDANÇAS
        nat_ser = {1:'Particular', 2:'Contrato com Administração Pública'}
        pessoa = {1:'Física', 2:'Jurídica'}
        situacao = {1:'Imóvel Registrado', 2:'Área Titulada não Registrada', 3:'Área não Titulada'}
        natureza = {1:'Assentamento',2:'Assentamento Parcela',3:'Estrada',4:'Ferrovia',5:'Floresta Pública',6:'Gleba Pública',7:'Particular',8:'Perímetro Urbano',9:'Terra Indígena',10:'Terreno de Marinha',11:'Terreno Marginal',12:'Território Quilombola',13:'Unidade de Conservação'}
        
        with open(os.path.join(path_macro,'qgis_macro.py'),'r') as arq:
            data = arq.read()
            
            # Extração segura de atributos para dicionários
            nat_serv_int = self.get_safe_int_attribute(feature, 'nat_serv')
            natureza_servico_str = nat_ser.get(nat_serv_int, '')
            data = data.replace("Natureza do serviço", natureza_servico_str)

            pessoa_int = self.get_safe_int_attribute(feature, 'pessoa')
            pessoa_str = pessoa.get(pessoa_int, '')
            data = data.replace("Tipo de pessoa", pessoa_str)
            
            situacao_int = self.get_safe_int_attribute(feature, 'situacao')
            situacao_str = situacao.get(situacao_int, '')
            data = data.replace("Situação", situacao_str)

            natureza_int = self.get_safe_int_attribute(feature, 'natureza')
            natureza_str = natureza.get(natureza_int, '')
            data = data.replace("Natureza da area", natureza_str)

            # Extração segura de atributos string para substituição direta
            data = data.replace("Nome", self.get_safe_string_attribute(feature, 'nome'))
            data = data.replace("CPF", self.get_safe_string_attribute(feature, 'cpf_cnpj'))
            data = data.replace("Denominação", self.get_safe_string_attribute(feature, 'denominacao'))
            data = data.replace("Codigo do Imovel", self.get_safe_string_attribute(feature, 'sncr'))
            data = data.replace("Codigo do cartorio", self.get_safe_string_attribute(feature, 'cod_cartorio'))
            data = data.replace("Matricula", self.get_safe_string_attribute(feature, 'matricula'))
            
            # Combinação de município e UF com extração segura
            municipio_val = self.get_safe_string_attribute(feature, 'municipio')
            uf_val = self.get_safe_string_attribute(feature, 'uf')
            municipio_completo = f"{municipio_val}-{uf_val}" if municipio_val and uf_val else municipio_val or uf_val
            
            # Trata o valor para a célula A17, pegando apenas o que vem antes do ';'
            municipio_a17 = municipio_completo.split(';')[0]
            data = data.replace("Municipio_A17", municipio_a17)
            data = data.replace("Municipio_B17", municipio_completo)
            
            
        geom = feature.geometry()
        if geom.isMultipart():
            polygons = geom.asMultiPolygon()
        else:
            polygons = [geom.asPolygon()]

        # A lógica de criar sheets é condicional aqui, mas o loop abaixo sempre espera 'polygons'.
        # Se 'len(polygons) != 1', a função createSheets é chamada.
        # Caso contrário (se len(polygons) == 1), createSheets não é chamada e a variável 'data'
        # manterá seu estado anterior, sem as modificações de #copy_sheet e #activate_sheet.
        # Isso pode gerar um erro se a macro esperar essas tags em todos os casos.
        # Para fins de demonstração, manterei a estrutura original.
        if len(polygons) != 1:
            data = self.createSheets(data,polygons)


        # createSpreadsheet
        denom_raw = self.get_safe_string_attribute(feature, 'denominacao')
        if isinstance(denom_raw, str) and ';' in denom_raw:
            denom_clean = denom_raw.split(';')[0].replace('"', '\\"').replace('\n', ' ')
        else:
            denom_clean = str(denom_raw).replace('"', '\\"').replace('\n', ' ')
        
        for n, pol in enumerate(polygons):
            pnt_str = ''
            sheet_idx = n + 1
            # Ativa a planilha perimetro_X e já define B3 e B4 conforme comentário desejado
            pnt_str += '\tdoc.activate("perimetro_{}")\n'.format(sheet_idx)
            pnt_str += '\tdoc.setValue("B3", "Parte {}")\n'.format(sheet_idx)
            pnt_str += '\tdoc.setValue("B4", "{:03d}")\n'.format(sheet_idx)
            
            pnt_body = ''
            # Aplica a reordenação dos pontos do polígono para padronizar o início
            reordered_polygon_points = self.reorder_polygon_points(pol[0])
            for k1, pnt in enumerate(reordered_polygon_points[:-1]):
                codigo,longitude,sigma_x,latitude,sigma_y,altitude, sigma_z,metodo_pos = self.vertice (pnt,vertice,dec_coord,dec_prec)
                pnt_seg = reordered_polygon_points[k1 + 1]
                try:
                    tipo,confrontan,cns,matricula = self.limite(pnt,pnt_seg,limite)
                except QgsProcessingException as e: # Captura a exceção específica levantada por self.limite
                    raise QgsProcessingException(f'Erro de topologia ao verificar limites para a feição parcela: {str(e)}')
                except Exception as e: # Captura outras exceções inesperadas
                    raise QgsProcessingException(f'Verifique possível erro de topologia na camada limite para o ponto ({pnt.y()}, {pnt.x()})! Detalhes: {e}')
                k = k1+12
                pnt_body +='\tdoc.setValue("A{}", "{}")\n'.format(k,codigo)
                pnt_body +='\tdoc.setValue("B{}", "{}")\n'.format(k,longitude)
                pnt_body +='\tdoc.setValue("C{}", "{}")\n'.format(k,sigma_x)
                pnt_body +='\tdoc.setValue("D{}", "{}")\n'.format(k,latitude)
                pnt_body +='\tdoc.setValue("E{}", "{}")\n'.format(k,sigma_y)
                pnt_body +='\tdoc.setValue("F{}", "{}")\n'.format(k,altitude)
                pnt_body +='\tdoc.setValue("G{}", "{}")\n'.format(k,sigma_z)
                pnt_body +='\tdoc.setValue("H{}", "{}")\n'.format(k,metodo_pos)
                pnt_body +='\tdoc.setValue("I{}", "{}")\n'.format(k,tipo)
                pnt_body +='\tdoc.setValue("J{}", "{}")\n'.format(k,cns)
                pnt_body +='\tdoc.setValue("K{}", "{}")\n'.format(k,matricula)
                pnt_body +='\tdoc.setValue("L{}", "{}")\n'.format(k,confrontan)
    
            pnt_str += pnt_body
            data = data.replace('#table_{}'.format(sheet_idx), pnt_str)

        data = data.replace('output_path', output_path)

        with open(os.path.join(path_macro,'qgis_macro.py'),'w') as arq:
            arq.write(data)

        #executa macro
        try:
            subprocess.call(f"{path_libfile} "
                         " --invisible "
                         f"{path_ods} "
                        'vnd.sun.star.script:qgis_macro.py$create_table?language=Python&location=user'
                        )
            # Seleciona o próximo lote
            self.selecionar_proximo()

        except Exception as e: # Captura a exceção para fornecer mais detalhes
            raise QgsProcessingException(f"Erro ao executar a macro do LibreOffice. Verifique se a versão do seu LibreOffice ou o seu SO estão atualizados e se o caminho '{path_libfile}' está correto! Detalhes: {e}")
        os.remove(os.path.join(path_macro,'qgis_macro.py'))

        # Mensagem de finalização
        feedback.reportError(f"\nODS Gerada com sucesso!!\n__________________\n\n>----FIM DO JOB!!----<\n__________________\n\n")
        
		# Retorna o caminho do arquivo de saída
        return {self.OUTPUT: output_path}

        

    def vld_1(self, vertice):
        for feat in vertice.getFeatures():
            id_feat = feat.id()
            sigma_x = feat['sigma_x']
            sigma_y = feat['sigma_y']
            sigma_z = feat['sigma_z']
            metodo_pos = feat['metodo_pos']
            tipo_verti = feat['tipo_verti']
            vert_code = str(feat['vertice']).strip()

            if sigma_x is None or not (0 <= sigma_x <= 10):
                raise QgsProcessingException(f'Erro no vértice {id_feat}: o valor de "sigma_x" ({sigma_x}) está fora do intervalo (0 a 10) ou é nulo!')
            if sigma_y is None or not (0 <= sigma_y <= 10):
                raise QgsProcessingException(f'Erro no vértice {id_feat}: o valor de "sigma_y" ({sigma_y}) está fora do intervalo (0 a 10) ou é nulo!')
            if sigma_z is None or not (0 <= sigma_z <= 10):
                raise QgsProcessingException(f'Erro no vértice {id_feat}: o valor de "sigma_z" ({sigma_z}) está fora do intervalo (0 a 10) ou é nulo!')
            if metodo_pos not in ('PG1', 'PG2', 'PG3', 'PG4', 'PG5', 'PG6', 'PG7', 'PG8', 'PG9', 'PT1', 'PT2', 'PT3', 'PT4', 'PT5', 'PT6', 'PT7', 'PT8', 'PT9', 'PA1', 'PA2', 'PA3', 'PS1', 'PS2', 'PS3', 'PS4', 'PB1', 'PB2'):
                raise QgsProcessingException(f'Erro no vértice {id_feat}: o "metodo_pos" ({metodo_pos}) é inválido! Verifique a lista de métodos permitidos.')
            if tipo_verti not in ('M', 'P', 'V'):
                raise QgsProcessingException(f'Erro no vértice {id_feat}: o "tipo_verti" ({tipo_verti}) é inválido! Deve ser "M", "P" ou "V".')
            if len(vert_code) < 7:
                raise QgsProcessingException(f'Erro no vértice {id_feat}: o "código do vértice" ("{vert_code}") deve ter ao menos 7 caracteres!')
            if vert_code in ('', 'NULL'):
                raise QgsProcessingException(f'Erro no vértice {id_feat}: o atributo "código do vértice" está vazio ou nulo!')

    def vld_2(self, limite, vertice):
        # Otimização: criar um set de pontos de vértice para busca mais rápida, uma única vez
        pontos_vertice = {f.geometry().asPoint() for f in vertice.getFeatures()}
        for feat1 in limite.getFeatures():
            id_feat1 = feat1.id()
            if feat1['tipo'] not in ('LA1', 'LA2', 'LA3', 'LA4', 'LA5', 'LA6', 'LA7', 'LN1', 'LN2', 'LN3', 'LN4', 'LN5', 'LN6'):
                raise QgsProcessingException(f'Erro na feição limite {id_feat1}: o atributo "tipo" ({feat1["tipo"]}) é inválido! Verifique a lista de tipos permitidos.')
            if len(str(feat1['confrontan']).strip()) < 3:
                raise QgsProcessingException(f'Erro na feição limite {id_feat1}: o atributo "confrontan" ("{feat1["confrontan"]}") deve ter ao menos 3 caracteres!')
            # Topologia
            linha = feat1.geometry().asPolyline()
            for pnt in linha:
                if pnt not in pontos_vertice:
                    raise QgsProcessingException(f'Erro na feição limite {id_feat1}: Ponto de coordenadas ({pnt.y()}, {pnt.x()}) da camada limite não possui correspondente na camada vértice!')

    def vld_3(self, parcela, vertice):
        # Otimização: criar um set de pontos de vértice para busca mais rápida, uma única vez
        pontos_vertice = {f.geometry().asPoint() for f in vertice.getFeatures()}
        for feat1 in parcela.getFeatures():
            id_feat1 = feat1.id()
            geom1 = feat1.geometry()
            if geom1.isMultipart():
                pols = geom1.asMultiPolygon()
            else:
                pols = [geom1.asPolygon()]
            for pol in pols:
                for pnt in pol[0]:
                    if pnt not in pontos_vertice:
                        raise QgsProcessingException(f'Erro na feição parcela {id_feat1}: Ponto de coordenadas ({pnt.y()}, {pnt.x()}) da camada parcela não possui correspondente na camada vértice!')

    def createSheets(self,data,pols):
        add_sheets = ''
        act_sheets = ''
        for i in range(len(pols)):
            if i!=0:
                add_sheets +='\tdoc.copySheet("perimetro_{}","perimetro_{}","sobre")\n'.format(i,i+1)
                act_sheets +='\tdoc.activate("perimetro_{}")\n'.format(i+1)
                act_sheets +='#table_{}\n'.format(i+1)
        data = data.replace('#copy_sheet',add_sheets)
        data = data.replace('#activate_sheet',act_sheets)
        return data


    def vertice (self,pnt,vertice,dec_coord,dec_prec):
        dec_prec = str(dec_prec)
        def dd2dms(dd, n_digits=3):
            if dd != 0:
                graus = int(floor(abs(dd)))
                resto = round(abs(dd) - graus, 10)
                minutos = int(floor(60*resto))
                resto = round(resto*60 - minutos, 10)
                segundos = resto*60
                if round(segundos,n_digits) == 60:
                    minutos += 1
                    segundos = 0
                if minutos == 60:
                    graus += 1
                    minutos = 0
                if dd < 0:
                    texto = '{:02d}'.format(graus) + ' '
                else:
                    texto = '{:02d}'.format(graus) + ' '
                texto = texto + '{:02d}'.format(minutos) + " "
                if n_digits < 1:
                    texto = texto + '{:02d}'.format(int(segundos)) + ' '
                else:
                    texto = texto + ('{:0' + str(3+n_digits) + '.' + str(n_digits) + 'f}').format(segundos) + ' '
                return texto.replace('.',',')
            else:
                texto = "00 00 " + ('{:0' + str(3+n_digits) + '.' + str(n_digits) + 'f}').format(0)
                return texto.replace('.',',')
        for feat in vertice.getFeatures():
            vert = feat.geometry().asPoint()
            if vert == pnt:
                codigo = str(feat['vertice']).strip().replace('\n','')
                longitude = dd2dms(vert.x(), dec_coord) + 'W'
                sigma_x = ('{:.'+ dec_prec + 'f}').format(feat['sigma_x']).replace('.',',')
                latitude = dd2dms(vert.y(), dec_coord) + 'S' if vert.y() < 0 else dd2dms(vert.y(), dec_coord) + 'N'
                sigma_y = ('{:.'+ dec_prec + 'f}').format(feat['sigma_y']).replace('.',',')
                z = float(feat.geometry().constGet().z())
                if str(z) != 'nan':
                    altitude = ('{:.'+ dec_prec + 'f}').format(z).replace('.',',')
                else:
                    altitude = '0,00'
                    QgsMessageLog.logMessage(f'Advertência: Ponto de código {codigo} (ID: {feat.id()}) está com altitude igual a 0 (zero). Verifique!', 'GeneratorOds', Qgis.Warning)
                sigma_z = ('{:.'+ dec_prec + 'f}').format(feat['sigma_z']).replace('.',',')
                metodo_pos = feat['metodo_pos']
                return codigo,longitude,sigma_x,latitude,sigma_y,altitude, sigma_z,metodo_pos
        # Se nenhum vértice correspondente for encontrado (o que não deveria acontecer se as validações passarem)
        raise QgsProcessingException(f'Erro interno: Não foi possível encontrar os dados do vértice para o ponto ({pnt.y()}, {pnt.x()}).')


    def limite (self,pnt,pnt_seg,limite):
        for feat in limite.getFeatures():
            linha = feat.geometry().asPolyline()
            for k2, vert in enumerate(linha[:-1]):
                vert_seg = linha[k2 + 1]
                if vert == pnt and vert_seg == pnt_seg:
                    tipo = feat['tipo']
                    confrontan = str(feat['confrontan']).strip().replace('\n','')
                    cns = str(feat['cns']).replace('NULL', '').strip().replace('\n','')
                    matricula = str(feat['matricula']).replace('NULL', '').strip().replace('\n','')

                    return tipo,confrontan,cns,matricula
        # Se nenhum limite correspondente for encontrado
        raise QgsProcessingException(f'Limite não encontrado para o segmento de ponto ({pnt.y()}, {pnt.x()}) para ({pnt_seg.y()}, {pnt_seg.x()}).')

    # Configuração básica de logging (apenas uma vez, geralmente fora da função)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Seleciona a próxima feição do    lote
    def selecionar_proximo(self):

        # Abrir camada vértice
        vertice = QgsProject.instance().mapLayersByName('vertice')[0]
        # Abrir camada limite
        limite = QgsProject.instance().mapLayersByName('limite')[0]
        # Abrir camada parcela
        parcela = QgsProject.instance().mapLayersByName('parcela')[0]

        # Iteração
        feitos = []

        # Obter os lotes
        lotes = [feat for feat in parcela.getFeatures()]

        # Ordenar os lotes pelo campo 'lote'
        lotes_ordenados = sorted(lotes, key=lambda feat: int(''.join(filter(str.isdigit, str(feat['lote'])))) if ''.join(filter(str.isdigit, str(feat['lote']))) else 0)

        # Identificar a seleção atual
        current_selection = parcela.selectedFeatures()
        current_lote_val = current_selection[0]['lote'] if current_selection else None
        current_lote = str(current_lote_val) if current_lote_val is not None else None

        # Encontrar o índice do lote atual
        if current_lote:
            current_index = next((i for i, feat in enumerate(lotes_ordenados) if str(feat['lote']) == current_lote), None)
        else:
            current_index = -1

        # Log do valor de current_lote
        if current_lote is not None:
            QgsMessageLog.logMessage(f"Tentando selecionar o próximo lote. Lote atual: {current_lote}", "MeuPlugin", Qgis.Info)

        # Selecionar o próximo lote
        if current_index is not None and current_index + 1 < len(lotes_ordenados):
            next_feat = lotes_ordenados[current_index + 1]
            lote = next_feat['lote']
            feitos.append(lote)

            # Selecionar a feição na camada parcela
            parcela.selectByIds([next_feat.id()])
            QgsMessageLog.logMessage(f"Lote '{lote}' selecionado na camada parcela.", "MeuPlugin", Qgis.Info)


            # Criar expressão para selecionar feições nas outras camadas
            expression = QgsExpression('"lote" = \'{}\''.format(lote))
            # Selecionar feições na camada vértice
            ids_selecionados_vertice = [f.id() for f in vertice.getFeatures(QgsFeatureRequest(expression))]
            vertice.selectByIds(ids_selecionados_vertice)
            QgsMessageLog.logMessage(f"{len(ids_selecionados_vertice)} vértices selecionados para o lote '{lote}'.", "MeuPlugin", Qgis.Info)


            # Selecionar feições na camada limite
            ids_selecionados_limite = [f.id() for f in limite.getFeatures(QgsFeatureRequest(expression))]
            limite.selectByIds(ids_selecionados_limite)
            QgsMessageLog.logMessage(f"{len(ids_selecionados_limite)} limites selecionados para o lote '{lote}'.", "MeuPlugin", Qgis.Info)
        else:
            QgsMessageLog.logMessage("Não há mais lotes para selecionar ou a seleção atual é o último lote.", "MeuPlugin", Qgis.Info)

    def reorder_polygon_points(self, pontos):
        """
        Reordena os pontos de um polígono para que o ponto inicial seja aquele com a maior latitude.
        Isso garante uma padronização na ordem dos vértices, útil para macros SIGEF.
        A lista 'pontos' deve representar um anel fechado (primeiro e último ponto iguais).
        """
        ponto_inicial = None
        max_latitude = -99999999  # Latitude mínima muito baixa para garantir que qualquer ponto seja maior

        # Procura o ponto com a maior latitude (exclui o último ponto duplicado se for o caso)
        for pnt in pontos[:-1]:
            if pnt.y() > max_latitude:
                max_latitude = pnt.y()
                ponto_inicial = pnt
        
        # Se nenhum ponto foi encontrado (polígono vazio ou inválido), retorna a lista original
        if ponto_inicial is None and pontos:
            return pontos
        elif ponto_inicial is None: # Se a lista de pontos está vazia
            return []

        # Encontra o índice do ponto inicial na lista original
        try:
            index = pontos.index(ponto_inicial)
        except ValueError:
            # Caso o ponto inicial não seja encontrado, pode indicar um problema com QgsPoint equality
            # ou um polígono malformado. Retorna a lista original para evitar quebrar.
            return pontos 
            
        # Reordena a lista de pontos para começar no ponto_inicial e manter a ordem cíclica
        # O resultado incluirá o ponto inicial no começo e no fim, fechando o polígono.
        # Ex: [A, B, C, D, A]. Se C é o ponto inicial (índice 2).
        # pontos[2:] -> [C, D, A]
        # pontos[1:2+1] -> pontos[1:3] -> [B, C]
        # Concatenação: [C, D, A, B, C]
        pontos_reordenados = pontos[index:] + pontos[1:index+1]
        return pontos_reordenados