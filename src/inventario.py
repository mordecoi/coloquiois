"""
Sistema de Gestión de Inventario - Ejemplo de Pruebas de Integración
====================================================================
Este módulo implementa un sistema con múltiples componentes que interactúan
entre sí, demostrando las pruebas de integración.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Producto:
    """Representa un producto en el inventario"""
    id: int
    nombre: str
    precio: float
    stock: int


class BaseDatos:
    """Simula una base de datos para productos"""
    
    def __init__(self):
        self._productos: Dict[int, Producto] = {}
        self._next_id = 1
    
    def guardar_producto(self, producto: Producto) -> int:
        """Guarda un producto y retorna su ID"""
        if producto.id == 0:
            producto.id = self._next_id
            self._next_id += 1
        self._productos[producto.id] = producto
        return producto.id
    
    def obtener_producto(self, id: int) -> Optional[Producto]:
        """Obtiene un producto por ID"""
        return self._productos.get(id)
    
    def actualizar_stock(self, id: int, nuevo_stock: int) -> bool:
        """Actualiza el stock de un producto"""
        if id in self._productos:
            self._productos[id].stock = nuevo_stock
            return True
        return False
    
    def listar_productos(self) -> List[Producto]:
        """Lista todos los productos"""
        return list(self._productos.values())


class ValidadorProducto:
    """Valida datos de productos"""
    
    @staticmethod
    def validar(producto: Producto) -> tuple[bool, str]:
        """
        Valida un producto.
        
        Returns:
            (es_valido, mensaje_error)
        """
        if not producto.nombre or len(producto.nombre.strip()) == 0:
            return False, "El nombre no puede estar vacío"
        
        if producto.precio <= 0:
            return False, "El precio debe ser mayor a cero"
        
        if producto.stock < 0:
            return False, "El stock no puede ser negativo"
        
        return True, ""


class InventarioService:
    """Servicio de gestión de inventario que integra BD y validación"""
    
    def __init__(self, base_datos: BaseDatos, validador: ValidadorProducto):
        self.bd = base_datos
        self.validador = validador
        self._log: List[str] = []
    
    def agregar_producto(self, nombre: str, precio: float, stock: int) -> tuple[bool, str, int]:
        """
        Agrega un producto al inventario.
        
        Returns:
            (exito, mensaje, id_producto)
        """
        producto = Producto(id=0, nombre=nombre, precio=precio, stock=stock)
        
        # Validar
        es_valido, mensaje = self.validador.validar(producto)
        if not es_valido:
            self._registrar_log(f"Error validación: {mensaje}")
            return False, mensaje, 0
        
        # Guardar
        id_producto = self.bd.guardar_producto(producto)
        self._registrar_log(f"Producto agregado: {nombre} (ID: {id_producto})")
        return True, "Producto agregado exitosamente", id_producto
    
    def vender_producto(self, id_producto: int, cantidad: int) -> tuple[bool, str]:
        """
        Registra la venta de un producto.
        
        Returns:
            (exito, mensaje)
        """
        producto = self.bd.obtener_producto(id_producto)
        
        if not producto:
            return False, "Producto no encontrado"
        
        if cantidad <= 0:
            return False, "La cantidad debe ser mayor a cero"
        
        if producto.stock < cantidad:
            return False, f"Stock insuficiente. Disponible: {producto.stock}"
        
        nuevo_stock = producto.stock - cantidad
        self.bd.actualizar_stock(id_producto, nuevo_stock)
        self._registrar_log(f"Venta registrada: {cantidad} unidades de {producto.nombre}")
        return True, "Venta registrada exitosamente"
    
    def obtener_valor_total_inventario(self) -> float:
        """Calcula el valor total del inventario"""
        productos = self.bd.listar_productos()
        total = sum(p.precio * p.stock for p in productos)
        return total
    
    def _registrar_log(self, mensaje: str):
        """Registra un evento en el log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._log.append(f"[{timestamp}] {mensaje}")
    
    def obtener_log(self) -> List[str]:
        """Obtiene el historial de log"""
        return self._log.copy()
