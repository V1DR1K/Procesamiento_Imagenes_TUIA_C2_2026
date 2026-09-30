"""Problema 1.c: comparar tamaños y formas de la ventana de procesamiento."""

import argparse
import csv
from pathlib import Path
from time import perf_counter

# Reutilizamos la lectura y la referencia global del apartado b.
from analizar_imagen import IMAGEN, RAIZ, ZONAS, ecualizacion_global, guardar_imagen, leer_imagen
import matplotlib.pyplot as plt

from ecualizacion import ecualizacion_local


# Los cuadrados muestran la influencia del tamaño; los rectángulos, la orientación.
# 1x1 es el caso límite y 4x6 permite observar también una ventana par.
VENTANAS = [(1, 1), (3, 3), (7, 7), (15, 15), (31, 31), (63, 63),
            (127, 127), (7, 31), (31, 7), (4, 6)]


def comparar_ventanas(ruta_imagen=IMAGEN, carpeta_salida=None):
    imagen = leer_imagen(ruta_imagen)
    carpeta = Path(carpeta_salida) if carpeta_salida is not None else RAIZ / "resultados" / "c"
    carpeta.mkdir(parents=True, exist_ok=True)
    resultados = {}
    tiempos = []

    # Todas las ventanas procesan la misma entrada, conservando el borde replicado.
    for m, n in VENTANAS:
        inicio = perf_counter()
        resultado = ecualizacion_local(imagen, (m, n))
        segundos = perf_counter() - inicio
        resultados[(m, n)] = resultado
        tiempos.append((m, n, m * n, f"{segundos:.6f}"))
        guardar_imagen(carpeta / f"local_{m}x{n}.png", resultado)
        print(f"Ventana {m}x{n}: {segundos:.2f} segundos", flush=True)

    # Este CSV registra el tiempo del cálculo, sin incluir escritura ni figuras.
    with (carpeta / "tiempos.csv").open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["M_filas", "N_columnas", "pixeles_ventana", "segundos"])
        escritor.writerows(tiempos)

    # Unidad 1, páginas 6 y 7: comparamos siempre con escala de gris fija 0 a 255.
    paneles = [("Original", imagen), ("Global", ecualizacion_global(imagen))]
    paneles += [(f"Local {m}x{n}", resultados[(m, n)]) for m, n in VENTANAS]
    figura, ejes = plt.subplots(3, 4, figsize=(12, 10))
    for eje, (titulo, resultado) in zip(ejes.flatten(), paneles):
        eje.imshow(resultado, cmap="gray", vmin=0, vmax=255)
        eje.set_title(titulo)
        eje.axis("off")
    figura.suptitle("Influencia del tamaño y la forma de la ventana")
    figura.tight_layout()
    figura.savefig(carpeta / "comparacion_ventanas.png", dpi=150)
    plt.close(figura)

    # M*N es igual para estos dos rectángulos: cambia solamente su orientación.
    figura, ejes = plt.subplots(1, 3, figsize=(10, 4))
    for eje, ventana in zip(ejes, [(15, 15), (7, 31), (31, 7)]):
        eje.imshow(resultados[ventana], cmap="gray", vmin=0, vmax=255)
        eje.set_title(f"Local {ventana[0]}x{ventana[1]}")
        eje.axis("off")
    figura.tight_layout()
    figura.savefig(carpeta / "comparacion_rectangulares.png", dpi=150)
    plt.close(figura)

    if imagen.shape == (256, 256):
        # Unidad 1, página 12: ampliamos los recortes de las cinco zonas conocidas.
        seleccion = [(3, 3), (15, 15), (31, 31), (63, 63), (127, 127)]
        figura, ejes = plt.subplots(5, 5, figsize=(12, 12))
        for fila, (nombre, (f0, f1, c0, c1)) in enumerate(ZONAS):
            for columna, (m, n) in enumerate(seleccion):
                recorte = resultados[(m, n)][f0:f1, c0:c1]
                ejes[fila, columna].imshow(recorte, cmap="gray", vmin=0, vmax=255)
                ejes[fila, columna].set_title(f"{nombre}\nLocal {m}x{n}", fontsize=9)
                ejes[fila, columna].axis("off")
        figura.tight_layout()
        figura.savefig(carpeta / "comparacion_zonas.png", dpi=150)
        plt.close(figura)
    print(f"Apartado c: resultados guardados en {carpeta}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--imagen", type=Path, default=IMAGEN)
    parser.add_argument("--salida", type=Path, default=RAIZ / "resultados" / "c")
    args = parser.parse_args()
    comparar_ventanas(args.imagen, args.salida)
