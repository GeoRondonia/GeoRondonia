# geo-scripts
-----------------------------------------------------
## Expressões QGIS para checagem dados GeoRural:

### Verifica se Grade Leste tem Valores nulos
 `count_missing("Grade Leste (m)",group_by:="fid")`

 ### Verifica se a coluna nome tem dados duplicados
`count(expression:="Nome", group_by:="Nome") > 1` 

### Verifica se a xcoord e ycoord tem dados duplicados
`count(expression:="xcoord", group_by:="xcoord") > 1 OR count(expression:="ycoord", group_by:="ycoord") > 1`

-----------------------------------------------------