# Problema 2 — Apartado 2.b: nombres de libres y recuperantes

El apartado 2.b genera una imagen con los recortes de Nombre y Apellido de los registros correctos cuya Condición Final es `L` (libre) o `R` (recupera). La lógica está dentro de `procesar_planilla` en [`validar_planilla.py`](../validar_planilla.py); la clasificación del carácter está en `clasificar_condicion`.

## Selección de registros

Primero se valida la fila completa con las reglas del apartado [2.a](apartado_2a.md). Solo se consideran las filas cuyos seis campos tienen estado `OK`. Por lo tanto, un nombre no aparece en el resultado si cualquiera de sus campos —legajo, nombre, un parcial o condición— incumple el formato esperado.

## Clasificación de la condición

El campo Condición Final se binariza con umbral inverso de 127. Se recorta el componente de tinta más grande para aislar el glifo. La función aplica una heurística específica para las letras mayúsculas de estas planillas; no es un OCR general:

1. Invierte el glifo, agrega un borde de fondo y cuenta los componentes del fondo con conectividad 4. El borde hace que el fondo exterior quede conectado.
2. Si no se detecta un agujero interior, clasifica el carácter como `L`.
3. Si hay un agujero, calcula la densidad de tinta del cuarto superior izquierdo. Si supera `0,4`, clasifica como `R`; si no, como `A`.

La regla se apoya en la forma de las letras previstas: `L` no tiene un agujero cerrado, mientras que `R` y `A` sí. La densidad superior izquierda busca separar la `R` de la `A` en las imágenes de entrada. El carácter `A` se reconoce internamente, pero no se incorpora a la imagen pedida para libres y recuperantes.

## Construcción de la imagen

Para cada fila correcta clasificada como `L` o `R`, se recorta la celda Nombre y Apellido. Se agrega un borde azul para `L` y rojo para `R`, y luego se apilan los recortes verticalmente. Como las celdas pueden tener anchos distintos, se completa cada una hasta el ancho máximo con un fondo gris claro antes de apilarla.

OpenCV representa los colores en orden BGR: azul `(255, 0, 0)` y rojo `(0, 0, 255)`. La salida se llama `grade_sheet_<id>_recortes_LR.png` y se guarda junto al CSV de esa planilla. Si no hay registros que cumplan simultáneamente todos los campos y tengan condición `L` o `R`, no se genera la imagen.

## Alcance y límites

El clasificador usa conectividad, presencia de agujeros y densidad en una región fija. No lee ni valida semánticamente el nombre ni los demás campos. Si la letra está deformada, cortada, unida a ruido o cambia de tamaño, el umbral o la heurística geométrica puede clasificarla mal. Los colores solo distinguen visualmente las dos categorías en la salida.

Para una planilla individual, el mismo comando de [2.a](apartado_2a.md) ejecuta también este apartado. Para todas las planillas en lote, véase [apartado 2.d](apartado_2d.md).
