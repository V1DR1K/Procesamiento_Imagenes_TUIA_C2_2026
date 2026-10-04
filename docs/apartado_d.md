# Apartado 2.d Procesamiento cíclico de las planillas

El enunciado (página 3, punto d) pide aplicar el algoritmo desarrollado, de forma cíclica, a las cuatro imágenes `grade_sheet_<id>.png` e informar los resultados. Este apartado no agrega técnicas de procesamiento de imágenes: repite sobre cada planilla los pasos de 2.a, 2.b y 2.c.

## Organización del código

- [validar_planilla.py](../validar_planilla.py) contiene la función `procesar_planilla(ruta, carpeta_salida)`. Recibe la ruta de **una** planilla, informa en la terminal el estado OK o MAL de cada campo (2.a), genera la imagen con los recortes de libres y recuperantes (2.b) y escribe el CSV (2.c). Devuelve un resumen con la cantidad de registros, de registros correctos, de libres y de alumnos que recuperan.
- [procesar_planillas.py](../procesar_planillas.py) busca en una carpeta los archivos que siguen el patrón `grade_sheet_<id>.png`, los ordena por su id numérico y llama a `procesar_planilla` para cada uno. Al terminar muestra una tabla con el resumen de todas las planillas.

La planilla vacía `grade_sheet_empty.png` no tiene un id numérico, por lo que queda fuera del ciclo. El orden numérico evita que, por ejemplo, `grade_sheet_10` se procese antes que `grade_sheet_2`.

## Salidas

Cada planilla escribe sus resultados en una subcarpeta propia dentro de la carpeta indicada con `--salida`. Por defecto es `%TEMP%\Procesamiento_Imagenes_TUIA_C2_2026\planillas`:

```
planillas/
  grade_sheet_1/
    grade_sheet_1_recortes_LR.png
    grade_sheet_1_validacion.csv
  grade_sheet_2/
    ...
```

Así, la imagen de 2.b sigue siendo única por planilla y ninguna ejecución pisa los resultados de otra. Si una planilla no tiene registros correctos con condición L o R, no se genera su imagen y la terminal lo informa.

## Ejecución

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -B procesar_planillas.py --carpeta "C:\ruta\planillas" --salida "$env:TEMP\Procesamiento_Imagenes_TUIA_C2_2026\planillas"
```

Para procesar una sola planilla:

```powershell
.\.venv\Scripts\python.exe -B validar_planilla.py --imagen "C:\ruta\planillas\grade_sheet_1.png"
```

## Resultados

Al ejecutar `procesar_planillas.py` sobre las cuatro planillas se obtuvo el siguiente resumen. Cada planilla tiene 20 filas; las que no tienen ningún carácter en sus seis campos se cuentan como vacías y el resto son los registros con datos. "Correctos" son los registros con los seis campos OK y "Con MAL" los registros con datos que tienen al menos un campo incorrecto. "Libres" y "Recuperan" cuentan, entre los correctos, los que tienen condición L y R, que son los que aparecen en la imagen de 2.b.

| Planilla | Filas | Vacías | Con datos | Correctos | Con MAL | Libres | Recuperan |
| --- | --- | --- | --- | --- | --- | --- | --- |
| grade_sheet_1.png | 20 | 5 | 15 | 15 | 0 | 6 | 4 |
| grade_sheet_2.png | 20 | 3 | 17 | 3 | 14 | 3 | 0 |
| grade_sheet_3.png | 20 | 3 | 17 | 0 | 17 | 0 | 0 |
| grade_sheet_4.png | 20 | 3 | 17 | 6 | 11 | 2 | 2 |

En la terminal (2.a) y en el CSV (2.c) se informan las 20 filas, para que el ID coincida con el número de fila de la planilla; los campos de una fila vacía figuran como MAL porque no cumplen las restricciones.

El detalle campo por campo de cada registro se informa en la terminal (2.a) y queda guardado en el CSV de cada planilla (2.c).
