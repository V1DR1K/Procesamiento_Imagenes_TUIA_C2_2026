# Procesamiento de Imágenes I - TP1

**Integrantes:** Tomas Colombo, Manuel Ibarbia, Juan Manuel Ayala y Franco Cerana. TUIA, UNR, segundo semestre de 2026.

Este repositorio resuelve únicamente el **Problema 1: ecualización local de histograma**, apartados a, b y c. Las planillas `grade_sheet` pertenecen al Problema 2 y quedan fuera del alcance solicitado.

La implementación y la explicación se basan en el enunciado y en el material proporcionado por la cátedra. Véase el [mapa de referencias](docs/referencias.md), con enlaces a los PDF originales y páginas utilizadas. La resolución abarca el Problema 1, apartados a, b y c.

## Preparación

Versiones utilizadas:

| Componente | Versión |
| --- | --- |
| Python | 3.12.10 |
| NumPy | 2.2.6 |
| OpenCV | 4.12.0.88 |
| Matplotlib | 3.10.6 |
| ReportLab (compilación del informe) | 4.4.9 |

Desde la raíz del repositorio, en PowerShell, se prepara el entorno:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install numpy==2.2.6 opencv-python==4.12.0.88 matplotlib==3.10.6 reportlab==4.4.9
```

NumPy, OpenCV y Matplotlib se usan para el procesamiento y las figuras. ReportLab compila el informe Markdown a PDF. Las versiones están fijadas para repetir la ejecución. No hace falta instalar una biblioteca para correr las pruebas: usan `unittest`, incluido en Python.

## Apartado a

La función está en [ecualizacion.py](ecualizacion.py). La [explicación del apartado a](docs/apartado_a.md) detalla el cálculo, los bordes y las ventanas pares. El script del apartado b la ejecuta sobre la imagen de entrada.

```python
import cv2
from pathlib import Path
import tempfile
from ecualizacion import ecualizacion_local

imagen = cv2.imread(r"C:\ruta\Imagen_con_detalles_escondidos.tif", cv2.IMREAD_GRAYSCALE)
resultado = ecualizacion_local(imagen, (15, 15))
salida = Path(tempfile.gettempdir()) / "resultado.png"
cv2.imwrite(str(salida), resultado)
```

Para ejecutar las verificaciones:

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

## Apartado b

[analizar_imagen.py](analizar_imagen.py) procesa la imagen proporcionada y guarda la comparación global/local, sus histogramas y los recortes de las cinco zonas. Se debe indicar la ruta de la imagen y se pueden guardar los resultados temporales fuera del repositorio:

```powershell
$imagenTp = "C:\ruta\Imagen_con_detalles_escondidos.tif"
$salidaTp = Join-Path $env:TEMP "Procesamiento_Imagenes_TUIA_C2_2026"
.\.venv\Scripts\python.exe analizar_imagen.py --imagen $imagenTp --salida (Join-Path $salidaTp "b")
```

La [explicación del apartado b](docs/apartado_b.md) identifica los objetos: un cuadrado, una diagonal, la letra a, cuatro líneas horizontales y un círculo.

## Apartado c

[comparar_ventanas.py](comparar_ventanas.py) ejecuta diez tamaños: 1x1, 3x3, 7x7, 15x15, 31x31, 63x63, 127x127, 7x31, 31x7 y 4x6. Guarda las imágenes, comparaciones y tiempos fuera del repositorio.

```powershell
.\.venv\Scripts\python.exe comparar_ventanas.py --imagen $imagenTp --salida (Join-Path $salidaTp "c")
```

La [explicación del apartado c](docs/apartado_c.md) analiza el contraste, los halos, las variaciones del fondo y la orientación de los rectángulos. Para esta imagen se eligió 15x15, mientras que 31x31 también permite reconocer los detalles.

## Problema 2, apartado d

[procesar_planillas.py](procesar_planillas.py) aplica de forma cíclica la validación de [validar_planilla.py](validar_planilla.py) a todos los archivos `grade_sheet_<id>.png` de una carpeta, ordenados por id; la planilla vacía queda excluida. Por cada planilla se guardan su imagen de recortes y su CSV en una subcarpeta propia, y al final se muestra un resumen de todas.

```powershell
$planillas = "C:\ruta\planillas"
.\.venv\Scripts\python.exe procesar_planillas.py --carpeta $planillas --salida (Join-Path $salidaTp "planillas")
```

Para validar una sola planilla: `.\.venv\Scripts\python.exe validar_planilla.py --imagen (Join-Path $planillas "grade_sheet_1.png")`. La [explicación del apartado 2.d](docs/apartado_d.md) detalla la organización y las salidas.

## Informe en PDF

El [informe fuente en Markdown](docs/informe.md) incluye marcas para insertar las capturas generadas por los apartados b y c. Después de ejecutar ambos scripts, se compila con:

```powershell
.\.venv\Scripts\python.exe generar_informe.py --capturas-b (Join-Path $salidaTp "b") --capturas-c (Join-Path $salidaTp "c")
```

Esto crea `docs/informe.pdf`, con el desarrollo, las observaciones, las conclusiones y las figuras intermedias. Para repetirlo hay que conservar los resultados temporales hasta que termine la compilación.

## Informe y archivos entregados

El [informe del problema 1 en Markdown](docs/informe.md) y su versión [compilada en PDF](docs/informe.pdf) reúnen el desarrollo, las capturas, el análisis y las conclusiones. El [registro de validación](docs/validacion.md) describe las verificaciones realizadas.

Los archivos incluidos en el repositorio usan únicamente los formatos `.py`, `.pdf` y `.md`. La imagen de entrada se proporciona con el enunciado; su ruta se indica con `--imagen`. Las figuras y la planilla de tiempos se guardan en la carpeta temporal elegida con `--salida` y se incluyen en el informe PDF.

Para elegir una ventana, las dimensiones se expresan como **filas por columnas**. La entrada de la función es una imagen en gris de 8 bits. Los argumentos `--imagen` y `--salida` permiten indicar las rutas de entrada y salida; el apartado b también acepta `--ventana M N`.
