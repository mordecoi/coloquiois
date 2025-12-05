"""
Pruebas de Integración para el Sistema de Inventario
====================================================
Estas pruebas verifican la integración entre múltiples componentes:
BaseDatos, ValidadorProducto e InventarioService.
"""

import pytest
from src.inventario import (
    Producto, BaseDatos, ValidadorProducto, InventarioService
)


class TestIntegracionBaseDatos:
    """Tests de integración para BaseDatos"""
    
    def test_guardar_y_recuperar_producto(self):
        """Verifica que se pueda guardar y recuperar un producto"""
        bd = BaseDatos()
        producto = Producto(id=0, nombre="Laptop", precio=1000.0, stock=5)
        
        # Guardar
        id_guardado = bd.guardar_producto(producto)
        assert id_guardado > 0
        
        # Recuperar
        producto_recuperado = bd.obtener_producto(id_guardado)
        assert producto_recuperado is not None
        assert producto_recuperado.nombre == "Laptop"
        assert producto_recuperado.precio == 1000.0
        assert producto_recuperado.stock == 5
    
    def test_actualizar_stock_producto_existente(self):
        """Verifica que se pueda actualizar el stock de un producto"""
        bd = BaseDatos()
        producto = Producto(id=0, nombre="Mouse", precio=20.0, stock=10)
        id_producto = bd.guardar_producto(producto)
        
        # Actualizar stock
        resultado = bd.actualizar_stock(id_producto, 15)
        assert resultado is True
        
        # Verificar actualización
        producto_actualizado = bd.obtener_producto(id_producto)
        assert producto_actualizado.stock == 15
    
    def test_listar_multiples_productos(self):
        """Verifica que se listen todos los productos correctamente"""
        bd = BaseDatos()
        bd.guardar_producto(Producto(id=0, nombre="Teclado", precio=50.0, stock=3))
        bd.guardar_producto(Producto(id=0, nombre="Monitor", precio=200.0, stock=2))
        
        productos = bd.listar_productos()
        assert len(productos) == 2
        nombres = [p.nombre for p in productos]
        assert "Teclado" in nombres
        assert "Monitor" in nombres


class TestIntegracionValidador:
    """Tests de integración para ValidadorProducto"""
    
    def test_validar_producto_correcto(self):
        """Verifica que un producto válido pase la validación"""
        validador = ValidadorProducto()
        producto = Producto(id=1, nombre="Auriculares", precio=75.0, stock=10)
        
        es_valido, mensaje = validador.validar(producto)
        assert es_valido is True
        assert mensaje == ""
    
    def test_validar_producto_nombre_vacio(self):
        """Verifica que se rechace un producto con nombre vacío"""
        validador = ValidadorProducto()
        producto = Producto(id=1, nombre="", precio=75.0, stock=10)
        
        es_valido, mensaje = validador.validar(producto)
        assert es_valido is False
        assert "nombre" in mensaje.lower()
    
    def test_validar_producto_precio_invalido(self):
        """Verifica que se rechace un producto con precio inválido"""
        validador = ValidadorProducto()
        producto = Producto(id=1, nombre="Webcam", precio=-10.0, stock=5)
        
        es_valido, mensaje = validador.validar(producto)
        assert es_valido is False
        assert "precio" in mensaje.lower()


class TestIntegracionInventarioCompleto:
    """
    Tests de integración completa del sistema.
    Verifican la interacción entre todos los componentes.
    """
    
    @pytest.fixture
    def sistema_inventario(self):
        """Fixture que crea un sistema de inventario completo"""
        bd = BaseDatos()
        validador = ValidadorProducto()
        servicio = InventarioService(bd, validador)
        return servicio
    
    def test_flujo_completo_agregar_producto(self, sistema_inventario):
        """
        Test de integración: Flujo completo de agregar un producto.
        Verifica BD -> Validador -> Service
        """
        # Agregar producto
        exito, mensaje, id_producto = sistema_inventario.agregar_producto(
            nombre="SSD 1TB",
            precio=150.0,
            stock=8
        )
        
        assert exito is True
        assert "exitosamente" in mensaje.lower()
        assert id_producto > 0
        
        # Verificar que se guardó en la BD
        producto = sistema_inventario.bd.obtener_producto(id_producto)
        assert producto is not None
        assert producto.nombre == "SSD 1TB"
        
        # Verificar log
        log = sistema_inventario.obtener_log()
        assert len(log) > 0
        assert "SSD 1TB" in log[0]
    
    def test_flujo_completo_agregar_producto_invalido(self, sistema_inventario):
        """
        Test de integración: Intentar agregar un producto inválido.
        Verifica que el validador rechace y el servicio maneje el error.
        """
        exito, mensaje, id_producto = sistema_inventario.agregar_producto(
            nombre="",  # Nombre inválido
            precio=100.0,
            stock=5
        )
        
        assert exito is False
        assert "nombre" in mensaje.lower()
        assert id_producto == 0
        
        # Verificar que NO se guardó en la BD
        productos = sistema_inventario.bd.listar_productos()
        assert len(productos) == 0
    
    def test_flujo_completo_venta_producto(self, sistema_inventario):
        """
        Test de integración: Flujo completo de venta de producto.
        Verifica Service -> BD (consulta) -> BD (actualización)
        """
        # Preparar: agregar producto
        _, _, id_producto = sistema_inventario.agregar_producto(
            "RAM 16GB", 80.0, 10
        )
        
        # Vender producto
        exito, mensaje = sistema_inventario.vender_producto(id_producto, 3)
        
        assert exito is True
        assert "exitosamente" in mensaje.lower()
        
        # Verificar actualización de stock en BD
        producto = sistema_inventario.bd.obtener_producto(id_producto)
        assert producto.stock == 7  # 10 - 3
        
        # Verificar log
        log = sistema_inventario.obtener_log()
        assert any("Venta registrada" in entrada for entrada in log)
    
    def test_flujo_completo_venta_stock_insuficiente(self, sistema_inventario):
        """
        Test de integración: Intentar vender más unidades de las disponibles.
        """
        # Preparar: agregar producto con poco stock
        _, _, id_producto = sistema_inventario.agregar_producto(
            "Cable HDMI", 15.0, 2
        )
        
        # Intentar vender más de lo disponible
        exito, mensaje = sistema_inventario.vender_producto(id_producto, 5)
        
        assert exito is False
        assert "insuficiente" in mensaje.lower()
        
        # Verificar que el stock NO cambió
        producto = sistema_inventario.bd.obtener_producto(id_producto)
        assert producto.stock == 2
    
    def test_calculo_valor_total_inventario(self, sistema_inventario):
        """
        Test de integración: Cálculo del valor total con múltiples productos.
        Verifica Service -> BD (listar todos) -> cálculo
        """
        # Agregar varios productos
        sistema_inventario.agregar_producto("Producto A", 100.0, 5)
        sistema_inventario.agregar_producto("Producto B", 50.0, 10)
        sistema_inventario.agregar_producto("Producto C", 25.0, 4)
        
        # Calcular valor total
        valor_total = sistema_inventario.obtener_valor_total_inventario()
        
        # Verificar: (100*5) + (50*10) + (25*4) = 500 + 500 + 100 = 1100
        assert valor_total == 1100.0
    
    def test_multiples_operaciones_secuenciales(self, sistema_inventario):
        """
        Test de integración: Secuencia de múltiples operaciones.
        Simula un flujo de trabajo real.
        """
        # 1. Agregar productos
        _, _, id1 = sistema_inventario.agregar_producto("Producto 1", 100.0, 10)
        _, _, id2 = sistema_inventario.agregar_producto("Producto 2", 200.0, 5)
        
        # 2. Vender del producto 1
        sistema_inventario.vender_producto(id1, 3)
        
        # 3. Vender del producto 2
        sistema_inventario.vender_producto(id2, 2)
        
        # 4. Verificar estado final
        prod1 = sistema_inventario.bd.obtener_producto(id1)
        prod2 = sistema_inventario.bd.obtener_producto(id2)
        
        assert prod1.stock == 7  # 10 - 3
        assert prod2.stock == 3  # 5 - 2
        
        # 5. Verificar valor total
        valor_total = sistema_inventario.obtener_valor_total_inventario()
        assert valor_total == (100.0 * 7) + (200.0 * 3)  # 700 + 600 = 1300
        
        # 6. Verificar log completo
        log = sistema_inventario.obtener_log()
        assert len(log) == 4  # 2 agregados + 2 ventas
