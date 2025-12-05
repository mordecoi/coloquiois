"""
Pruebas Orientadas a Objetos para el Sistema de Biblioteca
==========================================================
Estas pruebas demuestran técnicas específicas para sistemas OO:

1. Pruebas de Clase (Class Testing)
2. Pruebas de Comportamiento de Estado
3. Pruebas de Herencia y Polimorfismo
4. Pruebas de Encapsulación
5. Pruebas de Colaboración entre Objetos
"""

import pytest
from datetime import datetime, timedelta
from src.biblioteca import (
    Libro, Revista, DVD, Usuario, Prestamo, Biblioteca, Publicacion
)


class TestPruebasDeClaseLibro:
    """
    Pruebas de Clase para Libro.
    Objetivo: Ejercitar todas las operaciones de la clase.
    """
    
    def test_construccion_libro(self):
        """Verifica la construcción correcta de un Libro"""
        libro = Libro(1, "Clean Code", 2008, "Robert Martin", "978-0132350884")
        
        assert libro.id == 1
        assert libro.titulo == "Clean Code"
        assert libro.anio == 2008
        assert libro.autor == "Robert Martin"
        assert libro.isbn == "978-0132350884"
        assert libro.disponible is True
    
    def test_encapsulacion_atributos(self):
        """Verifica que los atributos están encapsulados (solo lectura)"""
        libro = Libro(1, "Test Book", 2020, "Test Author", "123")
        
        # Los atributos son de solo lectura (no tienen setter)
        with pytest.raises(AttributeError):
            libro.id = 999
        
        with pytest.raises(AttributeError):
            libro.titulo = "Nuevo Titulo"
    
    def test_metodo_marcar_prestado(self):
        """Verifica el cambio de estado al marcar como prestado"""
        libro = Libro(1, "Test", 2020, "Author", "123")
        
        assert libro.disponible is True
        libro.marcar_prestado()
        assert libro.disponible is False
    
    def test_metodo_marcar_prestado_ya_prestado(self):
        """Verifica que no se puede prestar dos veces"""
        libro = Libro(1, "Test", 2020, "Author", "123")
        libro.marcar_prestado()
        
        with pytest.raises(ValueError, match="ya está prestada"):
            libro.marcar_prestado()
    
    def test_metodo_marcar_devuelto(self):
        """Verifica el cambio de estado al devolver"""
        libro = Libro(1, "Test", 2020, "Author", "123")
        libro.marcar_prestado()
        
        assert libro.disponible is False
        libro.marcar_devuelto()
        assert libro.disponible is True
    
    def test_metodo_obtener_tipo(self):
        """Verifica el método polimórfico obtener_tipo"""
        libro = Libro(1, "Test", 2020, "Author", "123")
        assert libro.obtener_tipo() == "Libro"
    
    def test_calculo_penalizacion(self):
        """Verifica el cálculo de penalización específico de Libro"""
        libro = Libro(1, "Test", 2020, "Author", "123")
        
        assert libro.calcular_penalizacion_retraso(0) == 0.0
        assert libro.calcular_penalizacion_retraso(5) == 5.0
        assert libro.calcular_penalizacion_retraso(10) == 10.0


class TestPolimorfismoPublicaciones:
    """
    Pruebas de Polimorfismo.
    Objetivo: Verificar que las subclases implementan correctamente
    los métodos abstractos de la clase base.
    """
    
    def test_polimorfismo_obtener_tipo(self):
        """Verifica que cada tipo retorna su identificador correcto"""
        libro = Libro(1, "Test Libro", 2020, "Autor", "123")
        revista = Revista(2, "Test Revista", 2020, 15)
        dvd = DVD(3, "Test DVD", 2020, 120)
        
        assert libro.obtener_tipo() == "Libro"
        assert revista.obtener_tipo() == "Revista"
        assert dvd.obtener_tipo() == "DVD"
    
    def test_polimorfismo_calculo_penalizacion(self):
        """Verifica que cada tipo calcula su penalización correctamente"""
        libro = Libro(1, "Test", 2020, "Autor", "123")
        revista = Revista(2, "Test", 2020, 15)
        dvd = DVD(3, "Test", 2020, 120)
        
        dias_retraso = 10
        
        # Libro: $1/día
        assert libro.calcular_penalizacion_retraso(dias_retraso) == 10.0
        
        # Revista: $0.50/día
        assert revista.calcular_penalizacion_retraso(dias_retraso) == 5.0
        
        # DVD: $2/día
        assert dvd.calcular_penalizacion_retraso(dias_retraso) == 20.0
    
    def test_tratamiento_uniforme_como_publicacion(self):
        """Verifica que todas las publicaciones se pueden tratar uniformemente"""
        publicaciones: list[Publicacion] = [
            Libro(1, "Libro", 2020, "Autor", "123"),
            Revista(2, "Revista", 2020, 15),
            DVD(3, "DVD", 2020, 120)
        ]
        
        # Todas las publicaciones deben estar disponibles inicialmente
        for pub in publicaciones:
            assert pub.disponible is True
        
        # Todas se pueden marcar como prestadas
        for pub in publicaciones:
            pub.marcar_prestado()
            assert pub.disponible is False


class TestComportamientoEstadoUsuario:
    """
    Pruebas de Comportamiento de Estado.
    Objetivo: Verificar las transiciones de estado del Usuario.
    """
    
    def test_estado_inicial_usuario(self):
        """Verifica el estado inicial de un usuario recién creado"""
        usuario = Usuario(1, "Juan Pérez", "juan@example.com")
        
        assert usuario.id == 1
        assert usuario.nombre == "Juan Pérez"
        assert usuario.email == "juan@example.com"
        assert usuario.penalizacion_acumulada == 0.0
        assert len(usuario.obtener_prestamos_activos()) == 0
        assert usuario.puede_pedir_prestamo() is True
    
    def test_transicion_agregar_prestamos(self):
        """Verifica la transición al agregar préstamos"""
        usuario = Usuario(1, "Test", "test@example.com")
        libro1 = Libro(1, "Libro 1", 2020, "Autor", "123")
        libro2 = Libro(2, "Libro 2", 2020, "Autor", "456")
        
        prestamo1 = Prestamo(1, usuario, libro1)
        prestamo2 = Prestamo(2, usuario, libro2)
        
        usuario.agregar_prestamo(prestamo1)
        assert len(usuario.obtener_prestamos_activos()) == 1
        assert usuario.puede_pedir_prestamo() is True
        
        usuario.agregar_prestamo(prestamo2)
        assert len(usuario.obtener_prestamos_activos()) == 2
        assert usuario.puede_pedir_prestamo() is True
    
    def test_transicion_limite_prestamos(self):
        """Verifica que no se puedan tener más de 3 préstamos"""
        usuario = Usuario(1, "Test", "test@example.com")
        
        for i in range(3):
            libro = Libro(i, f"Libro {i}", 2020, "Autor", str(i))
            prestamo = Prestamo(i, usuario, libro)
            usuario.agregar_prestamo(prestamo)
        
        assert len(usuario.obtener_prestamos_activos()) == 3
        assert usuario.puede_pedir_prestamo() is False
    
    def test_transicion_penalizacion(self):
        """Verifica la transición al agregar penalizaciones"""
        usuario = Usuario(1, "Test", "test@example.com")
        
        assert usuario.puede_pedir_prestamo() is True
        
        usuario.agregar_penalizacion(10.0)
        assert usuario.penalizacion_acumulada == 10.0
        assert usuario.puede_pedir_prestamo() is False
        
        usuario.pagar_penalizacion(10.0)
        assert usuario.penalizacion_acumulada == 0.0
        assert usuario.puede_pedir_prestamo() is True


class TestColaboracionEntreObjetos:
    """
    Pruebas de Colaboración entre Objetos.
    Objetivo: Verificar la interacción correcta entre múltiples objetos.
    """
    
    def test_colaboracion_prestamo_usuario_publicacion(self):
        """Verifica la colaboración entre Prestamo, Usuario y Publicacion"""
        usuario = Usuario(1, "Juan", "juan@example.com")
        libro = Libro(1, "Clean Code", 2008, "Martin", "123")
        
        # Estado inicial
        assert libro.disponible is True
        assert len(usuario.obtener_prestamos_activos()) == 0
        
        # Crear préstamo
        prestamo = Prestamo(1, usuario, libro)
        libro.marcar_prestado()
        usuario.agregar_prestamo(prestamo)
        
        # Verificar colaboración
        assert libro.disponible is False
        assert len(usuario.obtener_prestamos_activos()) == 1
        assert prestamo.publicacion == libro
        assert prestamo.usuario == usuario
    
    def test_colaboracion_devolucion_sin_retraso(self):
        """Verifica la devolución sin retraso"""
        usuario = Usuario(1, "Test", "test@example.com")
        libro = Libro(1, "Test", 2020, "Author", "123")
        
        prestamo = Prestamo(1, usuario, libro)
        libro.marcar_prestado()
        usuario.agregar_prestamo(prestamo)
        
        # Devolver inmediatamente (sin retraso)
        prestamo.devolver()
        
        assert libro.disponible is True
        assert len(usuario.obtener_prestamos_activos()) == 0
        assert usuario.penalizacion_acumulada == 0.0
        assert prestamo.penalizacion == 0.0
    
    def test_integracion_completa_biblioteca(self):
        """Prueba de integración completa del sistema"""
        biblioteca = Biblioteca()
        
        # Crear usuarios y publicaciones
        usuario1 = Usuario(1, "Ana García", "ana@example.com")
        usuario2 = Usuario(2, "Carlos López", "carlos@example.com")
        libro1 = Libro(1, "Python Crash Course", 2019, "Eric Matthes", "123")
        libro2 = Libro(2, "Clean Code", 2008, "Robert Martin", "456")
        revista1 = Revista(3, "National Geographic", 2023, 202)
        
        # Agregar a la biblioteca
        biblioteca.agregar_usuario(usuario1)
        biblioteca.agregar_usuario(usuario2)
        biblioteca.agregar_publicacion(libro1)
        biblioteca.agregar_publicacion(libro2)
        biblioteca.agregar_publicacion(revista1)
        
        # Verificar búsquedas
        assert biblioteca.buscar_usuario(1) == usuario1
        assert biblioteca.buscar_publicacion(1) == libro1
        
        # Crear préstamo
        prestamo = biblioteca.crear_prestamo(1, 1)
        assert prestamo is not None
        assert prestamo.usuario == usuario1
        assert prestamo.publicacion == libro1
        assert libro1.disponible is False
        
        # Intentar prestar el mismo libro (debería fallar)
        with pytest.raises(ValueError, match="no está disponible"):
            biblioteca.crear_prestamo(2, 1)
        
        # Usuario 2 puede pedir libro 2
        prestamo2 = biblioteca.crear_prestamo(2, 2)
        assert prestamo2 is not None
    
    def test_colaboracion_usuario_con_penalizaciones(self):
        """Verifica que un usuario con penalizaciones no puede pedir préstamos"""
        biblioteca = Biblioteca()
        usuario = Usuario(1, "Test", "test@example.com")
        libro = Libro(1, "Test", 2020, "Author", "123")
        
        biblioteca.agregar_usuario(usuario)
        biblioteca.agregar_publicacion(libro)
        
        # Agregar penalización
        usuario.agregar_penalizacion(5.0)
        
        # No debería poder pedir préstamo
        with pytest.raises(ValueError, match="no puede pedir préstamos"):
            biblioteca.crear_prestamo(1, 1)


class TestHerenciaYComposicion:
    """
    Pruebas de Herencia.
    Objetivo: Verificar que las subclases heredan correctamente.
    """
    
    def test_herencia_metodos_comunes(self):
        """Verifica que las subclases heredan métodos de la clase base"""
        libro = Libro(1, "Test", 2020, "Author", "123")
        revista = Revista(2, "Test", 2020, 15)
        
        # Ambos heredan marcar_prestado de Publicacion
        libro.marcar_prestado()
        revista.marcar_prestado()
        
        assert libro.disponible is False
        assert revista.disponible is False
    
    def test_especializacion_subclases(self):
        """Verifica que las subclases tienen atributos específicos"""
        libro = Libro(1, "Test", 2020, "Author", "ISBN-123")
        revista = Revista(2, "Test", 2020, 42)
        dvd = DVD(3, "Test", 2020, 150)
        
        # Atributos específicos
        assert hasattr(libro, 'autor')
        assert hasattr(libro, 'isbn')
        assert libro.isbn == "ISBN-123"
        
        assert hasattr(revista, 'numero_edicion')
        assert revista.numero_edicion == 42
        
        assert hasattr(dvd, 'duracion_minutos')
        assert dvd.duracion_minutos == 150
    
    def test_imposible_instanciar_clase_abstracta(self):
        """Verifica que no se puede instanciar la clase abstracta Publicacion"""
        with pytest.raises(TypeError):
            # Esto debería fallar porque Publicacion es abstracta
            pub = Publicacion(1, "Test", 2020)
