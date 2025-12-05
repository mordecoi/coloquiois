"""
Módulo de Procesamiento de Datos - Ejemplo de Pruebas de Caja Blanca
====================================================================
Este módulo implementa funciones con lógica compleja para demostrar
las pruebas de caja blanca (pruebas estructurales).

Las pruebas de caja blanca se enfocan en:
- Cobertura de todas las rutas de ejecución
- Cobertura de decisiones (ramas)
- Complejidad ciclomática
"""


def clasificar_edad(edad: int) -> str:
    """
    Clasifica una persona según su edad.
    
    Esta función tiene múltiples rutas de ejecución (complejidad ciclomática = 5).
    
    Args:
        edad: Edad de la persona
    
    Returns:
        Clasificación: "Bebé", "Niño", "Adolescente", "Adulto", "Anciano"
    
    Raises:
        ValueError: Si la edad es negativa o mayor a 150
    """
    # Ruta 1: Validación de entrada negativa
    if edad < 0:
        raise ValueError("La edad no puede ser negativa")
    
    # Ruta 2: Validación de entrada fuera de rango
    if edad > 150:
        raise ValueError("La edad no puede ser mayor a 150")
    
    # Ruta 3: Bebé
    if edad < 3:
        return "Bebé"
    # Ruta 4: Niño
    elif edad < 13:
        return "Niño"
    # Ruta 5: Adolescente
    elif edad < 18:
        return "Adolescente"
    # Ruta 6: Adulto
    elif edad < 65:
        return "Adulto"
    # Ruta 7: Anciano
    else:
        return "Anciano"


def calcular_descuento(precio: float, es_miembro: bool, cantidad: int) -> float:
    """
    Calcula el precio final con descuentos aplicados.
    
    Lógica de descuentos (múltiples condiciones anidadas):
    - Si es miembro: 10% de descuento base
    - Si cantidad >= 10: 5% adicional
    - Si cantidad >= 20: 10% adicional (en lugar de 5%)
    - Si precio > 1000 y es miembro: 5% adicional
    
    Complejidad ciclomática = 6
    
    Args:
        precio: Precio unitario del producto
        es_miembro: Si el cliente es miembro
        cantidad: Cantidad de productos
    
    Returns:
        Precio final con descuentos aplicados
    """
    if precio <= 0:
        raise ValueError("El precio debe ser mayor a cero")
    
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a cero")
    
    total = precio * cantidad
    descuento = 0.0
    
    # Ruta: es miembro
    if es_miembro:
        descuento += 0.10  # 10% descuento base
        
        # Ruta anidada: precio alto
        if total > 1000:
            descuento += 0.05  # 5% adicional
    
    # Ruta: cantidad alta
    if cantidad >= 20:
        descuento += 0.10  # 10% por volumen
    elif cantidad >= 10:
        descuento += 0.05  # 5% por volumen
    
    precio_final = total * (1 - descuento)
    return precio_final


def buscar_elemento(lista: list, elemento) -> int:
    """
    Busca un elemento en una lista y retorna su índice.
    
    Implementa búsqueda lineal con múltiples condiciones.
    Complejidad ciclomática depende del tamaño de la lista.
    
    Args:
        lista: Lista donde buscar
        elemento: Elemento a buscar
    
    Returns:
        Índice del elemento o -1 si no se encuentra
    """
    # Ruta 1: Lista vacía
    if not lista:
        return -1
    
    # Ruta 2: Búsqueda iterativa
    for i, item in enumerate(lista):
        if item == elemento:
            return i
    
    # Ruta 3: No encontrado
    return -1


def validar_contrasena(contrasena: str) -> tuple[bool, list[str]]:
    """
    Valida una contraseña según múltiples criterios.
    
    Criterios de validación (cada uno es una ruta):
    1. Longitud mínima de 8 caracteres
    2. Al menos una letra mayúscula
    3. Al menos una letra minúscula
    4. Al menos un dígito
    5. Al menos un carácter especial
    
    Complejidad ciclomática = 6
    
    Args:
        contrasena: Contraseña a validar
    
    Returns:
        (es_valida, lista_de_errores)
    """
    errores = []
    
    # Ruta 1: Validar longitud
    if len(contrasena) < 8:
        errores.append("Debe tener al menos 8 caracteres")
    
    # Ruta 2: Validar mayúsculas
    if not any(c.isupper() for c in contrasena):
        errores.append("Debe contener al menos una mayúscula")
    
    # Ruta 3: Validar minúsculas
    if not any(c.islower() for c in contrasena):
        errores.append("Debe contener al menos una minúscula")
    
    # Ruta 4: Validar dígitos
    if not any(c.isdigit() for c in contrasena):
        errores.append("Debe contener al menos un dígito")
    
    # Ruta 5: Validar caracteres especiales
    caracteres_especiales = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in caracteres_especiales for c in contrasena):
        errores.append("Debe contener al menos un carácter especial")
    
    # Ruta 6: Determinar validez
    es_valida = len(errores) == 0
    return es_valida, errores


def procesar_calificacion(nota: float) -> str:
    """
    Determina la calificación según la nota.
    
    Función simple con múltiples decisiones en cascada.
    Complejidad ciclomática = 6
    
    Args:
        nota: Nota numérica (0-100)
    
    Returns:
        Calificación: "A", "B", "C", "D", "F"
    
    Raises:
        ValueError: Si la nota está fuera del rango 0-100
    """
    if nota < 0 or nota > 100:
        raise ValueError("La nota debe estar entre 0 y 100")
    
    if nota >= 90:
        return "A"
    elif nota >= 80:
        return "B"
    elif nota >= 70:
        return "C"
    elif nota >= 60:
        return "D"
    else:
        return "F"
