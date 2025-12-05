"""
Módulo de Calculadora - Ejemplo de Pruebas de Unidad
=====================================================
Este módulo implementa funciones matemáticas básicas para demostrar
las pruebas de unidad (unit tests).
"""


def sumar(a: float, b: float) -> float:
    """
    Suma dos números.
    
    Args:
        a: Primer número
        b: Segundo número
    
    Returns:
        La suma de a y b
    """
    return a + b


def restar(a: float, b: float) -> float:
    """
    Resta dos números.
    
    Args:
        a: Primer número
        b: Segundo número
    
    Returns:
        La diferencia de a - b
    """
    return a - b


def multiplicar(a: float, b: float) -> float:
    """
    Multiplica dos números.
    
    Args:
        a: Primer número
        b: Segundo número
    
    Returns:
        El producto de a * b
    """
    return a * b


def dividir(a: float, b: float) -> float:
    """
    Divide dos números.
    
    Args:
        a: Dividendo
        b: Divisor
    
    Returns:
        El cociente de a / b
    
    Raises:
        ValueError: Si el divisor es cero
    """
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b


def potencia(base: float, exponente: int) -> float:
    """
    Calcula la potencia de un número.
    
    Args:
        base: Número base
        exponente: Exponente
    
    Returns:
        base elevado a exponente
    """
    return base ** exponente


def factorial(n: int) -> int:
    """
    Calcula el factorial de un número.
    
    Args:
        n: Número entero no negativo
    
    Returns:
        El factorial de n
    
    Raises:
        ValueError: Si n es negativo
    """
    if n < 0:
        raise ValueError("El factorial no está definido para números negativos")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
