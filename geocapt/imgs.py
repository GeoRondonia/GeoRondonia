# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
__author__ = 'Leandro França e Maik Rodrigues de Souza'
__date__ = '2021-03-01'
__copyright__ = '(C) 2021, Leandro França e Maik Rodrigues de Souza'

import math, os, base64, PIL.Image
from math import atan, pi, sqrt, floor
from .assets import dic_color, geo_logo, lftools_logo

# Imagem para HTML
def img2html(path_file):
    arq = open(path_file, 'rb')
    leitura = arq.read()
    arq.close()
    encoded = base64.b64encode(leitura)
    texto = str(encoded)[2:-1]
    return texto

# Redimensionar Imagem
def ImgResize(path_file, lado, resized):
    caminho, arquivo = os.path.split(path_file)
    img = PIL.Image.open(path_file)
    altura = img.size[1]
    largura = img.size[0]
    if largura < altura:
        new_height = lado
        new_width =int(lado/float(altura)*largura)
    else:
        new_width = lado
        new_height =int(lado/float(largura)*altura)

    img = img.resize((new_width, new_height))
    path_file_reduced = os.path.join(caminho, resized)
    img.save(path_file_reduced)
    del img
    return path_file_reduced

# Imagem para HTML redimensionada
def img2html_resized(path_file, lado=500, resized = 'reduzido.jpg'):
    if os.path.isfile(path_file):
        caminho, arquivo = os.path.split(path_file)
        path_file_reduced = ImgResize(path_file, lado, resized)
        texto = img2html(path_file_reduced)
        os.remove(path_file_reduced)
        return texto
    else:
        return ''


# Repeated variables
class Imgs:
    social_BW = '''<a target="_blank" rel="noopener noreferrer" href="https://georondonia.ifro.edu.br/"><img title="GeoRondônia" src="data:image/png;base64,'''+geo_logo+'''"></a> <a target="_blank" rel="noopener noreferrer" href="https://www.youtube.com/@GeorondoniaOficial"><img title="Youtube" src="data:image/png;base64,'''+dic_color['youtube']+'''"></a> <a target="_blank" rel="noopener noreferrer" href="https://www.facebook.com/georondonia/"><img title="Facebook" src="data:image/png;base64,'''+dic_color['face']+'''"></a> <a target="_blank" rel="noopener noreferrer" href="https://www.instagram.com/projetogeorondonia/"><img title="Instagram" src="data:image/png;base64,''' + dic_color['instagram'] + '''"></a>'''

    social_table_color = '''<table style="text-align: right;" border="0"
     cellpadding="2" cellspacing="2">
      <tbody>
        <tr>
          <td><a target="_blank" rel="noopener noreferrer" href="https://georondonia.ifro.edu.br/">
          <img title="GeoRondônia" style="border: 0px solid ; width: 28px; height: 28px;" alt="udemy"
           src="data:image/png;base64,'''+geo_logo +'''">
           </a>
          </td>
          <td><a target="_blank" rel="noopener noreferrer" href="https://www.youtube.com/@GeorondoniaOficial">
          <img title="Youtube" style="border: 0px solid ; width: 28px; height: 28px;" alt="youtube"
           src="data:image/png;base64,'''+dic_color['youtube']+'''">
           </a>
          </td>
          <td><a target="_blank" rel="noopener noreferrer" href="https://www.facebook.com/georondonia/">
          <img title="Facebook" style="border: 0px solid ; width: 28px; height: 28px;" alt="facebook"
           src="data:image/png;base64,'''+dic_color['face']+'''">
           </a>
          </td>
          <td><a target="_blank" rel="noopener noreferrer" href="https://www.instagram.com/projetogeorondonia/">
          <img title="Linkedin" style="border: 0px solid ; width: 28px; height: 28px;" alt="linkedin"
           src="data:image/png;base64,'''+dic_color['instagram']+'''">
          </a>
          </td>
          </tr>
      </tbody>
    </table>'''

