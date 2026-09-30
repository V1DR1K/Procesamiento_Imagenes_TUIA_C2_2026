# Informe del problema 1 del TP1

**Integrantes:** Tomas Colombo, Manuel Ibarbia, Juan Manuel Ayala y Franco Cerana. Procesamiento de Imágenes I, TUIA, UNR. Segundo semestre de 2026.

Se resolvieron los apartados a, b y c del Problema 1 mediante ecualización local de histograma. La función recorre la imagen píxel por píxel, calcula el histograma de una ventana y transforma su píxel central. Para la imagen proporcionada, una ventana de 15 por 15 permite reconocer los cinco detalles ocultos.

## Solución por apartado

| Apartado | Implementación | Desarrollo y resultados |
| --- | --- | --- |
| a | [ecualizacion.py](../ecualizacion.py) | [Función, fórmula, bordes y tamaños pares](apartado_a.md) |
| b | [analizar_imagen.py](../analizar_imagen.py) | [Objetos identificados e imágenes comparativas](apartado_b.md) |
| c | [comparar_ventanas.py](../comparar_ventanas.py) | [Influencia de diez ventanas y tiempos de cálculo](apartado_c.md) |

En a se usa una matriz `uint8`, una ventana `(M, N)` de enteros positivos, un histograma de 256 niveles, su normalización y su suma acumulada. Se replica el borde y se guarda una imagen nueva, sin alterar la entrada. El código incluye comentarios con referencias a páginas de la cátedra.

## Problemas y decisiones de procesamiento

Los detalles oscuros tienen valores entre 0 y 11, mientras que el fondo claro está entre 226 y 228. La escasa diferencia de intensidades dentro de cada objeto los oculta en la imagen original y limita lo que muestra una ecualización global. La ecualización local adapta el histograma a los valores de cada entorno y deja ver esas formas.

El borde requiere completar el vecindario de los píxeles extremos. Se usó la replicación propuesta en la ayuda del enunciado. En las ventanas pares no hay un centro único; el código selecciona el píxel con índice `(M // 2, N // 2)`. Estos dos casos afectan la interpretación de los primeros y últimos píxeles de la imagen y se explican en el apartado a.

Los contenidos utilizados son la representación matricial, la escala de grises, el histograma de 256 niveles, su normalización y la transformación acumulada discreta. Se consultaron las páginas 3, 5 a 8 y 12 a 15 de la Presentación de PowerPoint2, las páginas 8 a 15 de PDI_TUIA_U2_Transformacion_y_Filtrado y la página 1 del enunciado. El [mapa de referencias](referencias.md) identifica los PDF originales.

En b se identificaron un cuadrado pequeño en la zona superior izquierda, una diagonal en la superior derecha, una a minúscula en el centro, cuatro líneas horizontales en la inferior izquierda y un círculo en la inferior derecha. La primera figura compara la imagen original, la referencia global y el resultado local con sus histogramas.

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

## Fuentes y alcance

Se adjuntaron el enunciado y los nueve PDF originales recibidos. Las operaciones empleadas corresponden a las Unidades 1 y 2 y a la ayuda de bordes del enunciado. El [mapa de referencias](referencias.md) indica las páginas concretas. El archivo de entrada conserva el nombre proporcionado, `Imagen_con_detalles_escondidos.tif`.

Esta entrega abarca solamente el Problema 1, según el alcance solicitado. Las planillas de calificaciones pertenecen al Problema 2 y no intervienen en la solución.

## Validación y ejecución

Las cuatro pruebas automatizadas pasaron, incluyendo subcasos para ventanas pares, impares, rectangulares, bordes y entradas inválidas. Se revisaron visualmente las figuras comparativas y se comprobó la integridad de las fuentes. Los detalles están en [validacion.md](validacion.md).

Las instrucciones para preparar el entorno, ejecutar cada apartado y compilar este PDF están en el [README](../README.md).

## Límites del resultado

La ecualización modifica el brillo, amplifica variaciones pequeñas y puede producir halos. Una ventana uniforme, incluida 1x1, pasa a blanco al aplicar directamente la CDF. La selección de 15x15 es una conclusión para esta imagen, no una garantía general. Los objetos se identificaron visualmente y los tiempos corresponden a una sola ejecución en este equipo.
