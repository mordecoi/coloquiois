# Ejecutar todas las pruebas
pytest

# Ejecutar con más detalle
pytest -v

# Ejecutar pruebas específicas
pytest tests/test_calculadora.py
pytest tests/test_inventario_integracion.py

# Ejecutar por tipo de prueba (usando marcadores)
pytest -m unit
pytest -m integration
pytest -m whitebox
pytest -m blackbox

# Ejecutar con reporte de cobertura
pytest --cov=src --cov-report=html --cov-report=term

# Ejecutar y generar reporte HTML
pytest --html=report.html --self-contained-html

# Ejecutar solo las pruebas que fallaron la última vez
pytest --lf

# Ejecutar en modo verbose con salida detallada
pytest -vv --tb=long

# Ejecutar con salida de print()
pytest -s
