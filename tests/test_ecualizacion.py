"""Verificaciones del apartado a, sin bibliotecas adicionales de pruebas."""

import unittest

import numpy as np

from ecualizacion import ecualizacion_local


class PruebasEcualizacionLocal(unittest.TestCase):
    def test_ventana_3x3_coincide_con_calculo_manual(self):
        imagen = np.array([[0, 10], [20, 30]], dtype=np.uint8)
        # Con borde replicado, los conteos acumulados son 4, 6, 7 y 9 sobre 9.
        esperado = np.array([[113, 170], [198, 255]], dtype=np.uint8)
        self.assertTrue(np.array_equal(ecualizacion_local(imagen, (3, 3)), esperado))

    def test_ventanas_coinciden_con_conteo_directo(self):
        imagen = np.array([[20, 5, 20], [0, 255, 10]], dtype=np.uint8)
        original = imagen.copy()
        # Contrastamos pares, impares, rectangulares y ventanas mayores que la imagen.
        for m, n in [(1, 1), (1, 3), (3, 1), (2, 2), (2, 4), (3, 5), (8, 9)]:
            with self.subTest(ventana=(m, n)):
                salida = ecualizacion_local(imagen, (m, n))
                self.assertEqual(salida.shape, imagen.shape)
                self.assertEqual(salida.dtype, np.uint8)
                for fila in range(imagen.shape[0]):
                    for columna in range(imagen.shape[1]):
                        cantidad = 0
                        # Cálculo independiente: no usamos histograma ni copyMakeBorder.
                        for i in range(fila - m // 2, fila - m // 2 + m):
                            for j in range(columna - n // 2, columna - n // 2 + n):
                                # Limitar los índices equivale a replicar el borde.
                                y = min(max(i, 0), imagen.shape[0] - 1)
                                x = min(max(j, 0), imagen.shape[1] - 1)
                                if imagen[y, x] <= imagen[fila, columna]:
                                    cantidad += 1
                        esperado = int(255 * cantidad / (m * n) + 0.5)
                        self.assertEqual(int(salida[fila, columna]), esperado)
                self.assertTrue(np.array_equal(imagen, original))

    def test_imagen_uniforme_y_ventana_1x1_dan_blanco(self):
        # La fórmula directa acumula probabilidad 1 en el nivel observado.
        for intensidad in [0, 70, 255]:
            imagen = np.full((2, 3), intensidad, dtype=np.uint8)
            self.assertTrue(np.all(ecualizacion_local(imagen, (3, 3)) == 255))
        imagen = np.array([[0, 10, 255]], dtype=np.uint8)
        self.assertTrue(np.all(ecualizacion_local(imagen, (1, 1)) == 255))

    def test_entrada_invalida_se_rechaza(self):
        imagen = np.zeros((2, 2), dtype=np.uint8)
        for ventana in [None, 3, (3,), (3, 3, 3), (0, 3), (-1, 3), (2.5, 3), (True, 3)]:
            with self.subTest(ventana=ventana), self.assertRaises(ValueError):
                ecualizacion_local(imagen, ventana)
        for entrada in [None, [[1]], np.zeros((0, 2), dtype=np.uint8),
                        np.zeros((2, 2, 3), dtype=np.uint8), np.zeros((2, 2))]:
            with self.subTest(entrada=str(type(entrada))), self.assertRaises(ValueError):
                ecualizacion_local(entrada, (3, 3))


if __name__ == "__main__":
    unittest.main()
