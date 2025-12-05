"""
Pruebas de Caja Blanca para el módulo de Procesamiento
======================================================
Estas pruebas demuestran el enfoque de Caja Blanca (White Box Testing).

Objetivo: Cubrir todas las rutas de ejecución, decisiones y ramas del código.
Se enfocan en la estructura interna y la lógica del programa.

Métricas clave:
- Cobertura de líneas (Line Coverage)
- Cobertura de ramas (Branch Coverage)
- Cobertura de rutas (Path Coverage)
- Complejidad ciclomática
"""

import pytest
from src.procesamiento import (
    clasificar_edad,
    calcular_descuento,
    buscar_elemento,
    validar_contrasena,
    procesar_calificacion
)


class TestClasificarEdadCajaBlanca:
    """
    Tests de caja blanca para clasificar_edad.
    Objetivo: Cubrir todas las 7 rutas posibles.
    Complejidad ciclomática = 5
    """
    
    def test_ruta_edad_negativa(self):
        """Ruta 1: Validación de edad negativa"""
        with pytest.raises(ValueError, match="no puede ser negativa"):
            clasificar_edad(-1)
    
    def test_ruta_edad_fuera_rango(self):
        """Ruta 2: Validación de edad > 150"""
        with pytest.raises(ValueError, match="no puede ser mayor a 150"):
            clasificar_edad(200)
    
    def test_ruta_bebe(self):
        """Ruta 3: Clasificación como Bebé (edad < 3)"""
        assert clasificar_edad(0) == "Bebé"
        assert clasificar_edad(2) == "Bebé"
    
    def test_ruta_nino(self):
        """Ruta 4: Clasificación como Niño (3 <= edad < 13)"""
        assert clasificar_edad(3) == "Niño"
        assert clasificar_edad(12) == "Niño"
    
    def test_ruta_adolescente(self):
        """Ruta 5: Clasificación como Adolescente (13 <= edad < 18)"""
        assert clasificar_edad(13) == "Adolescente"
        assert clasificar_edad(17) == "Adolescente"
    
    def test_ruta_adulto(self):
        """Ruta 6: Clasificación como Adulto (18 <= edad < 65)"""
        assert clasificar_edad(18) == "Adulto"
        assert clasificar_edad(64) == "Adulto"
    
    def test_ruta_anciano(self):
        """Ruta 7: Clasificación como Anciano (edad >= 65)"""
        assert clasificar_edad(65) == "Anciano"
        assert clasificar_edad(100) == "Anciano"
    
    def test_valores_limite(self):
        """
        Test de valores límite (boundary values).
        Complementa las pruebas de caja blanca.
        """
        assert clasificar_edad(0) == "Bebé"
        assert clasificar_edad(2) == "Bebé"
        assert clasificar_edad(3) == "Niño"
        assert clasificar_edad(12) == "Niño"
        assert clasificar_edad(13) == "Adolescente"
        assert clasificar_edad(17) == "Adolescente"
        assert clasificar_edad(18) == "Adulto"
        assert clasificar_edad(64) == "Adulto"
        assert clasificar_edad(65) == "Anciano"
        assert clasificar_edad(150) == "Anciano"


class TestCalcularDescuentoCajaBlanca:
    """
    Tests de caja blanca para calcular_descuento.
    Objetivo: Cubrir todas las combinaciones de condiciones.
    Complejidad ciclomática = 6
    """
    
    def test_ruta_precio_invalido(self):
        """Ruta: Validación de precio <= 0"""
        with pytest.raises(ValueError, match="precio debe ser mayor a cero"):
            calcular_descuento(0, False, 5)
    
    def test_ruta_cantidad_invalida(self):
        """Ruta: Validación de cantidad <= 0"""
        with pytest.raises(ValueError, match="cantidad debe ser mayor a cero"):
            calcular_descuento(100, False, 0)
    
    def test_ruta_sin_descuentos(self):
        """Ruta: Cliente NO miembro, cantidad < 10"""
        # Sin descuentos aplicables
        resultado = calcular_descuento(100, False, 5)
        assert resultado == 500.0  # 100 * 5, sin descuento
    
    def test_ruta_solo_descuento_miembro(self):
        """Ruta: Cliente miembro, sin otros descuentos"""
        # Descuento: 10% (miembro)
        resultado = calcular_descuento(100, True, 5)
        assert resultado == 450.0  # 500 * 0.90
    
    def test_ruta_miembro_y_precio_alto(self):
        """Ruta: Cliente miembro + total > 1000"""
        # Descuento: 10% (miembro) + 5% (precio alto) = 15%
        resultado = calcular_descuento(300, True, 4)
        # Total = 1200, descuento = 15%, final = 1020
        assert resultado == 1020.0
    
    def test_ruta_cantidad_media(self):
        """Ruta: Cantidad >= 10 y < 20"""
        # Descuento: 5% (volumen)
        resultado = calcular_descuento(100, False, 10)
        assert resultado == 950.0  # 1000 * 0.95
    
    def test_ruta_cantidad_alta(self):
        """Ruta: Cantidad >= 20"""
        # Descuento: 10% (volumen alto)
        resultado = calcular_descuento(100, False, 20)
        assert resultado == 1800.0  # 2000 * 0.90
    
    def test_ruta_todas_condiciones(self):
        """Ruta: Miembro + precio alto + cantidad alta"""
        # Descuento: 10% (miembro) + 5% (precio alto) + 10% (volumen) = 25%
        resultado = calcular_descuento(100, True, 20)
        # Total = 2000, descuento = 25%, final = 1500
        assert resultado == 1500.0
    
    def test_ruta_miembro_cantidad_media(self):
        """Ruta: Miembro + cantidad media (10-19)"""
        # Descuento: 10% (miembro) + 5% (volumen) = 15%
        resultado = calcular_descuento(100, True, 10)
        assert resultado == 850.0  # 1000 * 0.85


class TestBuscarElementoCajaBlanca:
    """
    Tests de caja blanca para buscar_elemento.
    Objetivo: Cubrir todas las rutas (lista vacía, encontrado, no encontrado).
    """
    
    def test_ruta_lista_vacia(self):
        """Ruta 1: Lista vacía"""
        resultado = buscar_elemento([], 5)
        assert resultado == -1
    
    def test_ruta_elemento_encontrado_inicio(self):
        """Ruta 2: Elemento encontrado en la primera posición"""
        resultado = buscar_elemento([10, 20, 30], 10)
        assert resultado == 0
    
    def test_ruta_elemento_encontrado_medio(self):
        """Ruta 2: Elemento encontrado en el medio"""
        resultado = buscar_elemento([10, 20, 30], 20)
        assert resultado == 1
    
    def test_ruta_elemento_encontrado_final(self):
        """Ruta 2: Elemento encontrado al final"""
        resultado = buscar_elemento([10, 20, 30], 30)
        assert resultado == 2
    
    def test_ruta_elemento_no_encontrado(self):
        """Ruta 3: Elemento no encontrado"""
        resultado = buscar_elemento([10, 20, 30], 40)
        assert resultado == -1


class TestValidarContrasenaCajaBlanca:
    """
    Tests de caja blanca para validar_contrasena.
    Objetivo: Cubrir todas las combinaciones de validaciones.
    Complejidad ciclomática = 6
    """
    
    def test_ruta_contrasena_valida(self):
        """Ruta: Contraseña que cumple todos los criterios"""
        es_valida, errores = validar_contrasena("Abc123!@")
        assert es_valida is True
        assert len(errores) == 0
    
    def test_ruta_longitud_insuficiente(self):
        """Ruta: Falla validación de longitud"""
        es_valida, errores = validar_contrasena("Abc1!")
        assert es_valida is False
        assert any("8 caracteres" in error for error in errores)
    
    def test_ruta_sin_mayusculas(self):
        """Ruta: Falla validación de mayúsculas"""
        es_valida, errores = validar_contrasena("abc12345!")
        assert es_valida is False
        assert any("mayúscula" in error for error in errores)
    
    def test_ruta_sin_minusculas(self):
        """Ruta: Falla validación de minúsculas"""
        es_valida, errores = validar_contrasena("ABC12345!")
        assert es_valida is False
        assert any("minúscula" in error for error in errores)
    
    def test_ruta_sin_digitos(self):
        """Ruta: Falla validación de dígitos"""
        es_valida, errores = validar_contrasena("Abcdefgh!")
        assert es_valida is False
        assert any("dígito" in error for error in errores)
    
    def test_ruta_sin_caracteres_especiales(self):
        """Ruta: Falla validación de caracteres especiales"""
        es_valida, errores = validar_contrasena("Abcd1234")
        assert es_valida is False
        assert any("carácter especial" in error for error in errores)
    
    def test_ruta_multiples_fallos(self):
        """Ruta: Múltiples validaciones fallan"""
        es_valida, errores = validar_contrasena("abc")
        assert es_valida is False
        assert len(errores) >= 3  # Al menos 3 errores


class TestProcesarCalificacionCajaBlanca:
    """
    Tests de caja blanca para procesar_calificacion.
    Objetivo: Cubrir todas las 6 rutas de decisión.
    """
    
    def test_ruta_nota_invalida_baja(self):
        """Ruta: Validación de nota < 0"""
        with pytest.raises(ValueError, match="debe estar entre 0 y 100"):
            procesar_calificacion(-1)
    
    def test_ruta_nota_invalida_alta(self):
        """Ruta: Validación de nota > 100"""
        with pytest.raises(ValueError, match="debe estar entre 0 y 100"):
            procesar_calificacion(101)
    
    def test_ruta_calificacion_a(self):
        """Ruta: Nota >= 90 (Calificación A)"""
        assert procesar_calificacion(90) == "A"
        assert procesar_calificacion(100) == "A"
    
    def test_ruta_calificacion_b(self):
        """Ruta: 80 <= Nota < 90 (Calificación B)"""
        assert procesar_calificacion(80) == "B"
        assert procesar_calificacion(89) == "B"
    
    def test_ruta_calificacion_c(self):
        """Ruta: 70 <= Nota < 80 (Calificación C)"""
        assert procesar_calificacion(70) == "C"
        assert procesar_calificacion(79) == "C"
    
    def test_ruta_calificacion_d(self):
        """Ruta: 60 <= Nota < 70 (Calificación D)"""
        assert procesar_calificacion(60) == "D"
        assert procesar_calificacion(69) == "D"
    
    def test_ruta_calificacion_f(self):
        """Ruta: Nota < 60 (Calificación F)"""
        assert procesar_calificacion(0) == "F"
        assert procesar_calificacion(59) == "F"
    
    def test_valores_limite_completo(self):
        """Test de todos los valores límite"""
        assert procesar_calificacion(0) == "F"
        assert procesar_calificacion(59) == "F"
        assert procesar_calificacion(60) == "D"
        assert procesar_calificacion(69) == "D"
        assert procesar_calificacion(70) == "C"
        assert procesar_calificacion(79) == "C"
        assert procesar_calificacion(80) == "B"
        assert procesar_calificacion(89) == "B"
        assert procesar_calificacion(90) == "A"
        assert procesar_calificacion(100) == "A"
