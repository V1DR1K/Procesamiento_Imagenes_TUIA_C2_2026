# Apartado b Detalles ocultos de la imagen

Se aplicó la función del apartado a sobre `datos/Imagen_con_detalles_escondidos.tif`, con una ventana de **15 por 15 píxeles**. Se inspeccionó el resultado y se identificaron los cinco detalles de la figura 1. La elección de esta ventana sirve para el análisis inicial; su influencia se estudia en el apartado c.

## Objetos observados

| Zona | Detalle identificado | Recorte en la matriz original |
| --- | --- | --- |
| Superior izquierda | Un cuadrado pequeño dentro del cuadrado oscuro | Filas `[6:68]`, columnas `[6:68]` |
| Superior derecha | Una línea diagonal ascendente de izquierda a derecha, semejante a `/` | Filas `[6:68]`, columnas `[187:249]` |
| Centro | La letra **a minúscula** | Filas `[97:159]`, columnas `[97:159]` |
| Inferior izquierda | **Cuatro líneas horizontales** paralelas | Filas `[188:250]`, columnas `[6:68]` |
| Inferior derecha | Un círculo relleno | Filas `[188:250]`, columnas `[187:249]` |

Los índices comienzan en cero y el extremo final de cada recorte queda excluido, como en el indexado de arreglos mostrado en la Unidad 1, página 12. Los nombres se asignaron por inspección visual; no se utilizó reconocimiento automático de objetos.

![Original arriba y resultado local abajo, para las cinco zonas](../resultados/b/zonas.png)

## Por qué mejora la visibilidad

En las cinco regiones oscuras, los valores de la imagen original van de 0 a 11, mientras que el fondo claro contiene valores de 226 a 228. Estas cifras se comprobaron en los píxeles de la imagen proporcionada. Una diferencia de pocos niveles en un objeto oscuro ocupa una parte muy pequeña del rango 0 a 255, por lo que resulta difícil distinguirlo.

La ecualización local calcula probabilidades usando los píxeles cercanos al centro. Así puede repartir esas diferencias sobre un intervalo mayor de intensidades. Es la transformación acumulada de la Unidad 2, páginas 11 a 15, aplicada al entorno pedido en la página 1 del enunciado.

Como referencia, se calculó también una ecualización global con la misma fórmula y el mismo redondeo, considerando toda la imagen. Los detalles siguen siendo débiles porque predominan el fondo claro y los grandes cuadrados oscuros. En la versión local se distinguen con mayor claridad las cinco formas.

![Comparación de imágenes e histogramas](../resultados/b/comparacion_histogramas.png)

Todos los paneles de imágenes usan `vmin=0` y `vmax=255`, como se muestra en la Unidad 1, páginas 6 y 7. Se evita que el visor ajuste por separado el contraste de cada imagen. Cada histograma conserva los 256 intervalos; su eje vertical se ajusta por panel para visualizar sus conteos.

## Efectos observados

La salida muestra puntos claros u oscuros más notorios: pequeñas variaciones ya presentes quedan amplificadas al cambiar su intensidad. También aparecen halos alrededor de los detalles y de los límites de los cuadrados. Son efectos del histograma que cambia al mover la ventana, no nuevos objetos descubiertos.

Las zonas uniformes se aproximan al blanco porque la CDF directa vale 1 en su único nivel; esto se explicó en el apartado a. Por esa razón, la salida sirve para revelar detalles, pero no conserva necesariamente la apariencia ni el brillo originales. Se mantiene el procedimiento pedido, sin agregar filtros de ruido ni otras técnicas.

## Repetir la ejecución

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe analizar_imagen.py
```

Opcionalmente se puede indicar otra ventana:

```powershell
.\.venv\Scripts\python.exe analizar_imagen.py --ventana 15 15 --salida resultados/b
```

El script genera `original.png`, `global.png`, `local_15x15.png`, `comparacion_histogramas.png` y `zonas.png`. Las imágenes de salida se guardan como PNG, según la escritura presentada en la Unidad 1, página 8. El [mapa de referencias](referencias.md) permite consultar las fuentes originales.
