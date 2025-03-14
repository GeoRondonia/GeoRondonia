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
__revision__ = '$Format:%H$'

from qgis.PyQt.QtCore import QCoreApplication
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
					   QgsExpressionContext,
					   QgsProcessingParameterFileDestination)
from ..geocapt.imgs import Imgs
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

	def group(self):
		return self.tr('')

	def groupId(self):
		return ''

	def icon(self):
		return QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images/spreadsheet.png'))
	
	txt_en = '''Creates a SIGEF ODS spreadsheet, filling it directly through Macros, from the GeoRural database layers worked in QGIS'''
	txt_pt = '''Cria uma planilha ODS do SIGEF, preenchendo-a diretamente através de Macros, a partir das camadas do banco de dados GeoRural trabalhado no QGIS.'''
	
	figure1 =  'images\illustration\ods-gods.png'
	figure2 = 'images\modelo-logos-parcerias-geo.png'
	
	
	def shortHelpString(self):
		social_BW = Imgs().social_BW
		footer = '''<div style="text-align: right;">
					  
                      <img src="'''+ os.path.join(os.path.dirname(os.path.dirname(__file__)),self.figure1) +'''"><br>
					  <img src="'''+ os.path.join(os.path.dirname(os.path.dirname(__file__)),self.figure2) +'''">
                      </div>
                      <div align="right">
                      <p align="right">
					  <b>'''+self.tr('Author: Maik Rodrigues, Leandro França, Tiago Prudencio, Valdir Moura, Ranieli dos Anjos, Mychelle Novais and Carolina Potratz', 'Autor: Maik Rodrigues, Leandro França, Tiago Prudencio, Valdir Moura, Ranieli dos Anjos, Mychelle Novais e Carolina Potratz')+'''</b>
                      </p>'''+ social_BW + '''</div>
                    </div>'''
		return self.tr(self.txt_en, self.txt_pt) + footer
	
	def initAlgorithm(self, config=None):

		self.addParameter(
			QgsProcessingParameterFeatureSource(
				self.VERTICE,
				self.tr('Camada Vertice'),
				[QgsProcessing.TypeVectorPoint]
			)
		)

		self.addParameter(
			QgsProcessingParameterFeatureSource(
				self.LIMITE,
				self.tr('Camada Limite'),
				[QgsProcessing.TypeVectorLine]
			)
		)

		self.addParameter(
			QgsProcessingParameterFeatureSource(
				self.PARCELA,
				self.tr('Camada Parcela'),
				[QgsProcessing.TypeVectorPolygon]
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

		path_macro = os.path.join(Path.home(), "AppData\\Roaming\\LibreOffice\\4\\user\\Scripts\\python")
		if not os.path.isdir(path_macro): # verifica se diretorio ja existe
			os.makedirs(path_macro) # cria pasta caso nao exista
			feedback.pushInfo ('Pasta criada com sucesso para a macro!  {}'.format(path_macro))


		path_ods = os.path.join(Path.home(), "AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\Georondonia\\algoritmos\\shp\\sigef_planilha_modelo_1.2_rc5.ods")
		shutil.copy(os.path.join(Path.home(),"AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\Georondonia\\algoritmos\\shp\\macro.py"),os.path.join(path_macro,'qgis_macro.py'))
		
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

		# construir macro
		nat_ser = {1:'Particular', 2:'Contrato com Administração Pública'}
		pessoa, situacao  = {1:'Física', 2:'Jurídica'}, {1:'Imóvel Registrado', 2:'Área Titulada não Registrada', 3:'Área não Titulada'}
		natureza = {1:'Assentamento',2:'Assentamento Parcela',3:'Estrada',4:'Ferrovia',5:'Floresta Pública',6:'Gleba Pública',7:'Particular',8:'Perímetro Urbano',9:'Terra Indígena',10:'Terreno de Marinha',11:'Terreno Marginal',12:'Território Quilombola',13:'Unidade de Conservação'}

		with open(os.path.join(path_macro,'qgis_macro.py'),'r') as arq:
			data = arq.read()
			data = data.replace("Natureza do serviço", nat_ser[feature['nat_serv']] if feature['nat_serv'] in nat_ser else '')
			data = data.replace("Tipo de pessoa", pessoa[feature['pessoa']] if feature['pessoa'] in pessoa else '')
					
			data = data.replace("Nome",str(feature['nome']).replace('NULL', '').replace('\n',''))
			data = data.replace("CPF",str(feature['cpf_cnpj']).replace('NULL', '').replace('\n',''))
			data = data.replace("Denominação",str(feature['denominacao']).replace('NULL', '').replace('\n',''))
			data = data.replace("Situação", situacao[feature['situacao']] if feature['situacao'] in situacao else '')
			data = data.replace("Natureza da area", natureza[feature['natureza']] if feature['natureza'] in natureza else '')
			data = data.replace("Codigo do Imovel", str(feature['sncr']).replace('NULL', '').replace('\n',''))
			data = data.replace("Codigo do cartorio", str(feature['cod_cartorio']).replace('NULL', '').replace('\n',''))
			data = data.replace("Matricula",str(feature['matricula']).replace('NULL', '').replace('\n',''))
			municipio = str(feature['municipio']).replace('NULL', '').replace('\n','') +'-'+ str(feature['uf']).replace('NULL', '').replace('\n','')
			data = data.replace("Municipio", municipio)

		geom = feature.geometry()
		if geom.isMultipart():
			polygons = geom.asMultiPolygon()
		else:
			polygons = [geom.asPolygon()]

		if len(polygons) != 1:
			data = self.createSheets(data,polygons)



		# createSpreadshee

		for n, pol in enumerate(polygons):
			pnt_str = ''
			for k1, pnt in enumerate(pol[0][:-1]):
				codigo,longitude,sigma_x,latitude,sigma_y,altitude, sigma_z,metodo_pos = self.vertice (pnt,vertice,dec_coord,dec_prec)
				pnt_seg = pol[0][k1 + 1]
				try:
					tipo,confrontan,cns,matricula = self.limite(pnt,pnt_seg,limite)
				except:
					raise QgsProcessingException ('Verifique possível erro de topologia!')
				k = k1+12
				pnt_str +='\tdoc.setValue("A{}", "{}")\n'.format(k,codigo)
				pnt_str +='\tdoc.setValue("B{}", "{}")\n'.format(k,longitude)
				pnt_str +='\tdoc.setValue("C{}", "{}")\n'.format(k,sigma_x)
				pnt_str +='\tdoc.setValue("D{}", "{}")\n'.format(k,latitude)
				pnt_str +='\tdoc.setValue("E{}", "{}")\n'.format(k,sigma_y)
				pnt_str +='\tdoc.setValue("F{}", "{}")\n'.format(k,altitude)
				pnt_str +='\tdoc.setValue("G{}", "{}")\n'.format(k,sigma_z)
				pnt_str +='\tdoc.setValue("H{}", "{}")\n'.format(k,metodo_pos)
				pnt_str +='\tdoc.setValue("I{}", "{}")\n'.format(k,tipo)
				pnt_str +='\tdoc.setValue("J{}", "{}")\n'.format(k,cns)
				pnt_str +='\tdoc.setValue("K{}", "{}")\n'.format(k,matricula)
				pnt_str +='\tdoc.setValue("L{}", "{}")\n'.format(k,confrontan)



			data = data.replace('#table_{}'.format(n+1),pnt_str)
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
		
		except:
			raise QgsProcessingException("Verifique se a versão do seu LibreOffice ou o seu SO estão atualizados!")
		os.remove(os.path.join(path_macro,'qgis_macro.py'))
		
		# Mensagem de finalização
		feedback.reportError(f"\nODS Gerada com sucesso!!\n__________________\n\n>----FIM DO JOB!!----<\n__________________\n\n")
		feedback.reportError(f"{output_path}")						
		
		return {}

	def vld_1(self,vertice):
		for feat in vertice.getFeatures():
			if feat['sigma_x'] < 0 or feat['sigma_x'] > 10 or feat['sigma_x'] == None:
				raise QgsProcessingException ('Verifique os valores do atrituto "sigma_x"!')
			if feat['sigma_y'] < 0 or feat['sigma_y'] > 10 or feat['sigma_y'] == None:
				raise QgsProcessingException ('Verifique os valores do atrituto "sigma_y"!')
			if feat['sigma_z'] < 0 or feat['sigma_z'] > 10 or feat['sigma_z'] == None:
				raise QgsProcessingException ('Verifique os valores do atrituto "sigma_z"!')
			if feat['metodo_pos'] not in ('PG1', 'PG2', 'PG3', 'PG4', 'PG5', 'PG6', 'PG7', 'PG8', 'PG9', 'PT1', 'PT2', 'PT3', 'PT4', 'PT5', 'PT6', 'PT7', 'PT8', 'PT9', 'PA1', 'PA2', 'PA3', 'PS1', 'PS2', 'PS3', 'PS4', 'PB1', 'PB2'):
				raise QgsProcessingException ('Verifique os valores do atrituto "metodo_pos"!')
			if feat['tipo_verti'] not in ('M', 'P', 'V'):
				raise QgsProcessingException ('Verifique os valores do atrituto "tipo_vertice"!')
			if len(str(feat['vertice'])) < 7:
				raise QgsProcessingException ('Verifique os valores do atrituto "código do vértice"!')
			if str(feat['vertice']) in ('', ' ', 'NULL'):
				raise QgsProcessingException ('O atrituto "código do vértice" deve ser preenchido!')

	def vld_2(self,limite,vertice):
		for feat1 in limite.getFeatures():
			# Checar preenchimento dos atributos
			if feat1['tipo'] not in ('LA1', 'LA2', 'LA3', 'LA4', 'LA5', 'LA6', 'LA7', 'LN1', 'LN2', 'LN3', 'LN4', 'LN5', 'LN6'):
				raise QgsProcessingException ('Verifique os valores do atributo "tipo"!')
			if len(feat1['confrontan']) < 3:
				raise QgsProcessingException ('Verifique os valores do atrituto "confrontante"!')
			# Topologia
			linha = feat1.geometry().asPolyline()
			for pnt in linha:
				corresp = False
				for feat2 in vertice.getFeatures():
					vert = feat2.geometry().asPoint()
					if vert == pnt:
						corresp = True
						continue
				if not corresp:
					raise QgsProcessingException('Ponto de coordenadas ({}, {}) da camada limite não possui correspondente na camada vértice!'.format(pnt.y(), pnt.x()))

	def vld_3(self,parcela,vertice):
		for feat1 in parcela.getFeatures():
			geom1 = feat1.geometry()
			if geom1.isMultipart():
				pols = geom1.asMultiPolygon()
			else:
				pols = [geom1.asPolygon()]
			for pol in pols:
				for pnt in pol[0]:
					corresp = False
					for feat2 in vertice.getFeatures():
						vert = feat2.geometry().asPoint()
						if vert == pnt:
							corresp = True
							continue
					if not corresp:
						raise QgsProcessingException('Ponto de coordenadas ({}, {}) da camada parcela não possui correspondente na camada vértice!'.format(pnt.y(), pnt.x()))

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
		# dec_coord = str(dec_coord)
		# expr1 = QgsExpression("to_dms($y, 'y', {}, 'aligned')".format(dec_coord))
		# expr2 = QgsExpression("to_dms($x, 'x', {}, 'aligned')".format(dec_coord))
		# context = QgsExpressionContext()
		# context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(vertice))
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
			# context.setFeature(feat)
			vert = feat.geometry().asPoint()
			if vert == pnt:
				codigo = feat['vertice'].replace('\n','')
				#longitude = str(expr2.evaluate(context)).replace("°"," ").replace("′"," ").replace('″',' ')
				longitude = dd2dms(vert.x(), dec_coord) + 'W'
				#longitude = longitude.replace("°"," ").replace("'"," ").replace('"',' ')
				sigma_x = ('{:.'+ dec_prec + 'f}').format(feat['sigma_x']).replace('.',',')
				#latitude = str(expr1.evaluate(context)).replace("°"," ").replace("′"," ").replace('″',' ')
				latitude = dd2dms(vert.y(), dec_coord) + 'S' if vert.y() < 0 else dd2dms(vert.y(), 3) + 'N'
				#latitude = latitude.replace("°"," ").replace("'"," ").replace('"',' ')
				sigma_y = ('{:.'+ dec_prec + 'f}').format(feat['sigma_y']).replace('.',',')
				z = float(feat.geometry().constGet().z())
				if str(z) != 'nan':
					altitude = ('{:.'+ dec_prec + 'f}').format(z).replace('.',',')
				else:
					altitude = '0,00'
					feedback.pushInfo('Advertência: Ponto de código {} está com altitude igual a 0 (zero). Verifique!'.format(codigo))
				sigma_z = ('{:.'+ dec_prec + 'f}').format(feat['sigma_z']).replace('.',',')
				metodo_pos = feat['metodo_pos']
				return codigo,longitude,sigma_x,latitude,sigma_y,altitude, sigma_z,metodo_pos

	def limite (self,pnt,pnt_seg,limite):
		
		for feat in limite.getFeatures():
			linha = feat.geometry().asPolyline()
			for k2, vert in enumerate(linha[:-1]):
				vert_seg = linha[k2 + 1]
				if vert == pnt and vert_seg == pnt_seg:
					tipo = feat['tipo']
					confrontan = feat['confrontan'].replace('\n','')
					cns = str(feat['cns']).replace('NULL', '').replace('\n','')
					matricula = str(feat['matricula']).replace('NULL', '').replace('\n','')

					return tipo,confrontan,cns,matricula
    # Configuração básica de logging (apenas uma vez, geralmente fora da função)
	logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

	# Seleciona a próxima feição do	lote
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
		lotes_ordenados = sorted(lotes, key=lambda feat: int(''.join(filter(str.isdigit, feat['lote']))) if ''.join(filter(str.isdigit, feat['lote'])) else 0)

        # Identificar a seleção atual
		current_selection = parcela.selectedFeatures()
		current_lote = current_selection[0]['lote'] if current_selection else None

        # Encontrar o índice do lote atual
		if current_lote:
			current_index = next((i for i, feat in enumerate(lotes_ordenados) if feat['lote'] == current_lote), None)
		else:
			current_index = -1

		# AQUI	

		# Log e print do valor de current_lote
		if current_lote is not None:
			QgsMessageLog.logMessage("Esta é uma mensagem informativa", "MeuPlugin", Qgis.Info)
			QgsMessageLog.logMessage("Este é um aviso", "MeuPlugin", Qgis.Warning)
			QgsMessageLog.logMessage("Esta é uma mensagem crítica", "MeuPlugin", Qgis.Critical)

        # Selecionar o próximo lote
		if current_index is not None and current_index + 1 < len(lotes_ordenados):
			next_feat = lotes_ordenados[current_index + 1]
			lote = next_feat['lote']
			feitos.append(lote)
			
            # Selecionar a feição na camada parcela
			parcela.selectByIds([next_feat.id()])

            # Criar expressão para selecionar feições nas outras camadas
			expression = QgsExpression('"lote" = \'{}\''.format(lote))

            # Selecionar feições na camada vértice
			ids_selecionados_vertice = [f.id() for f in vertice.getFeatures(QgsFeatureRequest(expression))]
			vertice.selectByIds(ids_selecionados_vertice)

            # Selecionar feições na camada limite
			ids_selecionados_limite = [f.id() for f in limite.getFeatures(QgsFeatureRequest(expression))]
			limite.selectByIds(ids_selecionados_limite)
