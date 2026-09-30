"""Problema 1.a: ecualización por histograma de una ventana móvil.

Referencias: Unidad 2, páginas 8, 9, 13 y 15; enunciado, página 1.
"""

from numbers import Integral

import cv2
import numpy as np


def ecualizacion_local(imagen, tamano_ventana):
    """Devuelve una imagen en gris uint8 ecualizada píxel por píxel.

    imagen: matriz no vacía de tipo uint8, con intensidades entre 0 y 255.
    tamano_ventana: (M, N), cantidad de filas y columnas, enteros positivos.
    En ventanas pares, se toma como centro el índice (M // 2, N // 2).
    La entrada no se modifica y la salida conserva sus dimensiones.
    """
    # Unidad 1, páginas 3 y 14: imagen de un canal representada como matriz uint8.
    if not isinstance(imagen, np.ndarray):
        raise ValueError("La imagen debe ser un arreglo de NumPy.")
    if imagen.ndim != 2 or imagen.size == 0 or imagen.dtype != np.uint8:
        raise ValueError("La imagen debe ser una matriz no vacía en gris de tipo uint8.")

    # El enunciado pide M y N enteros positivos; se aceptan pares e impares.
    if not isinstance(tamano_ventana, (tuple, list)) or len(tamano_ventana) != 2:
        raise ValueError("El tamaño de ventana debe ser (M, N).")
    for dimension in tamano_ventana:
        if isinstance(dimension, (bool, np.bool_)) or not isinstance(dimension, Integral):
            raise ValueError("M y N deben ser enteros positivos.")
        if dimension <= 0:
            raise ValueError("M y N deben ser enteros positivos.")
    m, n = (int(dimension) for dimension in tamano_ventana)

    # Ubicamos el píxel que se actualizará dentro de la ventana.
    arriba, izquierda = m // 2, n // 2
    # Restamos el centro: el borde agregado total debe ser M-1 por N-1.
    abajo, derecha = m - 1 - arriba, n - 1 - izquierda
    # AYUDA del enunciado, página 1: replicamos los valores del borde.
    imagen_con_borde = cv2.copyMakeBorder(
        imagen, arriba, abajo, izquierda, derecha, cv2.BORDER_REPLICATE
    )
    # Guardamos los resultados separados para no alterar las ventanas siguientes.
    salida = np.zeros_like(imagen)
    filas, columnas = imagen.shape

    # Enunciado, página 1: desplazamos la ventana un píxel en cada posición.
    for fila in range(filas):
        for columna in range(columnas):
            # Unidad 1, página 12: obtenemos una región por indexado de la matriz.
            ventana = imagen_con_borde[fila:fila + m, columna:columna + n]
            # Unidad 2, página 9: contamos los píxeles de cada nivel de intensidad.
            histograma, _ = np.histogram(ventana.flatten(), 256, [0, 256])
            # Unidad 2, páginas 9 y 15: dividimos por los M*N píxeles de la ventana.
            histograma_normalizado = histograma.astype(np.double) / ventana.size
            # Unidad 2, páginas 13 y 15: acumulamos las probabilidades (CDF).
            acumulada = histograma_normalizado.cumsum()
            # Aplicamos la transformación solamente al valor del píxel central.
            intensidad = imagen[fila, columna]
            # Pasamos de [0, 1] a [0, 255] y redondeamos al entero más cercano.
            salida[fila, columna] = int(255 * acumulada[intensidad] + 0.5)

    return salida
