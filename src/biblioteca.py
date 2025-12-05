"""
Sistema de Gestión de Biblioteca - Ejemplo de Pruebas Orientadas a Objetos
==========================================================================
Este módulo implementa un sistema OO con herencia, encapsulación y polimorfismo
para demostrar las pruebas orientadas a objetos.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime, timedelta


class Publicacion(ABC):
    """Clase abstracta base para publicaciones"""
    
    def __init__(self, id: int, titulo: str, anio: int):
        self._id = id
        self._titulo = titulo
        self._anio = anio
        self._disponible = True
    
    @property
    def id(self) -> int:
        """Getter para id (encapsulación)"""
        return self._id
    
    @property
    def titulo(self) -> str:
        """Getter para titulo (encapsulación)"""
        return self._titulo
    
    @property
    def anio(self) -> int:
        """Getter para año (encapsulación)"""
        return self._anio
    
    @property
    def disponible(self) -> bool:
        """Getter para disponibilidad"""
        return self._disponible
    
    def marcar_prestado(self):
        """Marca la publicación como prestada"""
        if not self._disponible:
            raise ValueError("La publicación ya está prestada")
        self._disponible = False
    
    def marcar_devuelto(self):
        """Marca la publicación como devuelta"""
        if self._disponible:
            raise ValueError("La publicación no está prestada")
        self._disponible = True
    
    @abstractmethod
    def obtener_tipo(self) -> str:
        """Método abstracto para obtener el tipo de publicación"""
        pass
    
    @abstractmethod
    def calcular_penalizacion_retraso(self, dias_retraso: int) -> float:
        """Método abstracto para calcular penalización por retraso"""
        pass


class Libro(Publicacion):
    """Clase para libros"""
    
    def __init__(self, id: int, titulo: str, anio: int, autor: str, isbn: str):
        super().__init__(id, titulo, anio)
        self._autor = autor
        self._isbn = isbn
    
    @property
    def autor(self) -> str:
        return self._autor
    
    @property
    def isbn(self) -> str:
        return self._isbn
    
    def obtener_tipo(self) -> str:
        """Implementación del método abstracto"""
        return "Libro"
    
    def calcular_penalizacion_retraso(self, dias_retraso: int) -> float:
        """Libros: $1 por día de retraso"""
        return dias_retraso * 1.0


class Revista(Publicacion):
    """Clase para revistas"""
    
    def __init__(self, id: int, titulo: str, anio: int, numero_edicion: int):
        super().__init__(id, titulo, anio)
        self._numero_edicion = numero_edicion
    
    @property
    def numero_edicion(self) -> int:
        return self._numero_edicion
    
    def obtener_tipo(self) -> str:
        """Implementación del método abstracto"""
        return "Revista"
    
    def calcular_penalizacion_retraso(self, dias_retraso: int) -> float:
        """Revistas: $0.50 por día de retraso"""
        return dias_retraso * 0.5


class DVD(Publicacion):
    """Clase para DVDs"""
    
    def __init__(self, id: int, titulo: str, anio: int, duracion_minutos: int):
        super().__init__(id, titulo, anio)
        self._duracion_minutos = duracion_minutos
    
    @property
    def duracion_minutos(self) -> int:
        return self._duracion_minutos
    
    def obtener_tipo(self) -> str:
        """Implementación del método abstracto"""
        return "DVD"
    
    def calcular_penalizacion_retraso(self, dias_retraso: int) -> float:
        """DVDs: $2 por día de retraso"""
        return dias_retraso * 2.0


class Usuario:
    """Clase para usuarios de la biblioteca"""
    
    def __init__(self, id: int, nombre: str, email: str):
        self._id = id
        self._nombre = nombre
        self._email = email
        self._prestamos_activos: List['Prestamo'] = []
        self._penalizacion_acumulada = 0.0
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def penalizacion_acumulada(self) -> float:
        return self._penalizacion_acumulada
    
    def agregar_prestamo(self, prestamo: 'Prestamo'):
        """Agrega un préstamo activo"""
        self._prestamos_activos.append(prestamo)
    
    def remover_prestamo(self, prestamo: 'Prestamo'):
        """Remueve un préstamo activo"""
        if prestamo in self._prestamos_activos:
            self._prestamos_activos.remove(prestamo)
    
    def obtener_prestamos_activos(self) -> List['Prestamo']:
        """Obtiene la lista de préstamos activos"""
        return self._prestamos_activos.copy()
    
    def puede_pedir_prestamo(self) -> bool:
        """Verifica si el usuario puede pedir un préstamo"""
        # Máximo 3 préstamos simultáneos
        if len(self._prestamos_activos) >= 3:
            return False
        # No puede pedir si tiene penalizaciones pendientes
        if self._penalizacion_acumulada > 0:
            return False
        return True
    
    def agregar_penalizacion(self, monto: float):
        """Agrega una penalización al usuario"""
        self._penalizacion_acumulada += monto
    
    def pagar_penalizacion(self, monto: float):
        """Paga una penalización"""
        if monto > self._penalizacion_acumulada:
            raise ValueError("El monto excede la penalización acumulada")
        self._penalizacion_acumulada -= monto


class Prestamo:
    """Clase para gestionar préstamos"""
    
    def __init__(self, id: int, usuario: Usuario, publicacion: Publicacion, 
                 dias_prestamo: int = 7):
        self._id = id
        self._usuario = usuario
        self._publicacion = publicacion
        self._fecha_prestamo = datetime.now()
        self._fecha_devolucion_esperada = self._fecha_prestamo + timedelta(days=dias_prestamo)
        self._fecha_devolucion_real: Optional[datetime] = None
        self._penalizacion = 0.0
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def usuario(self) -> Usuario:
        return self._usuario
    
    @property
    def publicacion(self) -> Publicacion:
        return self._publicacion
    
    @property
    def fecha_devolucion_esperada(self) -> datetime:
        return self._fecha_devolucion_esperada
    
    @property
    def fecha_devolucion_real(self) -> Optional[datetime]:
        return self._fecha_devolucion_real
    
    @property
    def penalizacion(self) -> float:
        return self._penalizacion
    
    def esta_vencido(self) -> bool:
        """Verifica si el préstamo está vencido"""
        if self._fecha_devolucion_real:
            return False  # Ya fue devuelto
        return datetime.now() > self._fecha_devolucion_esperada
    
    def calcular_dias_retraso(self) -> int:
        """Calcula los días de retraso"""
        if not self.esta_vencido():
            return 0
        dias = (datetime.now() - self._fecha_devolucion_esperada).days
        return max(0, dias)
    
    def devolver(self):
        """Procesa la devolución del préstamo"""
        if self._fecha_devolucion_real:
            raise ValueError("El préstamo ya fue devuelto")
        
        self._fecha_devolucion_real = datetime.now()
        
        # Calcular penalización si hay retraso
        if self._fecha_devolucion_real > self._fecha_devolucion_esperada:
            dias_retraso = (self._fecha_devolucion_real - self._fecha_devolucion_esperada).days
            self._penalizacion = self._publicacion.calcular_penalizacion_retraso(dias_retraso)
            self._usuario.agregar_penalizacion(self._penalizacion)
        
        # Marcar publicación como disponible
        self._publicacion.marcar_devuelto()
        
        # Remover de préstamos activos del usuario
        self._usuario.remover_prestamo(self)


class Biblioteca:
    """Clase principal que coordina el sistema"""
    
    def __init__(self):
        self._publicaciones: List[Publicacion] = []
        self._usuarios: List[Usuario] = []
        self._prestamos: List[Prestamo] = []
        self._next_prestamo_id = 1
    
    def agregar_publicacion(self, publicacion: Publicacion):
        """Agrega una publicación al catálogo"""
        self._publicaciones.append(publicacion)
    
    def agregar_usuario(self, usuario: Usuario):
        """Registra un nuevo usuario"""
        self._usuarios.append(usuario)
    
    def buscar_publicacion(self, id: int) -> Optional[Publicacion]:
        """Busca una publicación por ID"""
        for pub in self._publicaciones:
            if pub.id == id:
                return pub
        return None
    
    def buscar_usuario(self, id: int) -> Optional[Usuario]:
        """Busca un usuario por ID"""
        for usr in self._usuarios:
            if usr.id == id:
                return usr
        return None
    
    def crear_prestamo(self, usuario_id: int, publicacion_id: int) -> Prestamo:
        """Crea un nuevo préstamo"""
        usuario = self.buscar_usuario(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        publicacion = self.buscar_publicacion(publicacion_id)
        if not publicacion:
            raise ValueError("Publicación no encontrada")
        
        if not usuario.puede_pedir_prestamo():
            raise ValueError("El usuario no puede pedir préstamos en este momento")
        
        if not publicacion.disponible:
            raise ValueError("La publicación no está disponible")
        
        # Crear préstamo
        prestamo = Prestamo(self._next_prestamo_id, usuario, publicacion)
        self._next_prestamo_id += 1
        
        # Actualizar estados
        publicacion.marcar_prestado()
        usuario.agregar_prestamo(prestamo)
        self._prestamos.append(prestamo)
        
        return prestamo
    
    def obtener_prestamos_vencidos(self) -> List[Prestamo]:
        """Obtiene todos los préstamos vencidos"""
        return [p for p in self._prestamos if p.esta_vencido()]
