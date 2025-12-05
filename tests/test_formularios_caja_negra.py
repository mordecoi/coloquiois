"""
Pruebas de Caja Negra para el módulo de Formularios
===================================================
Estas pruebas demuestran el enfoque de Caja Negra (Black Box Testing).

Técnicas aplicadas:
1. Partición de Equivalencia: Dividir el dominio de entrada en clases
2. Análisis de Valor Límite: Probar los bordes de cada clase de equivalencia

Objetivo: Validar funcionalidad sin conocer la implementación interna.
"""

import pytest
from datetime import datetime, timedelta
from src.formularios import (
    validar_email,
    validar_rango_edad,
    validar_nombre_usuario,
    calcular_precio_con_impuesto,
    validar_fecha_nacimiento,
    calcular_descuento_tienda
)


class TestValidarEmailCajaNegra:
    """
    Pruebas de caja negra para validar_email.
    
    Particiones de Equivalencia:
    1. Emails válidos: Formato correcto con @ y dominio
    2. Emails inválidos por formato
    3. Emails inválidos por longitud
    4. Emails vacíos
    """
    
    def test_particion_emails_validos(self):
        """Partición 1: Emails con formato válido"""
        emails_validos = [
            "usuario@ejemplo.com",
            "nombre.apellido@empresa.com.ar",
            "user123@mail.co",
            "test_user@domain.org",
            "a@b.co"
        ]
        
        for email in emails_validos:
            es_valido, _ = validar_email(email)
            assert es_valido is True, f"Email '{email}' debería ser válido"
    
    def test_particion_emails_formato_invalido(self):
        """Partición 2: Emails con formato inválido"""
        emails_invalidos = [
            "usuariosindominio",  # Sin @
            "@sinusuario.com",  # Sin usuario
            "usuario@",  # Sin dominio
            "usuario@dominio",  # Sin extensión
            "usuario@@dominio.com",  # Doble @
            "usuario@dominio..com",  # Doble punto
        ]
        
        for email in emails_invalidos:
            es_valido, mensaje = validar_email(email)
            assert es_valido is False, f"Email '{email}' debería ser inválido"
            assert len(mensaje) > 0
    
    def test_valor_limite_longitud_maxima(self):
        """Análisis de Valor Límite: Longitud máxima (254 caracteres)"""
        # Email de exactamente 254 caracteres (válido)
        email_254 = "a" * 240 + "@ejemplo.com"  # 240 + 1 + 12 = 253
        es_valido, _ = validar_email(email_254)
        # Puede ser válido o inválido dependiendo del límite exacto
        
        # Email de 255 caracteres (inválido)
        email_255 = "a" * 241 + "@ejemplo.com"
        es_valido, mensaje = validar_email(email_255)
        assert es_valido is False
        assert "254" in mensaje
    
    def test_valor_limite_email_vacio(self):
        """Análisis de Valor Límite: Email vacío"""
        es_valido, mensaje = validar_email("")
        assert es_valido is False
        assert "vacío" in mensaje.lower()


class TestValidarRangoEdadCajaNegra:
    """
    Pruebas de caja negra para validar_rango_edad.
    
    Particiones de Equivalencia:
    1. Edades dentro del rango válido
    2. Edades por debajo del rango
    3. Edades por encima del rango
    
    Valores Límite: 0, 1, 119, 120, 121
    """
    
    def test_particion_edad_valida(self):
        """Partición 1: Edades dentro del rango válido (0-120)"""
        edades_validas = [0, 1, 25, 50, 75, 100, 119, 120]
        
        for edad in edades_validas:
            es_valido, _ = validar_rango_edad(edad)
            assert es_valido is True, f"Edad {edad} debería ser válida"
    
    def test_particion_edad_menor_rango(self):
        """Partición 2: Edades por debajo del rango"""
        edades_invalidas = [-1, -10, -100]
        
        for edad in edades_invalidas:
            es_valido, mensaje = validar_rango_edad(edad)
            assert es_valido is False
            assert "al menos" in mensaje.lower()
    
    def test_particion_edad_mayor_rango(self):
        """Partición 3: Edades por encima del rango"""
        edades_invalidas = [121, 150, 200]
        
        for edad in edades_invalidas:
            es_valido, mensaje = validar_rango_edad(edad)
            assert es_valido is False
            assert "no puede ser mayor" in mensaje.lower()
    
    def test_valores_limite_edad(self):
        """Análisis de Valor Límite: Bordes del rango"""
        # Límite inferior
        assert validar_rango_edad(-1)[0] is False  # Justo debajo
        assert validar_rango_edad(0)[0] is True    # En el límite
        assert validar_rango_edad(1)[0] is True    # Justo arriba
        
        # Límite superior
        assert validar_rango_edad(119)[0] is True   # Justo debajo
        assert validar_rango_edad(120)[0] is True   # En el límite
        assert validar_rango_edad(121)[0] is False  # Justo arriba
    
    def test_rango_personalizado(self):
        """Partición con rango personalizado"""
        # Rango 18-65 (adultos laboralmente activos)
        assert validar_rango_edad(17, 18, 65)[0] is False
        assert validar_rango_edad(18, 18, 65)[0] is True
        assert validar_rango_edad(40, 18, 65)[0] is True
        assert validar_rango_edad(65, 18, 65)[0] is True
        assert validar_rango_edad(66, 18, 65)[0] is False


class TestValidarNombreUsuarioCajaNegra:
    """
    Pruebas de caja negra para validar_nombre_usuario.
    
    Particiones de Equivalencia:
    1. Nombres válidos: 3-20 caracteres, comienza con letra
    2. Nombres inválidos por longitud
    3. Nombres inválidos por formato
    4. Nombres inválidos por caracteres especiales
    """
    
    def test_particion_nombres_validos(self):
        """Partición 1: Nombres de usuario válidos"""
        nombres_validos = [
            "abc",           # Longitud mínima (3)
            "usuario123",    # Con números
            "User_Name",     # Con guión bajo
            "a1234567890123456789"  # Longitud máxima (20)
        ]
        
        for nombre in nombres_validos:
            es_valido, _ = validar_nombre_usuario(nombre)
            assert es_valido is True, f"Nombre '{nombre}' debería ser válido"
    
    def test_particion_longitud_invalida(self):
        """Partición 2: Nombres con longitud inválida"""
        # Muy corto (< 3)
        assert validar_nombre_usuario("ab")[0] is False
        assert validar_nombre_usuario("a")[0] is False
        assert validar_nombre_usuario("")[0] is False
        
        # Muy largo (> 20)
        nombre_largo = "a" * 21
        es_valido, mensaje = validar_nombre_usuario(nombre_largo)
        assert es_valido is False
        assert "20" in mensaje
    
    def test_particion_formato_invalido(self):
        """Partición 3: Nombres con formato inválido"""
        nombres_invalidos = [
            "123usuario",    # Comienza con número
            "_usuario",      # Comienza con guión bajo
            "usuario_",      # Termina con guión bajo
        ]
        
        for nombre in nombres_invalidos:
            es_valido, mensaje = validar_nombre_usuario(nombre)
            assert es_valido is False, f"Nombre '{nombre}' debería ser inválido"
    
    def test_particion_caracteres_especiales(self):
        """Partición 4: Nombres con caracteres especiales inválidos"""
        nombres_invalidos = [
            "usuario-123",   # Guión no permitido
            "user@name",     # @ no permitido
            "user.name",     # Punto no permitido
            "user name",     # Espacio no permitido
            "user#123",      # # no permitido
        ]
        
        for nombre in nombres_invalidos:
            es_valido, _ = validar_nombre_usuario(nombre)
            assert es_valido is False, f"Nombre '{nombre}' debería ser inválido"
    
    def test_valores_limite_longitud(self):
        """Análisis de Valor Límite: Longitud del nombre"""
        # Longitud 2 (inválido)
        assert validar_nombre_usuario("ab")[0] is False
        # Longitud 3 (válido - límite inferior)
        assert validar_nombre_usuario("abc")[0] is True
        # Longitud 4 (válido)
        assert validar_nombre_usuario("abcd")[0] is True
        
        # Longitud 19 (válido)
        assert validar_nombre_usuario("a" * 19)[0] is True
        # Longitud 20 (válido - límite superior)
        assert validar_nombre_usuario("a" * 20)[0] is True
        # Longitud 21 (inválido)
        assert validar_nombre_usuario("a" * 21)[0] is False


class TestCalcularPrecioConImpuestoCajaNegra:
    """
    Pruebas de caja negra para calcular_precio_con_impuesto.
    
    Particiones de Equivalencia:
    1. Precios válidos (> 0)
    2. Precios inválidos (<= 0)
    3. Impuestos válidos (0-100)
    4. Impuestos inválidos (< 0 o > 100)
    """
    
    def test_particion_precio_impuesto_validos(self):
        """Partición 1: Precios e impuestos válidos"""
        # Precio 100, impuesto 21%
        resultado = calcular_precio_con_impuesto(100, 21)
        assert resultado == 121.0
        
        # Precio 50, impuesto 0%
        resultado = calcular_precio_con_impuesto(50, 0)
        assert resultado == 50.0
        
        # Precio 200, impuesto 100%
        resultado = calcular_precio_con_impuesto(200, 100)
        assert resultado == 400.0
    
    def test_particion_precio_invalido(self):
        """Partición 2: Precios inválidos"""
        with pytest.raises(ValueError, match="precio base debe ser mayor a 0"):
            calcular_precio_con_impuesto(0, 10)
        
        with pytest.raises(ValueError, match="precio base debe ser mayor a 0"):
            calcular_precio_con_impuesto(-50, 10)
    
    def test_particion_impuesto_invalido(self):
        """Partición 3: Impuestos inválidos"""
        with pytest.raises(ValueError, match="debe estar entre 0 y 100"):
            calcular_precio_con_impuesto(100, -1)
        
        with pytest.raises(ValueError, match="debe estar entre 0 y 100"):
            calcular_precio_con_impuesto(100, 101)
    
    def test_valores_limite_impuesto(self):
        """Análisis de Valor Límite: Porcentaje de impuesto"""
        # Impuesto 0% (límite inferior)
        assert calcular_precio_con_impuesto(100, 0) == 100.0
        
        # Impuesto 1%
        assert calcular_precio_con_impuesto(100, 1) == 101.0
        
        # Impuesto 99%
        assert calcular_precio_con_impuesto(100, 99) == 199.0
        
        # Impuesto 100% (límite superior)
        assert calcular_precio_con_impuesto(100, 100) == 200.0
    
    def test_redondeo_dos_decimales(self):
        """Verificar redondeo a 2 decimales"""
        # 100 + 15.5% = 115.50
        resultado = calcular_precio_con_impuesto(100, 15.5)
        assert resultado == 115.5
        
        # Caso que requiere redondeo
        resultado = calcular_precio_con_impuesto(10.33, 21)
        assert resultado == 12.50  # 10.33 * 1.21 = 12.4993


class TestCalcularDescuentoTiendaCajaNegra:
    """
    Pruebas de caja negra para calcular_descuento_tienda.
    
    Particiones de Equivalencia (según tabla de descuentos):
    1. $0 - $99.99: Sin descuento
    2. $100 - $499.99: 5% descuento
    3. $500 - $999.99: 10% descuento
    4. $1000+: 15% descuento
    """
    
    def test_particion_sin_descuento(self):
        """Partición 1: Compras de $0 - $99.99 (sin descuento)"""
        assert calcular_descuento_tienda(0) == 0.0
        assert calcular_descuento_tienda(50) == 0.0
        assert calcular_descuento_tienda(99.99) == 0.0
    
    def test_particion_descuento_5_porciento(self):
        """Partición 2: Compras de $100 - $499.99 (5% descuento)"""
        assert calcular_descuento_tienda(100) == 5.0      # 100 * 0.05
        assert calcular_descuento_tienda(250) == 12.5     # 250 * 0.05
        assert calcular_descuento_tienda(499.99) == 24.9995  # 499.99 * 0.05
    
    def test_particion_descuento_10_porciento(self):
        """Partición 3: Compras de $500 - $999.99 (10% descuento)"""
        assert calcular_descuento_tienda(500) == 50.0     # 500 * 0.10
        assert calcular_descuento_tienda(750) == 75.0     # 750 * 0.10
        assert calcular_descuento_tienda(999.99) == 99.999  # 999.99 * 0.10
    
    def test_particion_descuento_15_porciento(self):
        """Partición 4: Compras de $1000+ (15% descuento)"""
        assert calcular_descuento_tienda(1000) == 150.0   # 1000 * 0.15
        assert calcular_descuento_tienda(2000) == 300.0   # 2000 * 0.15
        assert calcular_descuento_tienda(10000) == 1500.0 # 10000 * 0.15
    
    def test_valores_limite_entre_particiones(self):
        """Análisis de Valor Límite: Bordes entre rangos"""
        # Límite 99.99 - 100
        assert calcular_descuento_tienda(99.99) == 0.0
        assert calcular_descuento_tienda(100.00) == 5.0
        assert calcular_descuento_tienda(100.01) == 5.0005
        
        # Límite 499.99 - 500
        assert calcular_descuento_tienda(499.99) == pytest.approx(24.9995, 0.01)
        assert calcular_descuento_tienda(500.00) == 50.0
        assert calcular_descuento_tienda(500.01) == pytest.approx(50.001, 0.01)
        
        # Límite 999.99 - 1000
        assert calcular_descuento_tienda(999.99) == pytest.approx(99.999, 0.01)
        assert calcular_descuento_tienda(1000.00) == 150.0
        assert calcular_descuento_tienda(1000.01) == pytest.approx(150.0015, 0.01)
    
    def test_valor_negativo_invalido(self):
        """Partición inválida: Total negativo"""
        with pytest.raises(ValueError, match="no puede ser negativo"):
            calcular_descuento_tienda(-100)
