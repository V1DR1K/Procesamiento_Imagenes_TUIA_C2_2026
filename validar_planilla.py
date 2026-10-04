"""Problema 2: Validación de planilla de calificaciones sin OCR.
Resolución de apartados 2.a, 2.b, 2.c y 2.d.
"""

import argparse
import cv2
import numpy as np
import tempfile
from pathlib import Path
import csv
SALIDAS_TEMPORALES = Path(tempfile.gettempdir()) / "Procesamiento_Imagenes_TUIA_C2_2026"

def extraer_grilla(imagen_ruta):
    """Detecta las líneas de la tabla y recorta las celdas en escala de grises."""
    # cv2.imread falla en Windows con rutas con tildes (por ejemplo "Imágenes"):
    # leemos los bytes con NumPy y los decodificamos con OpenCV.
    img = cv2.imdecode(np.fromfile(str(imagen_ruta), dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"No se pudo leer la imagen: {imagen_ruta}")

    _, img_th = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)
    img_th_ones = (img_th / 255).astype(np.uint8)

    img_rows = np.sum(img_th_ones, axis=1)
    img_cols = np.sum(img_th_ones, axis=0)

    th_row = img.shape[1] * 0.5 
    th_col = img.shape[0] * 0.5 

    img_rows_th = img_rows > th_row
    img_cols_th = img_cols > th_col

    def encontrar_lineas(vector_binario):
        lineas = []
        en_linea = False
        inicio = 0
        for i, val in enumerate(vector_binario):
            if val and not en_linea:
                inicio = i
                en_linea = True
            elif not val and en_linea:
                lineas.append((inicio + i) // 2)
                en_linea = False
        return lineas

    filas = encontrar_lineas(img_rows_th)
    columnas = encontrar_lineas(img_cols_th)

    filas_registros = filas[-21:] 

    celdas = []
    for i in range(len(filas_registros) - 1):
        fila_celdas = []
        y_inicio = filas_registros[i]
        y_fin = filas_registros[i+1]
        
        for j in range(1, len(columnas) - 1):
            x_inicio = columnas[j]
            x_fin = columnas[j+1]
            
            margen = 4
            celda_gris = img[y_inicio+margen : y_fin-margen, x_inicio+margen : x_fin-margen]
            fila_celdas.append(celda_gris)
        
        celdas.append(fila_celdas)

    return celdas

def contar_caracteres_y_palabras(celda_gris):
    """Cuenta caracteres y palabras binarizando localmente."""
    _, celda_th = cv2.threshold(celda_gris, 127, 255, cv2.THRESH_BINARY_INV)
    num_labels, _, stats, _ = cv2.connectedComponentsWithStats(celda_th, connectivity=8, ltype=cv2.CV_32S)
    
    caracteres_validos = []
    # Con 2 se descartaba el punto de "1.0" (área 2 px). El margen de la celda ya quita las líneas.
    area_minima = 1
    
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area > area_minima:
            x = stats[i, cv2.CC_STAT_LEFT]
            width = stats[i, cv2.CC_STAT_WIDTH]
            caracteres_validos.append({'x_inicio': x, 'x_fin': x + width})
            
    cantidad_caracteres = len(caracteres_validos)
    if cantidad_caracteres == 0:
        return 0, 0
        
    caracteres_validos.sort(key=lambda c: c['x_inicio'])
    
    cantidad_palabras = 1
    umbral_espacio = 6 
    
    for i in range(1, len(caracteres_validos)):
        distancia = caracteres_validos[i]['x_inicio'] - caracteres_validos[i-1]['x_fin']
        if distancia > umbral_espacio:
            cantidad_palabras += 1
            
    return cantidad_caracteres, cantidad_palabras

def clasificar_condicion(celda_gris):
    """Clasifica un caracter en L, R o A analizando sus agujeros y densidad."""
    _, celda_th = cv2.threshold(celda_gris, 127, 255, cv2.THRESH_BINARY_INV)
    num_labels, _, stats, _ = cv2.connectedComponentsWithStats(celda_th, connectivity=8)
    
    if num_labels < 2:
        return 'X'
        
    largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    x, y, w, h = stats[largest_label, cv2.CC_STAT_LEFT:cv2.CC_STAT_LEFT+4]
    char_roi = celda_th[y:y+h, x:x+w]
    
    # Invertimos el ROI para contar los componentes del fondo (agujeros)
    bg = cv2.bitwise_not(char_roi)
    bg_padded = cv2.copyMakeBorder(bg, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=255)
    num_bg_labels, _, _, _ = cv2.connectedComponentsWithStats(bg_padded, connectivity=4)
    
    # Si el fondo tiene 2 componentes o menos (1 del objeto, 1 del fondo externo) no hay agujeros
    if num_bg_labels <= 2:
        return 'L'
    else:
        # Evaluamos la densidad de píxeles en el cuarto superior izquierdo para diferenciar R de A
        top_left = char_roi[0:h//4, 0:w//4]
        density_tl = np.sum(top_left) / 255 / (top_left.size + 1e-5)
        return 'R' if density_tl > 0.4 else 'A'

def validar_fila(celdas):
    """Valida formato y devuelve tupla de resultados."""
    chars_leg, pals_leg = contar_caracteres_y_palabras(celdas[0])
    ok_leg = (chars_leg == 8 and pals_leg == 1)
    
    chars_nom, pals_nom = contar_caracteres_y_palabras(celdas[1])
    ok_nom = (chars_nom <= 12 and pals_nom >= 2)
    
    chars_p1, pals_p1 = contar_caracteres_y_palabras(celdas[2])
    ok_p1 = (chars_p1 in [1, 2] and pals_p1 == 1)
    
    chars_p2, pals_p2 = contar_caracteres_y_palabras(celdas[3])
    ok_p2 = (chars_p2 in [1, 2] and pals_p2 == 1)
    
    chars_p3, pals_p3 = contar_caracteres_y_palabras(celdas[4])
    ok_p3 = (chars_p3 in [1, 2] and pals_p3 == 1)
        
    chars_cond, _ = contar_caracteres_y_palabras(celdas[5])
    ok_cond = (chars_cond == 1)
    
    return [ok_leg, ok_nom, ok_p1, ok_p2, ok_p3, ok_cond]

    """Genera un archivo CSV con los resultados de las validaciones.
    
    Resuelve el apartado 2.c del TP.
    """
def generar_csv_resultados(celdas_registros, ruta_salida_csv):

    encabezados = [
        "ID", 
        "Legajo", 
        "Nombre y Apellido", 
        "Parcial 1", 
        "Parcial 2", 
        "Parcial 3", 
        "Condicion Final"
    ]
    
    filas_csv = []
    
    # Recorremos cada registro (fila de celdas)
    for idx, fila_celdas in enumerate(celdas_registros):
        validacion_bool = validar_fila(fila_celdas)
        resultados_str = ["OK" if es_ok else "MAL" for es_ok in validacion_bool]
        
        # Formamos la fila con el ID en la primera columna + los resultados
        id_registro = idx + 1
        fila_registro = [id_registro] + resultados_str
        filas_csv.append(fila_registro)
        
    # Escribimos el archivo CSV
    with open(ruta_salida_csv, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados) 
        escritor.writerows(filas_csv)   

    print(f"Apartado 2.c: Archivo CSV generado exitosamente en {ruta_salida_csv}")

def procesar_planilla(ruta, carpeta_salida=None):
    """Resuelve 2.a, 2.b y 2.c para una planilla y devuelve un resumen para 2.d."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró la planilla: {ruta}")
    carpeta = Path(carpeta_salida) if carpeta_salida is not None else SALIDAS_TEMPORALES / ruta.stem
    carpeta.mkdir(parents=True, exist_ok=True)
    # Cada planilla escribe sus salidas con su nombre para no pisar las de las otras.
    img_salida_path = carpeta / f"{ruta.stem}_recortes_LR.png"
    csv_salida_path = carpeta / f"{ruta.stem}_validacion.csv"

    celdas_registros = extraer_grilla(ruta)
    recortes_imagenes = []
    resumen = {"planilla": ruta.name, "filas": len(celdas_registros), "vacias": 0,
               "correctos": 0, "libres": 0, "recuperan": 0,
               "imagen": None, "csv": csv_salida_path}

    for idx, fila_celdas in enumerate(celdas_registros):
        validacion = validar_fila(fila_celdas)
        es_valido_total = all(validacion)
        # Para el resumen de 2.d: una fila sin ningún carácter en sus seis campos está vacía.
        if all(contar_caracteres_y_palabras(celda)[0] == 0 for celda in fila_celdas):
            resumen["vacias"] += 1

        # Apartado 2.a
        str_resultados = ["OK" if v else "MAL" for v in validacion]
        print(f"> Registro {idx + 1}:")
        print(f"> Legajo: {str_resultados[0]}")
        print(f"> Nombre y apellido: {str_resultados[1]}")
        print(f"> Parcial 1: {str_resultados[2]}")
        print(f"> Parcial 2: {str_resultados[3]}")
        print(f"> Parcial 3: {str_resultados[4]}")
        print(f"> Condición Final: {str_resultados[5]}\n")
        
        # Apartado 2.b
        if es_valido_total:
            resumen["correctos"] += 1
            condicion = clasificar_condicion(fila_celdas[5])
            if condicion in ['L', 'R']:
                resumen["libres" if condicion == 'L' else "recuperan"] += 1
                nombre_color = cv2.cvtColor(fila_celdas[1], cv2.COLOR_GRAY2BGR)
                color_borde = (255, 0, 0) if condicion == 'L' else (0, 0, 255) # Azul Libre, Rojo Recupera
                nombre_con_borde = cv2.copyMakeBorder(
                    nombre_color, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=color_borde
                )
                recortes_imagenes.append(nombre_con_borde)

    if recortes_imagenes:
        ancho_max = max(img.shape[1] for img in recortes_imagenes)
        recortes_unificados = []
        for img in recortes_imagenes:
            ancho_faltante = ancho_max - img.shape[1]
            if ancho_faltante > 0:
                img = cv2.copyMakeBorder(img, 0, 0, 0, ancho_faltante, cv2.BORDER_CONSTANT, value=(200, 200, 200))
            recortes_unificados.append(img)
            
        collage_final = np.vstack(recortes_unificados)
        # Igual que en la lectura: codificamos con OpenCV y escribimos con NumPy por las tildes.
        ok, png = cv2.imencode(".png", collage_final)
        if not ok:
            raise OSError(f"No se pudo guardar la imagen: {img_salida_path}")
        png.tofile(str(img_salida_path))
        resumen["imagen"] = img_salida_path
        print(f"Apartado 2.b: Imagen de recortes guardada en {img_salida_path}")
    else:
        print("Apartado 2.b: no hay registros correctos con condición L o R; no se genera imagen.")
        
    generar_csv_resultados(celdas_registros, csv_salida_path)
    return resumen


if __name__ == "__main__":
    # Procesa una sola planilla; procesar_planillas.py recorre las cuatro (apartado 2.d).
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--imagen", type=Path, required=True)
    parser.add_argument("--salida", type=Path, default=None)
    args = parser.parse_args()
    procesar_planilla(args.imagen, args.salida)
