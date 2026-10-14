# Referencias de la cátedra para los problemas 1 y 2

Se adjuntan el [enunciado original](fuentes/TUIA_PDI_TP1_2026_C2.pdf) y los nueve PDF originales de la carpeta `Catedra`, sin modificarlos. La tabla resume los contenidos de cátedra consultados; los números corresponden a las páginas del PDF, contando desde 1.

| Contenido utilizado | Fuente | Páginas |
| --- | --- | --- |
| Ventana local, actualización del píxel central y recorrido de toda la imagen | Enunciado del TP1 | 1 |
| Agregado de bordes con `cv2.copyMakeBorder` y `cv2.BORDER_REPLICATE` | Enunciado del TP1 | 1, AYUDA |
| Imagen como matriz de filas y columnas | [Presentación de PowerPoint2.pdf](fuentes/catedra/Presentaci%C3%B3n%20de%20PowerPoint2.pdf), Unidad 1 | 2 y 3 |
| Lectura en gris y visualización con `imshow` y escala fija | Presentación de PowerPoint2.pdf | 5 a 7 |
| Escritura de imágenes con `cv2.imwrite` | Presentación de PowerPoint2.pdf | 8 |
| Recortes por indexado de arreglos | Presentación de PowerPoint2.pdf | 12 |
| Tipo `uint8`, rango 0 a 255 y conversión de tipos | Presentación de PowerPoint2.pdf | 14 y 15 |
| Histograma, 256 intervalos y normalización | [PDI_TUIA_U2_Transformacion_y_Filtrado.pdf](fuentes/catedra/PDI_TUIA_U2_Transformacion_y_Filtrado.pdf) | 8 y 9 |
| Ecualización y transformación acumulada discreta | PDI_TUIA_U2_Transformacion_y_Filtrado.pdf | 11 a 13 |
| Comparación de imágenes y sus histogramas | PDI_TUIA_U2_Transformacion_y_Filtrado.pdf | 14 |
| `np.histogram`, división por el número de píxeles y `cumsum` | PDI_TUIA_U2_Transformacion_y_Filtrado.pdf | 15 |
| Requisitos de los campos, ayudas para localizar la grilla y procesamiento cíclico de planillas | Enunciado del TP1 | 2 a 4 |

Los demás PDF se conservan como documentación recibida. Para el Problema 1 no se aplican técnicas de restauración, color, morfología, descriptores ni filtrado frecuencial; el Problema 2 se resuelve con los requisitos y ayudas del enunciado.

## Archivo de entrada y alcance

La página 1 del enunciado menciona `Imagen_con_objetos_ocultos.tiff`, pero el archivo proporcionado se llama `Imagen_con_detalles_escondidos.tif`. Está entre los archivos suministrados junto al repositorio; se pasa al programa mediante `--imagen` y no se incluye en el repositorio para respetar los formatos admitidos. Es una imagen de 256 filas por 256 columnas, de un canal y 8 bits, que coincide visualmente con la figura 1.

Los archivos `grade_sheet_<id>.png` son las entradas de los apartados 2.a a 2.d. La planilla `grade_sheet_empty.png` se excluye del procesamiento cíclico porque no tiene un id numérico.

## Decisiones de implementación

La extensión de la ecualización global a una ventana móvil está pedida por el enunciado. El redondeo a un entero entre 0 y 255 y la exigencia de ventanas impares son decisiones de implementación, explicadas en el apartado a. No se utiliza CLAHE ni una función de ecualización local ya resuelta por una biblioteca.

La organización de carpetas, los argumentos de ejecución y las verificaciones son herramientas auxiliares de Python; no agregan técnicas de procesamiento de imágenes. La conclusión sobre qué ventana resulta útil se obtiene observando los experimentos de esta entrega, no de una recomendación externa.
