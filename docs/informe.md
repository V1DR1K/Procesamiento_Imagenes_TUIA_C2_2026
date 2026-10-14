# Informe del Trabajo Práctico 1 - Problemas 1 y 2

**Integrantes:** Tomas Colombo, Manuel Ibarbia, Juan Manuel Ayala y Franco Cerana. Procesamiento de Imágenes I, TUIA, UNR. Segundo semestre de 2026.

Se resolvieron los apartados a, b y c del Problema 1 mediante ecualización local de histograma. La función recorre la imagen píxel por píxel, calcula el histograma de una ventana y transforma su píxel central. Para la imagen proporcionada, una ventana de 15 por 15 permite reconocer los cinco detalles ocultos.

También se desarrollaron los apartados a, b, c y d del Problema 2. La solución localiza las celdas de una planilla, verifica las restricciones de formato por campo, produce recortes de los registros correctos con condición L o R y genera un CSV con los estados. El procesamiento cíclico aplica estas operaciones a las cuatro planillas con registros.

## Solución por apartado

| Apartado | Implementación | Desarrollo y resultados |
| --- | --- | --- |
| a | [ecualizacion.py](../ecualizacion.py) | [Función, fórmula, bordes y tamaños pares](apartado_a.md) |
| b | [analizar_imagen.py](../analizar_imagen.py) | [Objetos identificados e imágenes comparativas](apartado_b.md) |
| c | [comparar_ventanas.py](../comparar_ventanas.py) | [Influencia de diez ventanas y tiempos de cálculo](apartado_c.md) |
| 2.a | [validar_planilla.py](../validar_planilla.py) | [Detección de grilla y validación estructural por campo](apartado_2a.md) |
| 2.b | [validar_planilla.py](../validar_planilla.py) | [Clasificación de condición y recortes de libres y recuperantes](apartado_2b.md) |
| 2.c | [validar_planilla.py](../validar_planilla.py) | CSV con ID y estado OK/MAL para los seis campos de cada registro. |
| 2.d | [procesar_planillas.py](../procesar_planillas.py) | [Ejecución cíclica y resumen de las cuatro planillas](apartado_2d.md) |

En a se usa una matriz `uint8`, una ventana `(M, N)` de enteros positivos, un histograma de 256 niveles, su normalización y su suma acumulada. Se replica el borde y se guarda una imagen nueva, sin alterar la entrada. El código incluye comentarios con referencias a páginas de la cátedra.

## Problemas y decisiones de procesamiento

Los detalles oscuros tienen valores entre 0 y 11, mientras que el fondo claro está entre 226 y 228. La escasa diferencia de intensidades dentro de cada objeto los oculta en la imagen original y limita lo que muestra una ecualización global. La ecualización local adapta el histograma a los valores de cada entorno y deja ver esas formas.

El borde requiere completar el vecindario de los píxeles extremos. Se usó la replicación propuesta en la ayuda del enunciado. En las ventanas pares no hay un centro único; el código selecciona el píxel con índice `(M // 2, N // 2)`. Estos dos casos afectan la interpretación de los primeros y últimos píxeles de la imagen y se explican en el apartado a.

Los contenidos utilizados son la representación matricial, la escala de grises, el histograma de 256 niveles, su normalización y la transformación acumulada discreta. Se consultaron las páginas 3, 5 a 8 y 12 a 15 de la Presentación de PowerPoint2, las páginas 8 a 15 de PDI_TUIA_U2_Transformacion_y_Filtrado y la página 1 del enunciado. El [mapa de referencias](referencias.md) identifica los PDF originales.

En b se identificaron un cuadrado pequeño en la zona superior izquierda, una diagonal en la superior derecha, una a minúscula en el centro, cuatro líneas horizontales en la inferior izquierda y un círculo en la inferior derecha. La primera figura compara la imagen original, la ecualización global de OpenCV (cv2.equalizeHist) y el resultado local con sus histogramas.

<!-- CAPTURA: b_histogramas -->

La segunda figura compara los recortes originales con sus resultados locales en las cinco zonas.

<!-- CAPTURA: b_zonas -->

En c se compararon las ventanas 1x1, 3x3, 7x7, 15x15, 31x31, 63x63, 127x127, 7x31, 31x7 y 4x6. Las chicas destacan contornos y variaciones; las grandes incluyen más fondo y debilitan varios detalles. Los rectángulos cambian la orientación de los halos. La figura siguiente reúne la comparación completa.

<!-- CAPTURA: c_ventanas -->

Los recortes permiten observar los cinco objetos con ventanas cuadradas. Las formas se mantienen legibles con 15x15 y 31x31.

<!-- CAPTURA: c_zonas -->

La comparación rectangular muestra que la orientación de la ventana cambia la respuesta alrededor de los objetos.

<!-- CAPTURA: c_rectangulares -->

Los tiempos se midieron durante el procesamiento de las ventanas; no incluyen el guardado de las imágenes ni de las figuras. Cambian según el equipo y su carga. Se listan como referencia del costo computacional.

| Ventana | Segundos |
| --- | ---: |
| 1x1 | 5,77 |
| 3x3 | 3,94 |
| 7x7 | 5,02 |
| 15x15 | 5,20 |
| 31x31 | 5,51 |
| 63x63 | 7,93 |
| 127x127 | 15,65 |
| 7x31 | 6,22 |
| 31x7 | 4,36 |
| 4x6 | 5,61 |

## Problema 2 - Validación de planillas de calificaciones

El enunciado (páginas 2 a 4) pide validar seis campos por registro: Legajo, Nombre y Apellido, tres parciales y Condición Final. Se comprueba que los campos respeten restricciones de formato; no se verifica que el nombre, el legajo o las notas sean verdaderos. La solución aprovecha el supuesto de que cada campo ocupa un renglón y contiene caracteres del conjunto indicado en el enunciado.

### Apartado 2.a - Estado de cada campo

La función **procesar_planilla** de [validar_planilla.py](../validar_planilla.py) recibe una imagen de planilla. Para localizar los campos, primero la lee en escala de grises y aplica un umbral inverso de 200: las líneas oscuras quedan como píxeles blancos en una máscara binaria. Luego suma esos píxeles por fila y por columna. Las líneas horizontales y verticales tienen proyecciones altas; el programa umbraliza cada proyección, agrupa coordenadas contiguas y toma el centro de cada grupo como posición de línea.

Se toman las últimas 21 líneas horizontales para delimitar los 20 registros. Las líneas verticales internas delimitan los seis campos que se validan; la columna de número de registro queda fuera. Cada celda se recorta con un margen de 4 píxeles para quitar las líneas de la tabla y evitar que se confundan con trazos escritos.

Dentro de cada recorte se aplica un umbral inverso de 127. **connectedComponentsWithStats** etiqueta los grupos de píxeles de tinta, calcula sus áreas y cajas delimitadoras, y se cuentan los componentes con área mayor que 1. Se usa conectividad 8, por lo que también se conectan píxeles diagonales. Las cajas se ordenan de izquierda a derecha; una separación horizontal mayor que 6 píxeles se interpreta como espacio entre palabras. Así se obtiene una estimación estructural de la cantidad de caracteres y palabras sin reconocer el texto.

| Campo | Restricción | Regla aplicada |
| --- | --- | --- |
| Legajo | 8 caracteres en una palabra | 8 componentes y 1 palabra. |
| Nombre y Apellido | Al menos 2 palabras y hasta 12 caracteres | 2 o más palabras y no más de 12 componentes. |
| Parciales 1, 2 y 3 | 1 o 2 caracteres consecutivos | 1 o 2 componentes y 1 palabra. |
| Condición Final | Un único carácter | 1 componente. |

El programa informa por terminal, para cada registro, OK o MAL en cada uno de los seis campos. La salida indica si la estructura detectada cumple las reglas; no transcribe el legajo, el nombre ni las notas. Una fila vacía tiene cero componentes, por lo que sus campos quedan MAL.

### Apartado 2.b - Recortes de alumnos libres y recuperantes

Para formar la imagen de salida se consideran únicamente los registros cuyos seis campos resultaron OK. Después se analiza el único carácter de Condición Final. El método **clasificar_condicion** es una heurística topológica y geométrica ajustada a las letras mayúsculas de las planillas, no un OCR general:

1. Se binariza el campo, se localiza el componente más grande y se lo recorta como glifo.

2. Se invierte el glifo, se agrega un borde de fondo y se cuentan los componentes del fondo con conectividad 4. Si no hay un agujero interno, se clasifica como L.

3. Si hay un agujero, se mide la proporción de píxeles de tinta en el cuarto superior izquierdo. Si supera 0,4 se clasifica como R; en caso contrario, como A.

Esta regla distingue las formas previstas porque L no tiene agujero, mientras que R y A sí; la densidad superior izquierda separa R de A en las imágenes proporcionadas. La clasificación depende de que la forma de la letra se conserve después del umbralado.

Para cada registro correcto con condición L o R se extrae el recorte de Nombre y Apellido. Se agrega un borde azul a L y uno rojo a R para diferenciarlos, y los recortes se apilan verticalmente en una única imagen por planilla. En OpenCV esos colores se escriben en orden BGR: azul (255, 0, 0) y rojo (0, 0, 255). Los registros A y los registros con algún campo MAL no se incluyen.

### Apartados 2.c y 2.d - CSV y ejecución sobre las cuatro planillas

El mismo procesamiento genera un CSV por planilla. Cada fila representa el registro en su orden original: la primera columna es el ID, numerado desde 1, seguida por Legajo, Nombre y Apellido, Parcial 1, Parcial 2, Parcial 3 y Condición Final. Cada campo contiene solamente OK o MAL; el CSV no incluye texto reconocido.

**procesar_planillas.py** busca los archivos grade_sheet_<id>.png, los ordena por el ID numérico y ejecuta el procesamiento para cada uno. El orden numérico evita, por ejemplo, que el archivo 10 se procese antes que el 2. grade_sheet_empty.png se excluye del lote porque no contiene un ID numérico. Cada planilla guarda sus archivos en una subcarpeta propia.

Los resultados documentados para las cuatro imágenes son:

| Planilla | Filas | Vacías | Con datos | Correctos | Con algún MAL | Libres | Recuperan |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| grade_sheet_1.png | 20 | 5 | 15 | 15 | 0 | 6 | 4 |
| grade_sheet_2.png | 20 | 3 | 17 | 3 | 14 | 3 | 0 |
| grade_sheet_3.png | 20 | 3 | 17 | 0 | 17 | 0 | 0 |
| grade_sheet_4.png | 20 | 3 | 17 | 6 | 11 | 2 | 2 |

Las filas vacías se cuentan aparte del total de registros con datos. En la salida campo por campo aparecen como MAL porque no satisfacen las restricciones.

## Fuentes y alcance

Se adjuntaron el enunciado y los nueve PDF originales recibidos. Para el Problema 1 se utilizan conceptos de las Unidades 1 y 2 y la ayuda de bordes del enunciado. El Problema 2 usa detección de grilla por proyecciones y conteo de componentes conectados, de acuerdo con las ayudas de las páginas 3 y 4 del enunciado. El [mapa de referencias](referencias.md) identifica los PDF y las páginas. El archivo de entrada de P1 conserva el nombre proporcionado, Imagen_con_detalles_escondidos.tif.

Este informe reúne los Problemas 1 y 2. Las funciones de P2 validan el formato de los campos bajo los supuestos de impresión, alineación y caracteres definidos por el enunciado; no realizan reconocimiento óptico de caracteres.

## Validación y ejecución

La validación automatizada documentada corresponde al Problema 1: incluye el caso de cálculo manual, ventanas pares, impares, rectangulares, bordes y entradas inválidas. También se revisaron visualmente las figuras comparativas y la integridad de las fuentes. Los detalles están en [validacion.md](validacion.md). Para el Problema 2, el repositorio documenta el desarrollo y los resultados de las planillas en las explicaciones de [2.a](apartado_2a.md), [2.b](apartado_2b.md) y [2.d](apartado_2d.md); no se informa allí una batería equivalente de pruebas automatizadas.

Las instrucciones para preparar el entorno, ejecutar cada apartado y compilar este PDF están en el [README](../README.md).

## Límites del resultado

En el Problema 1, la ecualización modifica el brillo, amplifica variaciones pequeñas y puede producir halos. Una ventana uniforme, incluida 1x1, pasa a blanco al aplicar directamente la CDF. La selección de 15x15 es una conclusión para esta imagen, no una garantía general. Los objetos se identificaron visualmente y los tiempos corresponden a una sola ejecución en este equipo.

En el Problema 2, las proyecciones de líneas y los umbrales fijos suponen planillas alineadas, con tamaño y contraste similares a las provistas. El margen de 4 píxeles y la separación de 6 píxeles entre componentes son parámetros geométricos. Si cambia la resolución, inclinación, iluminación o tipografía, pueden fallar la separación de campos y el conteo. Además, contar componentes no verifica el alfabeto permitido ni el significado de los datos.
