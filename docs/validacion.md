# Validación de la entrega del problema 1

La solución se ejecutó el 30 de septiembre de 2026 con **Python 3.12.10**, NumPy 2.2.6, OpenCV 4.12.0.88, Matplotlib 3.10.6 y ReportLab 4.4.9. Las versiones y las instrucciones para preparar el entorno están en el README.

## Verificaciones realizadas

| Verificación | Resultado |
| --- | --- |
| Cuatro pruebas automatizadas y sus subcasos | Todas pasaron |
| Ejemplo 2x2, ventana 3x3, cálculo manual con borde replicado | Salida `[[113, 170], [198, 255]]`, como se esperaba |
| Contraste con conteo independiente, sin histograma ni agregado de borde de OpenCV | Coincide para siete ventanas, incluidos tamaños pares y mayores que la imagen |
| Dimensiones, tipo y preservación de la entrada | La salida conserva la forma y `uint8`; no se modifica la imagen original |
| Imagen uniforme y ventana 1x1 | Salida blanca, según la CDF directa |
| Entradas inválidas | Se rechazan con un mensaje de error |
| Integridad de fuentes | Diez PDF y una imagen coinciden byte por byte con los originales |
| Archivos de salida | Los 18 PNG temporales se podían leer; las imágenes procesadas conservan 256x256 y `uint8` |
| Resultado local 15x15 | Idéntico en los apartados b y c |
| CSV de tiempos | Diez ventanas, áreas correctas y tiempos positivos |
| Documentación | Enlaces locales comprobados y cinco figuras comparativas inspeccionadas visualmente e incorporadas al PDF |
| Dependencias | Sin incompatibilidades informadas por `pip check` |

Las pruebas están en [tests/test_ecualizacion.py](../tests/test_ecualizacion.py). El cálculo independiente cuenta los vecinos cuya intensidad es menor o igual que la del centro, usando índices limitados al borde. Esa cuenta representa la misma probabilidad acumulada mediante otro procedimiento y permite revisar el resultado de la función.

## Repetir las verificaciones y los análisis

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -B analizar_imagen.py --imagen "C:\ruta\Imagen_con_detalles_escondidos.tif" --salida "$env:TEMP\Procesamiento_Imagenes_TUIA_C2_2026\b"
.\.venv\Scripts\python.exe -B comparar_ventanas.py --imagen "C:\ruta\Imagen_con_detalles_escondidos.tif" --salida "$env:TEMP\Procesamiento_Imagenes_TUIA_C2_2026\c"
.\.venv\Scripts\python.exe -B generar_informe.py --capturas-b "$env:TEMP\Procesamiento_Imagenes_TUIA_C2_2026\b" --capturas-c "$env:TEMP\Procesamiento_Imagenes_TUIA_C2_2026\c"
```

Las últimas dos instrucciones regeneran las imágenes y figuras. Los tiempos del CSV pueden cambiar al repetir la comparación. Las pruebas no sustituyen la inspección visual de las formas, y no se implementó una clasificación automática de objetos.
