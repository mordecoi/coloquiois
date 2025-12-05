"""
Pruebas de Unidad para el módulo Calculadora
============================================
Estas pruebas demuestran el concepto de Unit Testing (Pruebas de Unidad).
Cada función se prueba de manera aislada verificando su comportamiento.
"""

import pytest
from src.calculadora import sumar, restar, multiplicar, dividir, potencia, factorial


class TestOperacionesBasicas:
    """Tests para operaciones matemáticas básicas"""
    
    def test_sumar_numeros_positivos(self):
        """Verifica que la suma de números positivos funcione correctamente"""
        assert sumar(2, 3) == 5
        assert sumar(10, 20) == 30
        assert sumar(0.5, 0.5) == 1.0
    
    def test_sumar_numeros_negativos(self):
        """Verifica que la suma con números negativos funcione correctamente"""
        assert sumar(-5, -3) == -8
        assert sumar(-10, 5) == -5
        assert sumar(10, -10) == 0
    
    def test_restar(self):
        """Verifica que la resta funcione correctamente"""
        assert restar(10, 5) == 5
        assert restar(5, 10) == -5
        assert restar(0, 0) == 0
    
    def test_multiplicar(self):
        """Verifica que la multiplicación funcione correctamente"""
        assert multiplicar(3, 4) == 12
        assert multiplicar(-2, 5) == -10
        assert multiplicar(0, 100) == 0
        assert multiplicar(0.5, 4) == 2.0
    
    def test_dividir_numeros_validos(self):
        """Verifica que la división con números válidos funcione correctamente"""
        assert dividir(10, 2) == 5
        assert dividir(15, 3) == 5
        assert dividir(7, 2) == 3.5
    
    def test_dividir_por_cero_lanza_excepcion(self):
        """Verifica que dividir por cero lance una excepción ValueError"""
        with pytest.raises(ValueError, match="No se puede dividir por cero"):
            dividir(10, 0)


class TestOperacionesAvanzadas:
    """Tests para operaciones matemáticas avanzadas"""
    
    def test_potencia_exponente_positivo(self):
        """Verifica que la potencia con exponente positivo funcione correctamente"""
        assert potencia(2, 3) == 8
        assert potencia(5, 2) == 25
        assert potencia(10, 0) == 1
    
    def test_potencia_exponente_negativo(self):
        """Verifica que la potencia con exponente negativo funcione correctamente"""
        assert potencia(2, -1) == 0.5
        assert potencia(10, -2) == 0.01
    
    def test_factorial_casos_base(self):
        """Verifica que el factorial de 0 y 1 sea 1"""
        assert factorial(0) == 1
        assert factorial(1) == 1
    
    def test_factorial_numeros_positivos(self):
        """Verifica que el factorial de números positivos funcione correctamente"""
        assert factorial(5) == 120
        assert factorial(4) == 24
        assert factorial(3) == 6
    
    def test_factorial_numero_negativo_lanza_excepcion(self):
        """Verifica que el factorial de un número negativo lance una excepción"""
        with pytest.raises(ValueError, match="no está definido para números negativos"):
            factorial(-1)


# Fixture de ejemplo (setup/teardown)
@pytest.fixture
def calculadora_inicializada():
    """
    Fixture que demuestra el concepto de setup/teardown en pruebas.
    En un caso real, esto podría inicializar recursos compartidos.
    """
    print("\n[SETUP] Preparando entorno de prueba")
    datos = {"resultado": 0}
    yield datos
    print("\n[TEARDOWN] Limpiando entorno de prueba")


def test_con_fixture(calculadora_inicializada):
    """Ejemplo de test que usa un fixture"""
    calculadora_inicializada["resultado"] = sumar(5, 3)
    assert calculadora_inicializada["resultado"] == 8
