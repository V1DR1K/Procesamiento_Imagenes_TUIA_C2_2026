"""Problema 1.b: aplicar la función e inspeccionar los detalles ocultos."""

import argparse
from pathlib import Path

import cv2
import matplotlib
import numpy as np

# Guardamos las figuras sin necesitar una ventana gráfica abierta.
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ecualizacion import ecualizacion_local


# Las rutas predeterminadas se resuelven desde el repositorio, no desde la terminal.
RAIZ = Path(__file__).resolve().parent
IMAGEN = RAIZ / "datos" / "Imagen_con_detalles_escondidos.tif"
# Unidad 1, página 12: recortes con coordenadas (fila inicial, final, columna inicial, final).
ZONAS = [
    ("Superior izquierda", (6, 68, 6, 68)),
    ("Superior derecha", (6, 68, 187, 249)),
    ("Centro", (97, 159, 97, 159)),
    ("Inferior izquierda", (188, 250, 6, 68)),
    ("Inferior derecha", (188, 250, 187, 249)),
]


def leer_imagen(ruta):
    # Unidad 1, página 5: lectura de la imagen como una matriz de niveles de gris.
    imagen = cv2.imread(str(ruta), cv2.IMREAD_GRAYSCALE)
    if imagen is None:
        raise ValueError(f"No se pudo leer la imagen: {ruta}")
    return imagen


def guardar_imagen(ruta, imagen):
    # Unidad 1, página 8: PNG conserva los valores de intensidad sin pérdida.
    if not cv2.imwrite(str(ruta), imagen):
        raise OSError(f"No se pudo guardar la imagen: {ruta}")


def ecualizacion_global(imagen):
    # Unidad 2, páginas 9, 13 y 15: la misma CDF, usando toda la imagen.
    histograma, _ = np.histogram(imagen.flatten(), 256, [0, 256])
    acumulada = (histograma.astype(np.double) / imagen.size).cumsum()
    # Usamos el mismo redondeo del apartado a para comparar ambos alcances.
    tabla = (255 * acumulada + 0.5).astype(np.uint8)
    return tabla[imagen]


def analizar_imagen(ruta_imagen=IMAGEN, ventana=(15, 15), carpeta_salida=None):
    imagen = leer_imagen(ruta_imagen)
    # Se llama a la función propia del apartado a; no a una ecualización local de OpenCV.
    local = ecualizacion_local(imagen, ventana)
    global_ = ecualizacion_global(imagen)
    carpeta = Path(carpeta_salida) if carpeta_salida is not None else RAIZ / "resultados" / "b"
    carpeta.mkdir(parents=True, exist_ok=True)
    m, n = ventana
    guardar_imagen(carpeta / "original.png", imagen)
    guardar_imagen(carpeta / "global.png", global_)
    guardar_imagen(carpeta / f"local_{m}x{n}.png", local)

    # Unidad 2, página 14: visualización de las imágenes junto a sus histogramas.
    figura, ejes = plt.subplots(2, 3, figsize=(11, 7))
    for columna, (titulo, resultado) in enumerate([
        ("Original", imagen), ("Ecualización global", global_), (f"Local {m}x{n}", local)
    ]):
        # Unidad 1, páginas 6 y 7: una escala fija evita falsear la comparación.
        ejes[0, columna].imshow(resultado, cmap="gray", vmin=0, vmax=255)
        ejes[0, columna].set_title(titulo)
        ejes[0, columna].axis("off")
        ejes[1, columna].hist(resultado.flatten(), bins=256, range=(0, 256))
        ejes[1, columna].set_xlim(0, 255)
        ejes[1, columna].set_xlabel("Intensidad")
        ejes[1, columna].set_ylabel("Cantidad de píxeles")
    figura.tight_layout()
    figura.savefig(carpeta / "comparacion_histogramas.png", dpi=150)
    plt.close(figura)

    # Los recortes facilitan la inspección visual; no detectan objetos automáticamente.
    if imagen.shape == (256, 256):
        figura, ejes = plt.subplots(2, 5, figsize=(13, 6))
        for columna, (nombre, (f0, f1, c0, c1)) in enumerate(ZONAS):
            for fila, resultado in enumerate([imagen, local]):
                recorte = resultado[f0:f1, c0:c1]
                ejes[fila, columna].imshow(recorte, cmap="gray", vmin=0, vmax=255)
                ejes[fila, columna].set_title(nombre if fila == 0 else f"Local {m}x{n}")
                ejes[fila, columna].axis("off")
        figura.suptitle("Cinco zonas de la imagen: original arriba, ecualización local abajo")
        figura.tight_layout()
        figura.savefig(carpeta / "zonas.png", dpi=150)
        plt.close(figura)
    print(f"Apartado b: resultados guardados en {carpeta}")


if __name__ == "__main__":
    # Los argumentos permiten repetir el análisis con otra ventana o ruta de entrada.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--imagen", type=Path, default=IMAGEN)
    parser.add_argument("--ventana", nargs=2, type=int, default=(15, 15), metavar=("M", "N"))
    parser.add_argument("--salida", type=Path, default=RAIZ / "resultados" / "b")
    args = parser.parse_args()
    analizar_imagen(args.imagen, tuple(args.ventana), args.salida)
