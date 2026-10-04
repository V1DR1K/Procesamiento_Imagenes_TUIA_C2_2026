"""Problema 2.d: aplicar la validación, de forma cíclica, a las cuatro planillas."""

import argparse
from pathlib import Path
import re

from validar_planilla import SALIDAS_TEMPORALES, procesar_planilla


# Enunciado, página 3: los archivos se llaman grade_sheet_<id>.png.
# La planilla vacía (grade_sheet_empty.png) no tiene un id numérico y queda excluida.
PATRON = re.compile(r"grade_sheet_(\d+)\.png$", re.IGNORECASE)


def buscar_planillas(carpeta):
    """Devuelve las planillas con registros, ordenadas por su id numérico."""
    encontradas = []
    for ruta in Path(carpeta).iterdir():
        coincidencia = PATRON.match(ruta.name)
        if coincidencia:
            encontradas.append((int(coincidencia.group(1)), ruta))
    # Ordenamos por número para que grade_sheet_10 no quede antes que grade_sheet_2.
    return [ruta for _, ruta in sorted(encontradas)]


def procesar_planillas(carpeta_planillas, carpeta_salida=None):
    planillas = buscar_planillas(carpeta_planillas)
    if not planillas:
        raise FileNotFoundError(f"No hay archivos grade_sheet_<id>.png en {carpeta_planillas}")
    salida = Path(carpeta_salida) if carpeta_salida is not None else SALIDAS_TEMPORALES / "planillas"

    # Apartado 2.d: el mismo algoritmo de 2.a, 2.b y 2.c se repite para cada planilla.
    resumenes = []
    for ruta in planillas:
        print(f"===== {ruta.name} =====")
        # Cada planilla guarda su imagen y su CSV en una subcarpeta propia.
        resumenes.append(procesar_planilla(ruta, salida / ruta.stem))
        print()

    # Informe final con los resultados de todas las planillas.
    print("===== Resumen del apartado 2.d =====")
    # Las filas vacías se informan aparte; "Con datos" son los registros cargados.
    print(f"{'Planilla':<20}{'Filas':>6}{'Vacías':>8}{'Con datos':>11}{'Correctos':>11}"
          f"{'Con MAL':>9}{'Libres':>8}{'Recuperan':>11}")
    for r in resumenes:
        con_datos = r["filas"] - r["vacias"]
        con_errores = con_datos - r["correctos"]
        print(f"{r['planilla']:<20}{r['filas']:>6}{r['vacias']:>8}{con_datos:>11}{r['correctos']:>11}"
              f"{con_errores:>9}{r['libres']:>8}{r['recuperan']:>11}")
    print(f"Resultados guardados en {salida}")
    return resumenes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--carpeta", type=Path, required=True,
                        help="Carpeta que contiene los archivos grade_sheet_<id>.png")
    parser.add_argument("--salida", type=Path, default=SALIDAS_TEMPORALES / "planillas")
    args = parser.parse_args()
    procesar_planillas(args.carpeta, args.salida)
