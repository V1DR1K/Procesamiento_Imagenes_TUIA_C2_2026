# Procesamiento de Imágenes I - TP1

**Autor:** Tomas Colombo (V1DR1K). TUIA, UNR, segundo semestre de 2026.

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
