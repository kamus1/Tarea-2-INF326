# Discusión de Arquitectura y Trade-offs

## BONUS
Para asegurar la unicidad de los id de los registros se pueden utilizar identificadores con offsets unicos por nodos, es decir: 

`id = offset_inicial + offset_nodo + (contador_local * salto)`

Donde salto = 10^n y n es el número de dígitos que corresponden al offset del nodo.

Esta solución tiene la ventaja de no requerir comunicación entre los nodos, con la desventaja de que limita el número máximo de nodos que soporta el sistema (10^n nodos).
