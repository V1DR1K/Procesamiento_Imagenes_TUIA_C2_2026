# Apartado a Implementación de la ecualización local

La función `ecualizacion_local(imagen, tamano_ventana)` de [ecualizacion.py](../ecualizacion.py) recibe una imagen en gris de tipo `uint8` y una ventana `(M, N)`. Devuelve una nueva imagen con la misma forma y tipo. M indica filas y N indica columnas, como se representa una matriz en la Unidad 1, página 3.

## Cálculo en cada ventana

Se cuentan los píxeles de cada nivel entre 0 y 255 con `np.histogram`, se divide cada conteo por `M*N` y se calcula la suma acumulada con `cumsum`. Son las operaciones mostradas en la Unidad 2, páginas 9 y 15. La transformación discreta de la página 13 se aplica al nivel del píxel central:

```text
h[j] = cantidad de píxeles con intensidad j en la ventana
p[j] = h[j] / (M*N)
CDF[k] = p[0] + p[1] + ... + p[k]
salida[fila, columna] = redondear(255 * CDF[imagen[fila, columna]])
```

El factor 255 devuelve el valor normalizado al rango de una imagen de 8 bits. El redondeo se implementa sumando 0,5 y tomando la parte entera, ya que los valores son no negativos. Después se avanza un píxel. Cada ventana se lee de la imagen original con borde, de modo que los resultados anteriores no cambien el histograma siguiente.

## Bordes y tamaños pares

Se utiliza `cv2.copyMakeBorder` con `cv2.BORDER_REPLICATE`, sugeridos en la AYUDA de la página 1 del enunciado. Así se procesa también el borde sin reducir el tamaño de las ventanas ni las dimensiones de salida.

Para una dimensión impar, el anclaje `M // 2` es el centro único. Para una dimensión par no hay un único píxel central: elegimos el de índice `M // 2`, contando desde cero. Por ejemplo, para `(4, 6)` el anclaje es `(2, 3)`, se agregan 2 filas arriba, 1 abajo, 3 columnas a la izquierda y 2 a la derecha. Esta convención permite aceptar todos los enteros positivos pedidos en el enunciado; es una decisión de implementación y no una técnica nueva.

## Caso uniforme y límites

Se aplica la CDF directamente, sin restar su primer valor no nulo. Por eso una ventana uniforme tiene probabilidad acumulada 1 en su intensidad y su píxel central pasa a 255. Con `(1, 1)` ocurre esto en toda la imagen, por lo que no se revelan detalles. No se incorpora una excepción para estos casos: se conserva la fórmula de la cátedra.

Esta implementación explícita es fácil de seguir, aunque recalcular el histograma para cada píxel tarda más al aumentar la ventana. El trabajo se aproxima a `filas * columnas * (M*N + 256)` operaciones. No se usa CLAHE, interpolación por bloques ni optimizaciones ajenas al procedimiento indicado.

## Verificación

Se comprueban un ejemplo calculado a mano, los bordes, ventanas pares, impares, rectangulares y mayores que la imagen, imágenes uniformes, la ventana `(1, 1)`, entradas inválidas y que la imagen original no cambie. El resultado también se contrasta con un conteo directo de píxeles de intensidad menor o igual que el centro, independiente del cálculo de histograma.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Las pruebas son una verificación auxiliar y no agregan operaciones de procesamiento de imágenes a la solución. Las fuentes originales y sus páginas se encuentran en [referencias.md](referencias.md).
