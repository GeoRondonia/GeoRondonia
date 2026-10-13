<!-- PROJECT LOGO -->
<p align="center">
  <a href="https://georondonia.ifro.edu.br">
    <img src="images/logo-geo_original.png" alt="Logo" width="90" height="75">
  </a>
  <h3 align="center">GeoRondônia</h3>
  <p align="center">
    <b><i>Ferramentas para Georreferenciamento de imóveis rurais em Projetos de Assentamentos ou Projetos Fundiários, desenvolvido em parceria com o projeto georondonia, baseado no Manual Técnico para Georreferenciamento de Imóveis Rurais atualizado, do Instituto Nacional de Colonização e Reforma Agrária (INCRA)</i><b>
    <br />
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Conteúdo</summary>
  <ol>
      <li>
      <a href="#%EF%B8%8F-ferramentas-do-plugin">Ferramentas do Plugin</a>
      <ul>
      <li>
      <a href="#%EF%B8%8F-gerador-de-ods-gods">Gerador de ODS (GODS)</a>
      </li>
      </ul>
      <ul>
      <li>
      <a href="#%EF%B8%8F-validação-de-geometrias">Validação de Geometrias</a>
      </li>
      <li>
      <a href="#%EF%B8%8F-prepara-kml-para-o-car-cadastro-ambiental-rural">Prepara KML para o CAR</a>
      </li>
      </ul>
      <a href="#créditos">Créditos</a>
      </li>
      <li>
      <a href="#desenvolvedores">Desenvolvedores</a>
      </li>
      <li>
      <a href="#colaboradores">Colaboradores</a>
      </li>   
      <li>
      <a href="#ferramentas-base">Ferramentas Base</a>
      </li>
      <li>
      <a href="#conheça-mais-sobre-o-georondônia">Conheça mais sobre o GeoRondônia</a>
      </li>
      </ol>
</details>


## 🛠️ Ferramentas do Plugin


### ⚙️ Gerador de ODS (GODS)
A ferramenta descrita automatiza a criação da planilha ODS do SIGEF para georreferenciamento de imóveis rurais, integrando-se diretamente ao QGIS e ao banco de dados GeoRural. Ela utiliza macros para preencher a planilha ODS com dados extraídos das camadas do GeoRural trabalhadas no QGIS.

#### Processo de Seleção e Geração de Lotes (Atualizado)
#### Primeiro Lote:
* Selecione a parcela desejada.
* Escolha o limite apropriado.
* Defina o vértice necessário.
* Gere o lote com base nessas seleções.
#### Lotes Seguintes (automáticos):
Após a criação do primeiro lote, o sistema assume o controle:
* Parcela, limites e vértices são identificados e selecionados automaticamente em sequência de numeração dos lotes.
* Não é necessário repetir o processo manualmente de seleção.

Este processo simplifica a geração de múltiplos lotes, economizando tempo e reduzindo a possibilidade de erros na seleção manual.

#### Exemplo de Uso:

[![Gerador de ODS (GODS)](https://img.youtube.com/vi/NoDfbDumCag/0.jpg)](https://www.youtube.com/watch?v=NoDfbDumCag)

## Banco de Dados GeoRural:

Este modelo de dados pode ser implementado em banco de dados GeoPackage, PostGIS, ou atém mesmo no formato Shapefile, embora este último seja desaconselhado, por estar entrando em desuso.
O GeoRural é um modelo extremamente simples, de fácil entendimento e utilização. Ele consiste nas camadas: “vertice”, “limite” e “parcela”, contando também com camadas auxiliares para armazenar o histórico dos georreferenciamentos executados anteriormente, facilitando consultas e geração de relatórios.


### Classe Vértice:
É todo ponto onde a linha limítrofe do imóvel muda de direção ou onde existe interseção desta linha com qualquer outra linha limítrofe de imóveis contíguos ou servidões de passagem (INCRA, 2010).
<div align="center">
<p class="MsoNormal" style="text-align: center;"
 align="center">Tabela 1: Atributos
da camada v&eacute;rtice<o:p></o:p></p>
<div align="center">
<table class="MsoNormalTable" style="" border="0"
 cellpadding="0">
  <tbody>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: rgb(221, 221, 221) none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><b><span
 style="background: rgb(221, 221, 221) none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;"><b>Item</b>&nbsp;</span></b><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: rgb(221, 221, 221) none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><b><span
 style="background: rgb(221, 221, 221) none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">Nome&nbsp;</span></b><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: rgb(221, 221, 221) none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><b><span
 style="background: rgb(221, 221, 221) none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">Tipo&nbsp;</span></b><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: rgb(221, 221, 221) none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><b><span
 style="background: rgb(221, 221, 221) none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">Dom&iacute;nio</span></b><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">1</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">sigma_x&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">REAL&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">2</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">sigma_y&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">REAL&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">3</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">sigma_z&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">REAL&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">4</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">indice&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">INT&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">5</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">metodo_pos&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT(4)&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">PG1,
PG2, PG3, PG4, PG5, PG6, PG7, PG8, PG9, PT1, PT2, PT3, PT4, PT5, PT6,
PT7, PT8, PA1, PA2, PS1, PS2, PS3, PS4</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">6</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">tipo_verti&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT(4)&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">M,
P, V</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">7</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">vertice&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT(12)&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">8</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">qrcode&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT(40)&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
  </tbody>
</table>
</div>
<p class="MsoNormal"><o:p>&nbsp;</o:p></p>
</div>

### Classe Limite
Os limites são linhas que definem as confrontações, seja pelo tipo de confrontação ou pelo próprio confrontante.
<div align="center">
<p class="MsoNormal" style="text-align: center;"
 align="center">Tabela 2: Atributos
da camada limite<o:p></o:p></p>
<div align="center">
<table class="MsoNormalTable" style="" border="0"
 cellpadding="0">
  <tbody>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: rgb(221, 221, 221) none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><b><span
 style="background: rgb(221, 221, 221) none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">Item</span></b><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: rgb(221, 221, 221) none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><b><span
 style="background: rgb(221, 221, 221) none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">Nome&nbsp;</span></b><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: rgb(221, 221, 221) none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><b><span
 style="background: rgb(221, 221, 221) none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">Tipo&nbsp;</span></b><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: rgb(221, 221, 221) none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><b><span
 style="background: rgb(221, 221, 221) none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">Dom&iacute;nio&nbsp;</span></b><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">1</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">tipo&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT(4)&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">LA1,
LA2, LA3, LA4, LA5, LA6, LA7, LN1, LN2, LN3, LN4, LN5, LN6</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">2</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">confrontan&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT(254)&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">3</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">cns&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT(200)&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">4</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">matricula&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT(100)&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">5</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">qrcode&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT(40)&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
  </tbody>
</table>
</div>
<p class="MsoNormal"><o:p>&nbsp;</o:p></p>
</div>

### Classe Parcela
Representação planimétrica do imóvel levantado através de uma geometria do tipo polígono.
<div align="center">
<p class="MsoNormal" style="text-align: center;"
 align="center">Tabela 3: Atributos
da camada parcela<o:p></o:p></p>
<div align="center">
<table class="MsoNormalTable" style="" border="0"
 cellpadding="0">
  <tbody>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: rgb(221, 221, 221) none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><b><span
 style="background: rgb(221, 221, 221) none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">Item&nbsp;</span></b><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: rgb(221, 221, 221) none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><b><span
 style="background: rgb(221, 221, 221) none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">Nome&nbsp;</span></b><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: rgb(221, 221, 221) none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><b><span
 style="background: rgb(221, 221, 221) none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">Tipo&nbsp;</span></b><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: rgb(221, 221, 221) none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><b><span
 style="background: rgb(221, 221, 221) none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">Dom&iacute;nio&nbsp;</span></b><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">1</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">nome&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT(254)&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">2</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">nat_serv&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">INT&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">1
&ndash; Particular</span><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">2
&ndash; Contrato com Adm P&uacute;blica</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">3</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">pessoa&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">INT&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">1
&ndash; F&iacute;sica</span><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">2
&ndash; Jur&iacute;dica</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">4</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">cpf_cnpj&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT(20)&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">5</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">denominacao&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">6</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">situacao&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">INT&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="left"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
          <p>1 - Imóvel Registrado</p>
          <p>2 - Área Titulada não Registrada</p>
          <p>3 - Área não Titulada</p>
          </span><span style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">7</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">natureza&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">INT&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">1
- Im&oacute;vel Registrado</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">2
- &Aacute;rea Titulada n&atilde;o Registrada</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">3
- &Aacute;rea n&atilde;o Titulada</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">1
- Assentamento</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">2
- Assentamento Parcela</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">3
- Estrada</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">4
- Ferrovia</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">5
- Floresta P&uacute;blica</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">6
- Gleba P&uacute;blica</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">7
- Particular</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">8
- Per&iacute;metro Urbano</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">9
- Terra Ind&iacute;gena</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">10
- Terreno de Marinha</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">11
- Terreno Marginal</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">12
- Territ&oacute;rio Quilombola</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">13
- Unidade de Conserva&ccedil;&atilde;o</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">8</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">sncr&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT(20)&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">9</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">matricula&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT(50)&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">10</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">cod_cartorio&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT(30)&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">11</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">data&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">DATE&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">12</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">qrcode&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT(40)&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">-</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">13</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">municipio&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">Munic&iacute;pios
do Brasil (IBGE)</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">14</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">uf&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; line-height: normal;"><span
 style="background: whitesmoke none repeat scroll 0%; font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">TEXT&nbsp;</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
      <td
 style="padding: 0cm 7.5pt; background: whitesmoke none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;">
      <p class="MsoNormal"
 style="margin-bottom: 0cm; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif; color: black;">UFs
(IBGE)</span><span
 style="font-size: 12pt; font-family: &quot;Times New Roman&quot;,serif;"><o:p></o:p></span></p>
      </td>
    </tr>
  </tbody>
</table>
</div>
<p class="MsoNormal"><o:p>&nbsp;</o:p></p>
</div>
Observação: Também podem ser utilizadas as camadas “hist_vertice”, “hist_limite” e “hist_parcela” para armazenamento dos dados de georreferenciamento anteriores e, assim, manter o histórico de todos os trabalhos, possibilitando a consulta dos códigos anteriores, análises e relatórios de desempenho.
<br>

https://user-images.githubusercontent.com/88212377/161396633-24f01f9c-a15b-46c8-84db-c4a6acd49a27.mp4


### ⚙️ Validação de Geometrias

#### Descrição
Este plugin para QGIS oferece uma ferramenta eficiente para validar geometrias em camadas vetoriais. Ele é essencial para garantir a integridade dos dados geoespaciais em seus projetos.

#### Funcionalidades Principais
1. Verificação de Geometrias Inválidas
   
O plugin analisa todas as feições em uma camada vetorial selecionada, identificando e selecionando aquelas com geometrias inválidas na tabela de atributos.

<img src="https://i.postimg.cc/y6t61TZx/Check-Invalid-Geometry1.jpg" alt="CheckInvalidGeometry" width="850" height="auto">

Imagem 1: Projeto aberto: Seleção de geometrias invalidas

#### 2. Relatório Detalhado
Após a análise, o plugin gera um relatório na tela de log, listando:

* Todas as feições inválidas encontradas
* A quantidade total de geometrias inválidas
* O ID de cada feição com problema
  
<img src="https://i.postimg.cc/wvMKnFh9/Check-Invalid-Geometry2.jpg" alt="CheckInvalidGeometry" width="850" height="auto">

Imagem 2: Exemplo de relatório na tela de log

#### 3. Detecção de Geometrias "Fantasmas" 👻

Um diferencial único deste plugin é a capacidade de identificar geometrias "fantasmas". Estas são entradas na tabela de atributos que não possuem uma geometria associada, um problema comum mas frequentemente negligenciado em dados geoespaciais.

<img src="https://i.postimg.cc/h4pyTCr4/Check-Invalid-Geometry3.jpg" alt="CheckInvalidGeometry" width="850" height="auto">

Imagem 3: Exemplo de geometrias "fantasmas" detectadas na tabela de atributo

**Tratamento de Geometrias "Fantasmas**

Se o projeto contiver geometrias "fantasmas" (registros na tabela de atributos sem geometria associada), recomenda-se sua remoção para prevenir problemas futuros. Estas entradas podem ser eliminadas diretamente da tabela de atributos, seguindo estas etapas:

* Abra a tabela de atributos da camada em questão.

* Ative o modo de edição.

* Selecione as geometrias "fantasmas" identificadas pelo plugin.

* Use a função "Deletar feições selecionadas" para removê-las.

* Salve as edições e desative o modo de edição.

Esta limpeza ajuda a manter a integridade dos dados e evita erros em análises espaciais posteriores.

### ⚙️ Prepara KML para o CAR (Cadastro Ambiental Rural)
Este plugin permite exportar as feições selecionadas para o formato KML, visando a sua utilização no **Cadastro Ambiental Rural (CAR)**. Ele filtra os dados com base em uma camada de máscara (perímetro) e suporta geometrias de **ponto, linha e polígono**, garantindo a compatibilidade com o padrão WGS84 (EPSG:4326).

#### Funcionalidades Principais
* **Seleção por Perímetro :** Exporta apenas feições dentro da camada de entrada (máscara).
* **Suporte a Geometrias :** Mantém a integridade de pontos, linhas e polígonos durante a exportação.
* **Exportação Automática :** Gera arquivos KML prontos para uso em mapas online e ferramentas GIS.

#### Como Usar



1 - **Marque as Camadas de Sobreposição :** 

1. No "Painel de Camadas" do QGIS, marque o checkbox ✅ apenas nas camadas que você deseja incluir na exportação para KML.
2. Deixe a camada de entrada selecionada (a camada onde os lotes estão divididos).
3. Para definir o perímetro que deseja exportar, escolha uma camada poligonal para servir como máscara (Seleção em amarelo na imagem) e certifique-se de que ela esteja corretamente configurada para delimitar as feições.

<img src="https://github.com/user-attachments/assets/04da3b0c-5530-41eb-92b9-8a1b7762288d" width="850" height="auto">


2 - **Abra o plugin "Prepara KML para o CAR** 
1. Selecione a Camada de Entrada (Mascara), essa é a camada onde os poligonos estão divididos.
2. Selecione a coluna onde estão os nomes dos lotes. Esses nomes iram sair nos arquivos extraidos facilitando a identificação das camadas. 
3. Escolha a pasta de destino ou deixe na padrão mesmo.
4. "Executar" para iniciar a exportação das camadas.

<img src="https://github.com/user-attachments/assets/9618bc4a-347a-4f09-b7c2-72ab34809f5e" width="850" height="auto" >

#### Conclusão
Com essa ferramenta, você pode facilmente exportar suas feições do QGIS para KML, tornando mais simples a visualização e o compartilhamento de dados geoespaciais em diferentes plataformas.

----

## Créditos

Este projeto foi desenvolvido com a colaboração de diversos desenvolvedores e inspirado em ferramentas criadas por terceiros. Gostaríamos de expressar nossos sinceros agradecimentos a todos os envolvidos.


## Ferramentas Base:
Este plugin utiliza ou foi inspirado pelas seguintes ferramentas:

* [GeoINCRA](https://github.com/OpenGeoOne/GeoINCRA)
* [GeoCAR](https://github.com/OpenGeoOne/GeoCAR)


## Colaboradores:
Os seguintes colaboradores contribuíram diretamente para o desenvolvimento de funcionalidades específicas ou forneceram feedbacks valiosos:

<table>
  <tr>
    <td align="center">
      <a href="https://www.linkedin.com/in/valdir-moura-181a7b14/" title="Valdir">
        <img src="https://github.com/user-attachments/assets/4459a4e2-9938-4a6a-961e-e13573779b7d" width="100px;" alt="Valdir"/><br>
        <sub>
          <b>Valdir Moura</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://www.linkedin.com/in/ranieli-dos-anjos-de-souza-5a291b32" title="Raniele">
        <img src="https://github.com/user-attachments/assets/a70b31ab-37af-434d-9b18-4121d6f951dc" width="100px;" alt="Raniele"/><br>
        <sub>
          <b>Ranieli dos Anjos</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://www.linkedin.com/in/mychelle-novais" title="Mychelle">
        <img src="https://github.com/user-attachments/assets/6e76bfad-ed6c-41de-8b42-fd4920bcc124" width="100px;" alt="Mychelle"/><br>
        <sub>
          <b>Mychelle Novais</b>
        </sub>
      </a>
    </td>
     <td align="center">
      <a href="https://www.linkedin.com/in/carolina-potratz-giraldello" title="Carol">
        <img src="https://github.com/user-attachments/assets/fee2be2b-7ac7-4db8-bf86-7cc5d9900664" width="86px;" alt="Carol"/><br>
        <sub>
          <b>Carolina Potratz</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

<table>
<td align="center">
      <a href="https://www.linkedin.com/in/choroburaklein/" title="Ivan Chorobura">
        <img src="https://github.com/user-attachments/assets/7f7ba5ae-84de-43f7-8a49-3fa129b51f37" width="110px;" alt="Ivan Chorobura"/><br>
        <sub>
          <b>Ivan Chorobura</b>
        </sub>
      </a>
    </td>
     <td align="center">
      <a href="https://www.linkedin.com/in/%C3%ADsisnascimento/" title="Isis">
        <img src="https://github.com/user-attachments/assets/95399a33-99c1-4c88-a1e7-698f00ee52ca" width="110px;" alt="Isis"/><br>
        <sub>
          <b>Isis Nascimento</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://www.linkedin.com/in/jo%C3%A3o-vitor-ebeling-de-oliveira-259b132b1/" title="João">
        <img src="https://github.com/user-attachments/assets/a1df4705-72c9-4fb9-a095-e58399e78e22" width="110px;" alt="João"/><br>
        <sub>
          <b>João Vitor Ebeling</b>
        </sub>
      </a>
    </td>
  <td align="center">
      <a href="https://www.linkedin.com/in/rafaela-braga-silva-2427671b9" title="Rafaela">
        <img src="https://github.com/user-attachments/assets/ea9fa53c-b117-4707-b3dd-09f8b3977abe" width="110px;" alt="Rafaela"/><br>
        <sub>
          <b>Rafaela Braga</b>
        </sub>
      </a>
    </td>
   <td align="center">
      <a href="https://www.linkedin.com/in/alisson-pereira-amorim-734a7125a" title="Alisson">
        <img src="https://github.com/user-attachments/assets/f1dd9af6-10df-493c-b956-37c6e8ce81ca" width="110px;" alt="Alisson"/><br>
        <sub>
          <b>Alisson Amorim</b>
        </sub>
      </a>
    </td>
</table>

<table>
 <tr>
    <td align="center">
      <a href="https://www.linkedin.com/company/geoone/" title="GeoOne">
        <img src="https://i.postimg.cc/hvj3b9Dr/geoone-logo.jpg" width="110px;" alt="GeoOne"/><br>
        <sub>
          <b>GeoOne</b>
        </sub>
      </a>
    </td>    
</table>



## Desenvolvedores:

<b>Maik Rodrigues</b>
<div style="text-align: center;"><a
 href="https://www.linkedin.com/in/maikrodriguess/"><img
 style="border: 0px solid ;width: 40px" alt="GeoRonônia no QGIS"
 title="Maik Rodrigues"
 src="https://user-images.githubusercontent.com/25651083/178389727-7cf09fab-1c8f-4184-b80d-3a698de7c1be.png"></a>
  
<br>


<b>Bárbara Laura</b>
<div style="text-align: center;"><a
 href="https://www.linkedin.com/in/barbara-laura-tavares"><img
 style="border: 0px solid ;width: 40px" alt="GeoRonônia no QGIS"
 title="Bárbara Laura"
 src="https://user-images.githubusercontent.com/25651083/178389727-7cf09fab-1c8f-4184-b80d-3a698de7c1be.png"></a>
<br>

## Conheça mais sobre o GeoRondônia:

<div style="display: flex; justify-content: center; align-items: center;">
  <a href="http://georondonia.ifro.edu.br/">
    <img style="width: 40px; margin: 0 10px;" alt="GeoRonônia no QGIS" title="GeoRondônia-Portal" src="https://github.com/user-attachments/assets/5006adec-8fb8-4faa-8c54-4c738a8b04dc">
  </a>
  <a href="https://www.youtube.com/@GeorondoniaOficial">
    <img style="width: 40px; margin: 0 10px;" alt="GeoRonônia no QGIS" title="GeoRondônia-Youtube" src="https://github.com/user-attachments/assets/52d3c727-f93d-47c3-8ec4-b1564ae92a1c">
  </a>
  <a href="https://www.instagram.com/projetogeorondonia/">
    <img style="width: 40px; margin: 0 10px;" alt="GeoRonônia no QGIS" title="GeoRondônia-Instagram" src="https://github.com/user-attachments/assets/f7100cdd-fa9f-4e9e-a396-6d50f558b3f8">
  </a>
</div>

---
<p align="center">
  <a href="https://georondonia.ifro.edu.br/">
    <img src="https://github.com/user-attachments/assets/2fc22e6f-8ec0-455c-b924-6e769b1d8f3b" alt="incra-ifro" width="350" height="66">
  </a>
</p>
