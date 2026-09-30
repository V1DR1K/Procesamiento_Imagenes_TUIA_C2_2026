# Informe del problema 1 del TP1

**Autor:** Tomas Colombo (V1DR1K). Procesamiento de Imágenes I, TUIA, UNR. Segundo semestre de 2026.

Se resolvieron los apartados a, b y c del Problema 1 mediante ecualización local de histograma. La función recorre la imagen píxel por píxel, calcula el histograma de una ventana y transforma su píxel central. Para la imagen proporcionada, una ventana de 15 por 15 permite reconocer los cinco detalles ocultos.

## Solución por apartado

| Apartado | Implementación | Desarrollo y resultados |
| --- | --- | --- |
| a | [ecualizacion.py](../ecualizacion.py) | [Función, fórmula, bordes y tamaños pares](apartado_a.md) |
| b | [analizar_imagen.py](../analizar_imagen.py) | [Objetos identificados e imágenes comparativas](apartado_b.md) |
| c | [comparar_ventanas.py](../comparar_ventanas.py) | [Influencia de diez ventanas y tiempos de cálculo](apartado_c.md) |

En a se usa una matriz `uint8`, una ventana `(M, N)` de enteros positivos, un histograma de 256 niveles, su normalización y su suma acumulada. Se replica el borde y se guarda una imagen nueva, sin alterar la entrada. El código incluye comentarios con referencias a páginas de la cátedra.

En b se identificaron un cuadrado pequeño en la zona superior izquierda, una diagonal en la superior derecha, una a minúscula en el centro, cuatro líneas horizontales en la inferior izquierda y un círculo en la inferior derecha. Se guardaron la imagen original, la referencia global, el resultado local, los histogramas y los recortes.

En c se compararon las ventanas 1x1, 3x3, 7x7, 15x15, 31x31, 63x63, 127x127, 7x31, 31x7 y 4x6. Las chicas destacan contornos y variaciones; las grandes incluyen más fondo y debilitan varios detalles. Los rectángulos cambian la orientación de los halos. Se eligió 15x15 para esta imagen; 31x31 también permite distinguir las cinco formas.

## Fuentes y alcance

Se adjuntaron el enunciado y los nueve PDF originales recibidos. Las operaciones empleadas corresponden a las Unidades 1 y 2 y a la ayuda de bordes del enunciado. El [mapa de referencias](referencias.md) indica las páginas concretas. El archivo de entrada conserva el nombre proporcionado, `Imagen_con_detalles_escondidos.tif`.

Esta entrega abarca solamente el Problema 1. Las planillas de calificaciones pertenecen al Problema 2 y no intervienen en la solución.

## Validación y ejecución

Las cuatro pruebas automatizadas pasaron, incluyendo subcasos para ventanas pares, impares, rectangulares, bordes y entradas inválidas. Se revisaron visualmente las cinco figuras comparativas y se comprobaron las imágenes guardadas, los enlaces y la integridad de las fuentes. Los detalles están en [validacion.md](validacion.md).

Las instrucciones para preparar el entorno y ejecutar cada apartado están en el [README](../README.md). Las imágenes y los tiempos ya están guardados en `resultados/b` y `resultados/c`.

## Límites del resultado

La ecualización modifica el brillo, amplifica variaciones pequeñas y puede producir halos. Una ventana uniforme, incluida 1x1, pasa a blanco al aplicar directamente la CDF. La selección de 15x15 es una conclusión para esta imagen, no una garantía general. Los objetos se identificaron visualmente y los tiempos corresponden a una sola ejecución en este equipo.
