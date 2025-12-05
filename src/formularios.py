"""
Módulo de Formularios - Ejemplo de Pruebas de Caja Negra
=========================================================
Este módulo implementa validaciones de formularios para demostrar
las pruebas de caja negra (pruebas funcionales).

Las pruebas de caja negra se enfocan en:
- Partición de Equivalencia
- Análisis de Valor Límite
- Validación de requisitos funcionales (sin conocer la implementación interna)
"""

import re
from typing import Tuple
from datetime import datetime


def validar_email(email: str) -> Tuple[bool, str]:
    """
    Valida un email según las especificaciones RFC.
    
    Requisitos funcionales:
    - Debe contener exactamente un símbolo @
    - Debe tener caracteres antes y después del @
    - El dominio debe tener al menos un punto
    - La longitud máxima es 254 caracteres
    
    Args:
        email: Email a validar
    
    Returns:
        (es_valido, mensaje_error)
    """
    if not email or len(email) == 0:
        return False, "El email no puede estar vacío"
    
    if len(email) > 254:
        return False, "El email no puede tener más de 254 caracteres"
    
    # Patrón básico de email
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(patron, email):
        return False, "Formato de email inválido"
    
    return True, ""


def validar_rango_edad(edad: int, edad_minima: int = 0, edad_maxima: int = 120) -> Tuple[bool, str]:
    """
    Valida que una edad esté dentro de un rango específico.
    
    Requisitos funcionales:
    - La edad debe ser un número entero
    - La edad debe estar entre edad_minima y edad_maxima (inclusivo)
    
    Args:
        edad: Edad a validar
        edad_minima: Edad mínima permitida
        edad_maxima: Edad máxima permitida
    
    Returns:
        (es_valido, mensaje_error)
    """
    if edad < edad_minima:
        return False, f"La edad debe ser al menos {edad_minima}"
    
    if edad > edad_maxima:
        return False, f"La edad no puede ser mayor a {edad_maxima}"
    
    return True, ""


def validar_nombre_usuario(nombre_usuario: str) -> Tuple[bool, str]:
    """
    Valida un nombre de usuario.
    
    Requisitos funcionales:
    - Longitud entre 3 y 20 caracteres
    - Solo puede contener letras, números y guiones bajos
    - Debe comenzar con una letra
    - No puede terminar con guión bajo
    
    Args:
        nombre_usuario: Nombre de usuario a validar
    
    Returns:
        (es_valido, mensaje_error)
    """
    if not nombre_usuario:
        return False, "El nombre de usuario no puede estar vacío"
    
    if len(nombre_usuario) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres"
    
    if len(nombre_usuario) > 20:
        return False, "El nombre de usuario no puede tener más de 20 caracteres"
    
    if not nombre_usuario[0].isalpha():
        return False, "El nombre de usuario debe comenzar con una letra"
    
    if nombre_usuario.endswith('_'):
        return False, "El nombre de usuario no puede terminar con guión bajo"
    
    patron = r'^[a-zA-Z][a-zA-Z0-9_]*$'
    if not re.match(patron, nombre_usuario):
        return False, "El nombre de usuario solo puede contener letras, números y guiones bajos"
    
    return True, ""


def calcular_precio_con_impuesto(precio_base: float, porcentaje_impuesto: float) -> float:
    """
    Calcula el precio final incluyendo impuestos.
    
    Requisitos funcionales:
    - El precio base debe ser mayor a 0
    - El porcentaje de impuesto debe estar entre 0 y 100
    - El resultado debe redondearse a 2 decimales
    
    Args:
        precio_base: Precio sin impuestos
        porcentaje_impuesto: Porcentaje de impuesto (0-100)
    
    Returns:
        Precio final con impuesto
    
    Raises:
        ValueError: Si los parámetros son inválidos
    """
    if precio_base <= 0:
        raise ValueError("El precio base debe ser mayor a 0")
    
    if porcentaje_impuesto < 0 or porcentaje_impuesto > 100:
        raise ValueError("El porcentaje de impuesto debe estar entre 0 y 100")
    
    impuesto = precio_base * (porcentaje_impuesto / 100)
    precio_final = precio_base + impuesto
    
    return round(precio_final, 2)


def validar_fecha_nacimiento(fecha_str: str) -> Tuple[bool, str]:
    """
    Valida una fecha de nacimiento.
    
    Requisitos funcionales:
    - Formato: DD/MM/YYYY
    - La fecha debe ser válida (día y mes existentes)
    - La fecha debe ser anterior a hoy
    - La persona debe tener menos de 150 años
    
    Args:
        fecha_str: Fecha en formato DD/MM/YYYY
    
    Returns:
        (es_valido, mensaje_error)
    """
    if not fecha_str:
        return False, "La fecha no puede estar vacía"
    
    # Validar formato
    patron = r'^\d{2}/\d{2}/\d{4}$'
    if not re.match(patron, fecha_str):
        return False, "El formato debe ser DD/MM/YYYY"
    
    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
    except ValueError:
        return False, "Fecha inválida"
    
    # Validar que sea anterior a hoy
    if fecha >= datetime.now():
        return False, "La fecha de nacimiento debe ser anterior a hoy"
    
    # Validar que no tenga más de 150 años
    años_transcurridos = (datetime.now() - fecha).days / 365.25
    if años_transcurridos > 150:
        return False, "La fecha de nacimiento no puede ser hace más de 150 años"
    
    return True, ""


def calcular_descuento_tienda(total_compra: float) -> float:
    """
    Calcula el descuento según el total de la compra.
    
    Requisitos funcionales (Tabla de descuentos):
    - $0 - $99.99: Sin descuento (0%)
    - $100 - $499.99: 5% de descuento
    - $500 - $999.99: 10% de descuento
    - $1000 o más: 15% de descuento
    
    Args:
        total_compra: Total de la compra antes del descuento
    
    Returns:
        Monto del descuento
    
    Raises:
        ValueError: Si el total es negativo
    """
    if total_compra < 0:
        raise ValueError("El total de la compra no puede ser negativo")
    
    if total_compra < 100:
        return 0.0
    elif total_compra < 500:
        return total_compra * 0.05
    elif total_compra < 1000:
        return total_compra * 0.10
    else:
        return total_compra * 0.15
