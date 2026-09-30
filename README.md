# Procesamiento de Imágenes I - TP1

**Autor:** Tomas Colombo, Manuel Ibarbia, Juan Manuel Ayala, Franco Cerana. TUIA, UNR, segundo semestre de 2026.

Este repositorio resuelve únicamente el **Problema 1: ecualización local de histograma**, apartados a, b y c. Las planillas `grade_sheet` pertenecen al Problema 2 y quedan fuera del alcance solicitado.

La implementación y la explicación se basan en el enunciado y en el material proporcionado por la cátedra. Véase el [mapa de referencias](docs/referencias.md), con enlaces a los PDF originales y páginas utilizadas.

## Preparación

Se verificó con Python 3.12. Desde la raíz del repositorio, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Se utilizan NumPy, OpenCV y Matplotlib, las bibliotecas presentadas por la cátedra. Las versiones están fijadas para repetir la ejecución.

## Apartado a

La función está en [ecualizacion.py](ecualizacion.py). La [explicación del apartado a](docs/apartado_a.md) detalla el cálculo, los bordes y las ventanas pares.

```python
import cv2
from ecualizacion import ecualizacion_local

imagen = cv2.imread("datos/Imagen_con_detalles_escondidos.tif", cv2.IMREAD_GRAYSCALE)
resultado = ecualizacion_local(imagen, (15, 15))
cv2.imwrite("resultado.png", resultado)
```

Para ejecutar las verificaciones:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Apartado b

[analizar_imagen.py](analizar_imagen.py) procesa la imagen proporcionada y guarda la comparación global/local, sus histogramas y los recortes de las cinco zonas en `resultados/b`.

```powershell
.\.venv\Scripts\python.exe analizar_imagen.py
```

La [explicación del apartado b](docs/apartado_b.md) identifica los objetos: un cuadrado, una diagonal, la letra a, cuatro líneas horizontales y un círculo.

## Apartado c

[comparar_ventanas.py](comparar_ventanas.py) ejecuta diez tamaños: 1x1, 3x3, 7x7, 15x15, 31x31, 63x63, 127x127, 7x31, 31x7 y 4x6. Guarda las imágenes, comparaciones y tiempos en `resultados/c`.

```powershell
.\.venv\Scripts\python.exe comparar_ventanas.py
```

La [explicación del apartado c](docs/apartado_c.md) analiza el contraste, los halos, las variaciones del fondo y la orientación de los rectángulos. Para esta imagen se eligió 15x15, mientras que 31x31 también permite reconocer los detalles.

## Informe y archivos entregados

El [informe del problema 1](docs/informe.md) reúne el resumen y los enlaces a cada apartado. El [registro de validación](docs/validacion.md) indica qué se comprobó y cómo repetirlo.

Se incluyen tres archivos de implementación, las pruebas, 18 imágenes de resultados y figuras, un CSV de tiempos, la imagen de entrada y diez PDF de documentación original. Cada apartado tiene su propio commit, además de los commits de preparación y documentación.

Para elegir una ventana, las dimensiones se expresan como **filas por columnas**. La entrada de la función es una imagen en gris de 8 bits. Los argumentos `--imagen` y `--salida` permiten indicar otras rutas; el apartado b también acepta `--ventana M N`.
