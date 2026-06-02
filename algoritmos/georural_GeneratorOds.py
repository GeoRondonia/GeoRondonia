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
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFeatureSource,
                       QgsFeatureRequest,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFileDestination,
                       QgsVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsMessageLog,
                       Qgis,
                       QgsGeometry
                       )
# Assuming geocapt.imgs is available in the environment
# from ..geocapt.imgs import Imgs # This might need adjustment based on package structure
import logging
from math import floor
from qgis.PyQt.QtGui import QIcon
import subprocess
import os
import platform
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
    VER_Z = 'VER_Z'
    SEL_PROXIMO = 'SEL_PROXIMO'
    VAL_COMPLETA = 'VAL_COMPLETA'

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
            QgsProcessingParameterBoolean(
                self.VER_Z,
                self.tr('Verificar preenchimento de cota Z'),
                defaultValue = True
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SEL_PROXIMO,
                self.tr('Selecionar próxima parcela'),
                defaultValue = True
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.VAL_COMPLETA,
                self.tr('Validar projeto completo (Se desmarcado, valida apenas a parcela atual selecionada)'),
                defaultValue = False
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

    def vld_0(self, vertice, limite, parcela):
        if parcela is None or parcela.featureCount() != 1:
            raise QgsProcessingException('A camada Parcela deve conter exatamente uma feição selecionada!')
        if vertice is None or vertice.featureCount() == 0:
            raise QgsProcessingException('A camada Vértice não pode estar vazia!')
        if limite is None or limite.featureCount() == 0:
            raise QgsProcessingException('A camada Limite não pode estar vazia!')

    def vld_z(self, vertice, parcela_geom=None):
        ids_problematicos = []
        ids_null = []
        msgs = []
        if parcela_geom:
            request = QgsFeatureRequest().setFilterRect(parcela_geom.boundingBox())
            features = [f for f in vertice.getFeatures(request) if f.geometry() and not f.geometry().isEmpty() and f.geometry().touches(parcela_geom)]
        else:
            features = [f for f in vertice.getFeatures() if f.geometry() and not f.geometry().isEmpty()]

        # Detectar vértices com geometria nula
        if parcela_geom:
            request = QgsFeatureRequest().setFilterRect(parcela_geom.boundingBox())
            all_features = [f for f in vertice.getFeatures(request) if f.geometry().touches(parcela_geom)]
        else:
            all_features = list(vertice.getFeatures())

        for f in all_features:
            if not f.geometry() or f.geometry().isEmpty():
                ids_null.append(f.id())

        if ids_null:
            layers = QgsProject.instance().mapLayersByName('vertice')
            if layers:
                layers[0].selectByIds(ids_null)
            raise QgsProcessingException(
                f'Erro: Encontradas {len(ids_null)} feição(ões) com geometria nula na camada vértice '
                f'(feições selecionadas na tabela de atributos). IDs: {ids_null}'
            )

        for feat1 in features:
            z_value = feat1.attribute('Z')
            if z_value is None or z_value == '' or z_value == 'NULL':
                ids_problematicos.append(feat1.id())
                msgs.append('  • Feição id {}: Cota Z não preenchida ou igual a zero!'.format(feat1.id()))
            else:
                try:
                    z = float(z_value)
                    if z == 0:
                        ids_problematicos.append(feat1.id())
                        msgs.append('  • Feição id {}: Cota Z não preenchida ou igual a zero!'.format(feat1.id()))
                    elif z > 3000 or z < -10:
                        ids_problematicos.append(feat1.id())
                        msgs.append('  • Feição id {}: Cota Z ({}) fora dos limites permitidos (-10 a 3000 m)!'.format(feat1.id(), z))
                except (ValueError, TypeError):
                    ids_problematicos.append(feat1.id())
                    msgs.append('  • Feição id {}: Cota Z inválida!'.format(feat1.id()))

        if ids_problematicos:
            layers = QgsProject.instance().mapLayersByName('vertice')
            if layers:
                layers[0].selectByIds(ids_problematicos)
            raise QgsProcessingException(
                'Problemas encontrados na Cota Z em {} feição(ões) da camada Vértice '
                '(feições selecionadas na tabela de atributos):\n{}'.format(
                    len(ids_problematicos), '\n'.join(msgs)
                )
            )

    def vld_1(self, vertice, parcela_geom=None):
        ids_null = []
        if parcela_geom:
            request = QgsFeatureRequest().setFilterRect(parcela_geom.boundingBox())
            all_features = list(vertice.getFeatures(request))
            features = [f for f in all_features if f.geometry() and not f.geometry().isEmpty() and f.geometry().touches(parcela_geom)]
        else:
            all_features = list(vertice.getFeatures())
            features = [f for f in all_features if f.geometry() and not f.geometry().isEmpty()]

        # Detectar vértices com geometria nula
        for f in all_features:
            if not f.geometry() or f.geometry().isEmpty():
                ids_null.append(f.id())

        if ids_null:
            layers = QgsProject.instance().mapLayersByName('vertice')
            if layers:
                layers[0].selectByIds(ids_null)
            raise QgsProcessingException(
                f'Erro: Encontradas {len(ids_null)} feição(ões) com geometria nula na camada vértice '
                f'(feições selecionadas na tabela de atributos). IDs: {ids_null}'
            )

        for feat in features:
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

    def vld_2(self, limite, vertice, parcela_geom=None):
        ids_null_limite = []
        if parcela_geom:
            req_v = QgsFeatureRequest().setFilterRect(parcela_geom.boundingBox())
            features_v = [f for f in vertice.getFeatures(req_v) if f.geometry() and not f.geometry().isEmpty() and f.geometry().touches(parcela_geom)]
            req_l = QgsFeatureRequest().setFilterRect(parcela_geom.boundingBox())
            all_limite = list(limite.getFeatures(req_l))
            features_limite = [f for f in all_limite if f.geometry() and not f.geometry().isEmpty() and f.geometry().touches(parcela_geom)]
        else:
            features_v = [f for f in vertice.getFeatures() if f.geometry() and not f.geometry().isEmpty()]
            all_limite = list(limite.getFeatures())
            features_limite = [f for f in all_limite if f.geometry() and not f.geometry().isEmpty()]

        # Detectar limites com geometria nula
        if parcela_geom:
            for f in all_limite:
                if not f.geometry() or f.geometry().isEmpty():
                    ids_null_limite.append(f.id())
        else:
            for f in all_limite:
                if not f.geometry() or f.geometry().isEmpty():
                    ids_null_limite.append(f.id())

        if ids_null_limite:
            layers = QgsProject.instance().mapLayersByName('limite')
            if layers:
                layers[0].selectByIds(ids_null_limite)
            raise QgsProcessingException(
                f'Erro: Encontradas {len(ids_null_limite)} feição(ões) com geometria nula na camada limite '
                f'(feições selecionadas na tabela de atributos). IDs: {ids_null_limite}'
            )

        pontos_vertice = {f.geometry().asPoint() for f in features_v}
        for feat1 in features_limite:
            id_feat1 = feat1.id()
            if feat1['tipo'] not in ('LA1', 'LA2', 'LA3', 'LA4', 'LA5', 'LA6', 'LA7', 'LN1', 'LN2', 'LN3', 'LN4', 'LN5', 'LN6'):
                raise QgsProcessingException(f'Erro na feição limite {id_feat1}: o atributo "tipo" ({feat1["tipo"]}) é inválido! Verifique a lista de tipos permitidos.')
            confrontan = feat1['confrontan']
            if not confrontan or len(str(confrontan).strip()) < 3:
                raise QgsProcessingException(f'Erro na feição limite {id_feat1}: o atributo "confrontan" ("{confrontan}") deve ter ao menos 3 caracteres ou está vazio/nulo!')
            linha = feat1.geometry().asPolyline()
            for pnt in linha:
                # Ao validar uma parcela específica, valida apenas pontos que tocam a parcela
                if parcela_geom:
                    pnt_geom = QgsGeometry.fromPointXY(pnt)
                    if pnt_geom.touches(parcela_geom) and pnt not in pontos_vertice:
                        raise QgsProcessingException(f'Erro na feição limite {id_feat1}: Ponto de coordenadas ({pnt.y()}, {pnt.x()}) da camada limite não possui correspondente na camada vértice!')
                else:
                    # Ao validar tudo, valida todos os pontos
                    if pnt not in pontos_vertice:
                        raise QgsProcessingException(f'Erro na feição limite {id_feat1}: Ponto de coordenadas ({pnt.y()}, {pnt.x()}) da camada limite não possui correspondente na camada vértice!')

    def vld_3(self, parcela, vertice, parcela_geom=None):
        ids_null = []
        pontos_vertice = {}

        # Se validando uma parcela específica, considerar apenas vértices que tocam a parcela
        if parcela_geom:
            request = QgsFeatureRequest().setFilterRect(parcela_geom.boundingBox())
            features_v = [f for f in vertice.getFeatures(request) if f.geometry() and not f.geometry().isEmpty() and f.geometry().touches(parcela_geom)]
        else:
            features_v = [f for f in vertice.getFeatures() if f.geometry() and not f.geometry().isEmpty()]

        # Detectar vértices com geometria nula
        if parcela_geom:
            request = QgsFeatureRequest().setFilterRect(parcela_geom.boundingBox())
            all_features = [f for f in vertice.getFeatures(request) if f.geometry().touches(parcela_geom)]
        else:
            all_features = list(vertice.getFeatures())

        for f in all_features:
            if not f.geometry() or f.geometry().isEmpty():
                ids_null.append(f.id())

        if ids_null:
            layers = QgsProject.instance().mapLayersByName('vertice')
            if layers:
                layers[0].selectByIds(ids_null)
            raise QgsProcessingException(
                f'Erro: Encontradas {len(ids_null)} feição(ões) com geometria nula na camada vértice '
                f'(feições selecionadas na tabela de atributos). IDs: {ids_null}'
            )

        for f in features_v:
            geom = f.geometry()
            pontos_vertice[geom.asPoint()] = f.id()

        for feat1 in parcela.getFeatures():
            id_feat1 = feat1.id()
            geom1 = feat1.geometry()
            if geom1.isMultipart():
                pols = geom1.asMultiPolygon()
            else:
                pols = [geom1.asPolygon()]
            for pol in pols:
                for pnt in pol[0]:
                    # Ao validar uma parcela específica, valida apenas pontos que tocam a parcela
                    if parcela_geom:
                        pnt_geom = QgsGeometry.fromPointXY(pnt)
                        if pnt_geom.touches(parcela_geom) and pnt not in pontos_vertice:
                            raise QgsProcessingException(f'Erro na feição parcela {id_feat1}: Ponto de coordenadas ({pnt.y()}, {pnt.x()}) da camada parcela não possui correspondente na camada vértice!')
                    else:
                        # Ao validar tudo, valida todos os pontos
                        if pnt not in pontos_vertice:
                            raise QgsProcessingException(f'Erro na feição parcela {id_feat1}: Ponto de coordenadas ({pnt.y()}, {pnt.x()}) da camada parcela não possui correspondente na camada vértice!')



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

        ver_z = self.parameterAsBool(
            parameters,
            self.VER_Z,
            context
        )

        sel_proximo = self.parameterAsBool(
            parameters,
            self.SEL_PROXIMO,
            context
        )

        val_completa = self.parameterAsBool(
            parameters,
            self.VAL_COMPLETA,
            context
        )

        #path and create macro
        # Detectando o sistema operacional
        system_os = platform.system()

        # Definição de caminhos para LibreOffice
        if system_os == "Windows":
            libreoffice_path = Path("C:/Program Files/LibreOffice/program/soffice.exe")
        elif system_os == "Linux":
            libreoffice_path = Path("/usr/bin/soffice")
        elif system_os == "Darwin":  # macOS
            libreoffice_path = Path("/Applications/LibreOffice.app/Contents/MacOS/soffice")
        else:
            raise QgsProcessingException("Sistema operacional não suportado")
        path_libfile = str(libreoffice_path)

        # Definição de caminho para macros e ODS no LibreOffice
        if system_os == "Windows":
            path_macro = Path.home() / "AppData/Roaming/LibreOffice/4/user/Scripts/python"
            src_macro = Path.home() / "AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/Georondonia/algoritmos/shp/macro.py"
            path_ods = Path.home() / "AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/Georondonia/algoritmos/shp/sigef_planilha_modelo_1.2_rc5.ods"
        elif system_os == "Darwin":  # macOS
            path_macro = Path.home() / "Library/Application Support/LibreOffice/4/user/Scripts/python"
            src_macro = Path.home() / "Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/Georondonia/algoritmos/shp/macro.py"
            path_ods = Path.home() / "Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/Georondonia/algoritmos/shp/sigef_planilha_modelo_1.2_rc5.ods"
        else:  # Linux e outros
            path_macro = Path.home() / ".config/libreoffice/4/user/Scripts/python"
            src_macro = Path.home() / ".config/QGIS/QGIS3/profiles/default/python/plugins/Georondonia/algoritmos/shp/macro.py"
            path_ods = Path.home() / ".config/QGIS/QGIS3/profiles/default/python/plugins/Georondonia/algoritmos/shp/sigef_planilha_modelo_1.2_rc5.ods"

        # Criando diretório, se não existir
        path_macro.mkdir(parents=True, exist_ok=True)

        # Copiando macro do QGIS para LibreOffice
        dst_macro = path_macro / 'qgis_macro.py'
        shutil.copy(src_macro, dst_macro)

        # Extrair geometria da parcela selecionada para validações filtradas por localização
        feature = next(parcela.getFeatures())
        parcela_geom = None if val_completa else feature.geometry()

        # Validações
        self.vld_0(vertice, limite, parcela)
        self.vld_1(vertice, parcela_geom)
        self.vld_2(limite, vertice, parcela_geom)
        self.vld_3(parcela, vertice, parcela_geom)
        if ver_z:
            self.vld_z(vertice, parcela_geom)
        
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
        polygons = geom.asMultiPolygon() if geom.isMultipart() else [geom.asPolygon()]

        # Mapeia anéis externos e internos (ilhas) por polígono - portado do ODS_LEANDRO
        mapping = {0: []}
        for i, features in enumerate(polygons):
            mapping[0].append(self.reorder_polygon_points(features[0]))
            reorder = [self.reorder_polygon_points(feat) for feat in features[1:]]
            if reorder:
                mapping[i + 1] = reorder

        data = self.createSheets(mapping, data)

        # Escreve os dados de cada sheet com numeração linear (#table_1, #table_2, ...)
        sheet_num = 0
        for feat in mapping[0]:
            sheet_num += 1
            pnt_str = self.generate_table_substitution(feat, vertice, limite, dec_coord, dec_prec)
            data = data.replace('#table_{}'.format(sheet_num), pnt_str)

        for parcela_idx, features in list(mapping.items())[1:]:
            for feat in features:
                sheet_num += 1
                pnt_str = self.generate_table_substitution(feat, vertice, limite, dec_coord, dec_prec)
                data = data.replace('#table_{}'.format(sheet_num), pnt_str)

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
            # Seleção automática do próximo lote (vértices, limites e parcela)
            # Executado APÓS o subprocess para não interferir com parameterAsSource
            self.selecionar_por_parcela(feedback)
            if sel_proximo:
                self.selecionar_proximo()

        except Exception as e: # Captura a exceção para fornecer mais detalhes
            raise QgsProcessingException(f"Erro ao executar a macro do LibreOffice. Verifique se a versão do seu LibreOffice ou o seu SO estão atualizados e se o caminho '{path_libfile}' está correto! Detalhes: {e}")
        os.remove(os.path.join(path_macro,'qgis_macro.py'))

        # Mensagem de finalização
        feedback.reportError(f"\nODS Gerada com sucesso!!\n__________________\n\n>----FIM DO JOB!!----<\n__________________\n\n")
        
		# Retorna o caminho do arquivo de saída
        return {self.OUTPUT: output_path}

        


    def createSheets(self, mapping, data):
        """
        Cria sheets adicionais para múltiplos polígonos (multipart) e anéis internos (ilhas).
        Usa os marcadores #copy_sheet e #activate_sheet do template macro.py do GeoRondonia.
        O primeiro sheet (perimetro_1 / #table_1) já existe no template, os demais são criados aqui.
        """
        add_str = ''
        act_str = ''
        sheet_num = 1  # perimetro_1 já existe

        # Outer rings adicionais (multipolygon com mais de 1 polígono)
        for i in range(1, len(mapping[0])):
            sheet_num += 1
            add_str += '\tdoc.copySheet("perimetro_1", "perimetro_{}", "sobre")\n'.format(sheet_num)
            act_str += '\tdoc.activate("perimetro_{}")\n'.format(sheet_num)
            act_str += '\tdoc.setValue("B3", "Parte {}")\n'.format(sheet_num)
            act_str += '\tdoc.setValue("B4", "{:03d}")\n'.format(sheet_num)
            act_str += '#table_{}\n'.format(sheet_num)

        # Anéis internos (ilhas) de cada polígono
        for parcela_idx, features in list(mapping.items())[1:]:
            for feat in features:
                sheet_num += 1
                add_str += '\tdoc.copySheet("perimetro_1", "perimetro_{}", "sobre")\n'.format(sheet_num)
                act_str += '\tdoc.activate("perimetro_{}")\n'.format(sheet_num)
                act_str += '\tdoc.setValue("B3", "Parte {} - Interno")\n'.format(sheet_num)
                act_str += '\tdoc.setValue("B4", "{:03d}")\n'.format(sheet_num)
                act_str += '#table_{}\n'.format(sheet_num)

        data = data.replace('#copy_sheet', add_str)
        data = data.replace('#activate_sheet', act_str)
        return data

    def generate_table_substitution(self, feat, vertice, limite, dec_coord, dec_prec):
        """Gera o bloco de doc.setValue para cada ponto do polígono."""
        pnt_str = []
        for k1, pnt in enumerate(feat[:-1]):
            codigo, longitude, sigma_x, latitude, sigma_y, altitude, sigma_z, metodo_pos = self.vertice(pnt, vertice, dec_coord, dec_prec)
            pnt_seg = feat[k1 + 1]
            try:
                tipo, confrontan, cns, matricula = self.limite(pnt, pnt_seg, limite)
            except QgsProcessingException as e:
                raise QgsProcessingException(f'Erro de topologia ao verificar limites: {str(e)}')
            except Exception as e:
                raise QgsProcessingException(f'Verifique possível erro de topologia na camada limite para o ponto ({pnt.y()}, {pnt.x()})! Detalhes: {e}')
            row = k1 + 12
            values = [codigo, longitude, sigma_x, latitude, sigma_y, altitude, sigma_z, metodo_pos, tipo, cns, matricula, confrontan]
            pnt_str.append(self.format_doc_values(row, values))
        return "\n".join(pnt_str)

    def format_doc_values(self, k, values):
        fields = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
        return "\n".join(f'\tdoc.setValue("{fields[i]}{k}", "{value}")' for i, value in enumerate(values))


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
                z_value = feat['Z']
                if z_value is None or z_value == '' or str(z_value).strip() == 'NULL':
                    altitude = '0,00'
                    QgsMessageLog.logMessage(f'Advertência: Ponto de código {codigo} (ID: {feat.id()}) está com altitude igual a 0 (zero). Verifique!', 'GeneratorOds', Qgis.Warning)
                else:
                    try:
                        z = float(z_value)
                        altitude = ('{:.'+ dec_prec + 'f}').format(z).replace('.',',')
                    except (ValueError, TypeError):
                        altitude = '0,00'
                        QgsMessageLog.logMessage(f'Advertência: Ponto de código {codigo} (ID: {feat.id()}) tem altitude inválida. Verifique!', 'GeneratorOds', Qgis.Warning)
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

    def selecionar_por_parcela(self, feedback=None):
        """
        Com base na feição de parcela selecionada no projeto, seleciona automaticamente
        os vértices e limites correspondentes por localização espacial (touches).
        Isso permite que o usuário selecione apenas a parcela e rode o algoritmo
        com 'Apenas feições selecionadas' ativo nas 3 camadas.
        """
        layers_parcela = QgsProject.instance().mapLayersByName('parcela')
        layers_vertice = QgsProject.instance().mapLayersByName('vertice')
        layers_limite  = QgsProject.instance().mapLayersByName('limite')

        if not layers_parcela or not layers_vertice or not layers_limite:
            if feedback:
                feedback.pushInfo('Auto-seleção ignorada: uma ou mais camadas (parcela/vertice/limite) não foram encontradas no projeto.')
            return

        parcela_layer = layers_parcela[0]
        vertice_layer = layers_vertice[0]
        limite_layer  = layers_limite[0]

        selected = parcela_layer.selectedFeatures()
        if not selected:
            if feedback:
                feedback.pushInfo('Auto-seleção ignorada: nenhuma feição selecionada na camada parcela.')
            return

        parcela_geom = selected[0].geometry()

        # Usa blockSignals para suprimir sinais Qt (selectionChanged etc.) durante os selectByIds.
        # Isso evita que o QTimer de refresh do canvas seja agendado enquanto os dados ainda
        # estão sendo preparados para parameterAsSource, prevenindo o access violation.
        vertice_layer.blockSignals(True)
        limite_layer.blockSignals(True)
        try:
            # Seleciona vértices por localização espacial
            request_v = QgsFeatureRequest().setFilterRect(parcela_geom.boundingBox())
            ids_vertice = [f.id() for f in vertice_layer.getFeatures(request_v)
                           if f.geometry().touches(parcela_geom)]
            vertice_layer.selectByIds(ids_vertice)
            msg_v = f'{len(ids_vertice)} vértices selecionados automaticamente por localização.'
            QgsMessageLog.logMessage(msg_v, 'GeneratorOds', Qgis.Info)
            if feedback:
                feedback.pushInfo(msg_v)

            # Seleciona limites por localização espacial
            request_l = QgsFeatureRequest().setFilterRect(parcela_geom.boundingBox())
            ids_limite = [f.id() for f in limite_layer.getFeatures(request_l)
                          if f.geometry().touches(parcela_geom)]
            limite_layer.selectByIds(ids_limite)
            msg_l = f'{len(ids_limite)} limites selecionados automaticamente por localização.'
            QgsMessageLog.logMessage(msg_l, 'GeneratorOds', Qgis.Info)
            if feedback:
                feedback.pushInfo(msg_l)
        finally:
            # Restaura sinais e atualiza o canvas uma única vez ao final
            vertice_layer.blockSignals(False)
            limite_layer.blockSignals(False)
            vertice_layer.triggerRepaint()
            limite_layer.triggerRepaint()

    # Seleciona a próxima feição do lote
    def selecionar_proximo(self):

        # Abrir camada vértice
        vertice = QgsProject.instance().mapLayersByName('vertice')[0]
        # Abrir camada limite
        limite = QgsProject.instance().mapLayersByName('limite')[0]
        # Abrir camada parcela
        parcela = QgsProject.instance().mapLayersByName('parcela')[0]

        # Obter todas as parcelas
        todas_parcelas = list(parcela.getFeatures())

        # Identificar a parcela selecionada atualmente
        current_selection = parcela.selectedFeatures()
        if not current_selection:
            QgsMessageLog.logMessage("Nenhuma parcela selecionada.", "MeuPlugin", Qgis.Warning)
            return

        current_feat = current_selection[0]
        current_id = current_feat.id()

        # Encontrar o índice da parcela atual
        current_index = next((i for i, feat in enumerate(todas_parcelas) if feat.id() == current_id), -1)

        if current_index == -1:
            QgsMessageLog.logMessage("Parcela selecionada não encontrada.", "MeuPlugin", Qgis.Warning)
            return

        # Selecionar a próxima parcela
        if current_index + 1 < len(todas_parcelas):
            next_feat = todas_parcelas[current_index + 1]
            next_id = next_feat.id()

            # Selecionar a feição na camada parcela
            parcela.selectByIds([next_id])
            QgsMessageLog.logMessage(f"Parcela ID '{next_id}' selecionada.", "MeuPlugin", Qgis.Info)

            # Selecionar feições nas outras camadas por localização espacial
            next_geom = next_feat.geometry()

            # Selecionar feições na camada vértice por localização
            request_v = QgsFeatureRequest().setFilterRect(next_geom.boundingBox())
            ids_selecionados_vertice = [f.id() for f in vertice.getFeatures(request_v)
                                        if f.geometry().touches(next_geom)]
            vertice.selectByIds(ids_selecionados_vertice)
            QgsMessageLog.logMessage(f"{len(ids_selecionados_vertice)} vértices selecionados por localização.", "MeuPlugin", Qgis.Info)

            # Selecionar feições na camada limite por localização
            request_l = QgsFeatureRequest().setFilterRect(next_geom.boundingBox())
            ids_selecionados_limite = [f.id() for f in limite.getFeatures(request_l)
                                       if f.geometry().touches(next_geom)]
            limite.selectByIds(ids_selecionados_limite)
            QgsMessageLog.logMessage(f"{len(ids_selecionados_limite)} limites selecionados por localização.", "MeuPlugin", Qgis.Info)
        else:
            QgsMessageLog.logMessage("Não há mais parcelas para selecionar. Você está na última parcela.", "MeuPlugin", Qgis.Info)

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