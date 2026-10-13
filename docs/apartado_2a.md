# Problema 2 — Apartado 2.a: estado de cada campo

El objetivo de 2.a es informar, para cada registro de la planilla, si cada uno de sus seis campos cumple las restricciones de formato del enunciado. La implementación está en [`validar_planilla.py`](../validar_planilla.py), principalmente en `extraer_grilla`, `contar_caracteres_y_palabras`, `validar_fila` y `procesar_planilla`.

## 1. Localizar las celdas

La imagen se lee en escala de grises. Se aplica un umbral inverso de 200: los trazos oscuros de la tabla pasan a blanco en una máscara binaria y el fondo claro pasa a negro. Después se suman los píxeles blancos por fila y por columna. Una línea horizontal ocupa gran parte de una fila y una vertical gran parte de una columna, por lo que sus proyecciones superan la mitad de la dimensión correspondiente.

El programa agrupa coordenadas contiguas que superan ese umbral y usa el centro de cada grupo como posición de una línea. De las líneas horizontales conserva las últimas 21, que delimitan los 20 registros. Las líneas verticales internas delimitan los campos de datos; se omite la columna con el número de fila. A cada celda se le quitan 4 píxeles de margen para que las líneas de la tabla no se cuenten como tinta escrita.

## 2. Estimar caracteres y palabras

Cada celda se binariza con umbral inverso de 127. `cv2.connectedComponentsWithStats`, con conectividad 8, agrupa píxeles de tinta que se tocan incluso en diagonal. Se cuentan los componentes de área mayor que 1 y se usan sus cajas delimitadoras.

Las cajas se ordenan de izquierda a derecha. Si la distancia entre dos cajas consecutivas supera 6 píxeles, se interpreta que hay un espacio entre palabras. Así se estiman cantidades de caracteres y palabras para contrastarlas con las reglas del enunciado. El método no reconoce qué letras o números fueron escritos.

| Campo | Restricción de formato | Condición del código |
| --- | --- | --- |
| Legajo | Ocho caracteres en una palabra | 8 componentes y 1 palabra. |
| Nombre y Apellido | Al menos dos palabras y hasta 12 caracteres | 2 o más palabras y hasta 12 componentes. |
| Parciales 1, 2 y 3 | Uno o dos caracteres consecutivos | 1 o 2 componentes y 1 palabra. |
| Condición Final | Un único carácter | 1 componente. |

Para cada registro se imprimen seis estados `OK` o `MAL`, uno por campo. El CSV del apartado 2.c reutiliza la misma validación y guarda esos estados por registro. Una celda vacía no tiene componentes y queda `MAL`.

## Qué valida y qué no

La solución valida **estructura y cantidad**, no el contenido semántico. Por ejemplo, no comprueba que el legajo exista, que el nombre sea una persona, que una nota sea numérica ni que el carácter de condición pertenezca a `L`, `R` o `A`. Tampoco transcribe el texto: no implementa OCR. Esto es consistente con el alcance de 2.a, que pide comprobar las restricciones de los campos.

El conteo depende de que la planilla tenga tamaño, contraste y alineación parecidos a los ejemplos. Letras unidas, trazos separados, puntos, ruido o cambios de escala pueden alterar la cantidad de componentes o la estimación de espacios. El umbral de 6 píxeles y el margen de 4 son parámetros geométricos ajustados a las planillas provistas.

## Ejecución

Desde la raíz del repositorio, para procesar una planilla y mostrar los estados:

```powershell
.\.venv\Scripts\python.exe -B validar_planilla.py --imagen "C:\ruta\grade_sheet_1.png"
```

El proceso también genera el recorte del apartado 2.b cuando corresponde y el CSV del apartado 2.c. Para repetir el mismo algoritmo sobre todas las planillas, véase [apartado 2.d](apartado_2d.md).
