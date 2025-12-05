# 🧪 Ejemplos Prácticos de Pruebas de Software en Python

Este proyecto contiene ejemplos completos de diferentes tipos de pruebas de software, implementados en Python 3.13+ con pytest. Cada módulo demuestra una categoría específica de testing según los fundamentos de ingeniería de software.

## 📚 Contenido del Proyecto

### 1. **Pruebas de Unidad (Unit Tests)**
- **Archivo**: `src/calculadora.py` + `tests/test_calculadora.py`
- **Descripción**: Pruebas de funciones individuales aisladas
- **Conceptos demostrados**:
  - Testing de funciones puras
  - Manejo de excepciones
  - Fixtures (setup/teardown)
  - Verificación de valores de retorno

### 2. **Pruebas de Integración (Integration Tests)**
- **Archivo**: `src/inventario.py` + `tests/test_inventario_integracion.py`
- **Descripción**: Verificación de la colaboración entre múltiples componentes
- **Conceptos demostrados**:
  - Integración entre BaseDatos, Validador y Service
  - Flujos completos de negocio
  - Verificación de estados compartidos

### 3. **Pruebas de Caja Blanca (White Box Testing)**
- **Archivo**: `src/procesamiento.py` + `tests/test_procesamiento_caja_blanca.py`
- **Descripción**: Pruebas estructurales basadas en el código interno
- **Conceptos demostrados**:
  - Cobertura de rutas de ejecución
  - Cobertura de ramas (branch coverage)
  - Complejidad ciclomática
  - Testing de todas las decisiones

### 4. **Pruebas de Caja Negra (Black Box Testing)**
- **Archivo**: `src/formularios.py` + `tests/test_formularios_caja_negra.py`
- **Descripción**: Pruebas funcionales sin conocer la implementación
- **Conceptos demostrados**:
  - Partición de Equivalencia
  - Análisis de Valor Límite
  - Testing basado en especificaciones

### 5. **Pruebas Orientadas a Objetos (OO Testing)**
- **Archivo**: `src/biblioteca.py` + `tests/test_biblioteca_oo.py`
- **Descripción**: Testing de sistemas con herencia, polimorfismo y encapsulación
- **Conceptos demostrados**:
  - Pruebas de clase (class testing)
  - Pruebas de comportamiento de estado
  - Pruebas de herencia y polimorfismo
  - Pruebas de colaboración entre objetos

### 6. **Pruebas para Aplicaciones Web (WebApp Testing)**
- **Archivo**: `src/api_tareas.py` + `tests/test_api_tareas_webapp.py`
- **Descripción**: Testing de APIs REST
- **Conceptos demostrados**:
  - Pruebas de contenido (content testing)
  - Pruebas de interfaz (API testing)
  - Pruebas de funcionalidad
  - Validación de códigos HTTP
  - Verificación de endpoints

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.13 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar o descargar el proyecto**:
```bash
cd coloquiois
```

2. **Crear un entorno virtual** (recomendado):
```bash
python -m venv .venv

# En Windows
.venv\Scripts\activate

# En Linux/Mac
source .venv/bin/activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

### Dependencias Instaladas
- `pytest==8.3.3` - Framework de testing
- `pytest-cov==6.0.0` - Reporte de cobertura de código
- `pytest-html==4.1.1` - Reportes HTML de pruebas
- `flask==3.1.0` - Framework web para ejemplos de WebApp
- `requests==2.32.3` - Cliente HTTP para testing de APIs

## 🧪 Ejecutar las Pruebas

### Ejecutar Todas las Pruebas
```bash
pytest
```

### Ejecutar con Modo Verbose (más detalle)
```bash
pytest -v
```

### Ejecutar Pruebas Específicas por Archivo
```bash
# Pruebas de Unidad
pytest tests/test_calculadora.py -v

# Pruebas de Integración
pytest tests/test_inventario_integracion.py -v

# Pruebas de Caja Blanca
pytest tests/test_procesamiento_caja_blanca.py -v

# Pruebas de Caja Negra
pytest tests/test_formularios_caja_negra.py -v

# Pruebas OO
pytest tests/test_biblioteca_oo.py -v

# Pruebas WebApp
pytest tests/test_api_tareas_webapp.py -v
```

### Ejecutar Pruebas por Tipo (usando marcadores)
```bash
pytest -m unit           # Solo pruebas unitarias
pytest -m integration    # Solo pruebas de integración
pytest -m whitebox      # Solo pruebas de caja blanca
pytest -m blackbox      # Solo pruebas de caja negra
pytest -m oo            # Solo pruebas OO
pytest -m webapp        # Solo pruebas de WebApp
```

### Generar Reporte de Cobertura
```bash
# Generar reporte en terminal y HTML
pytest --cov=src --cov-report=html --cov-report=term

# Ver el reporte HTML (se genera en htmlcov/index.html)
# En Windows:
start htmlcov/index.html

# En Linux/Mac:
open htmlcov/index.html
```

### Generar Reporte HTML de Pruebas
```bash
pytest --html=report.html --self-contained-html
```

### Otras Opciones Útiles
```bash
# Ejecutar solo las pruebas que fallaron la última vez
pytest --lf

# Ejecutar con salida muy detallada
pytest -vv --tb=long

# Mostrar salida de print()
pytest -s

# Ejecutar en paralelo (requiere pytest-xdist)
pytest -n auto
```

## 📊 Estructura del Proyecto

```
coloquiois/
│
├── src/                          # Código fuente
│   ├── calculadora.py           # Módulo de ejemplo para pruebas unitarias
│   ├── inventario.py            # Sistema para pruebas de integración
│   ├── procesamiento.py         # Código para pruebas de caja blanca
│   ├── formularios.py           # Validaciones para pruebas de caja negra
│   ├── biblioteca.py            # Sistema OO para pruebas orientadas a objetos
│   └── api_tareas.py            # API REST para pruebas de WebApp
│
├── tests/                        # Suite de pruebas
│   ├── test_calculadora.py      # Tests de unidad
│   ├── test_inventario_integracion.py  # Tests de integración
│   ├── test_procesamiento_caja_blanca.py  # Tests de caja blanca
│   ├── test_formularios_caja_negra.py  # Tests de caja negra
│   ├── test_biblioteca_oo.py    # Tests OO
│   └── test_api_tareas_webapp.py  # Tests de WebApp
│
├── .github/
│   └── workflows/
│       └── ci.yml               # Configuración de CI/CD (GitHub Actions)
│
├── requirements.txt              # Dependencias del proyecto
├── pytest.ini                    # Configuración de pytest
├── run_tests.sh                  # Script para ejecutar pruebas
└── README.md                     # Este archivo
```

## 🎯 Conceptos Clave Demostrados

### Niveles de Prueba
1. **Pruebas de Unidad**: Verifican componentes individuales aislados
2. **Pruebas de Integración**: Verifican la interacción entre componentes
3. **Pruebas de Sistema**: Verifican el sistema completo (ejemplos en WebApp)

### Técnicas de Diseño de Casos de Prueba

#### Caja Blanca (Estructural)
- Cobertura de líneas
- Cobertura de ramas/decisiones
- Cobertura de rutas
- Complejidad ciclomática

#### Caja Negra (Funcional)
- Partición de Equivalencia: Dividir entradas en clases
- Análisis de Valor Límite: Probar bordes de rangos
- Tablas de decisión

### Principios de Testing Aplicados
- **Aislamiento**: Cada test es independiente
- **Repetibilidad**: Los tests producen los mismos resultados
- **Claridad**: Cada test tiene un propósito claro
- **Automatización**: Todos los tests se pueden ejecutar automáticamente

## 🔧 Integración Continua (CI/CD)

Este proyecto incluye configuración para GitHub Actions (`.github/workflows/ci.yml`) que:

- Ejecuta todas las pruebas automáticamente en cada push
- Funciona en Windows y Linux
- Genera reportes de cobertura
- Falla el build si alguna prueba falla

## 📖 Ejemplos de Uso

### Ejecutar un Test Específico
```bash
# Ejecutar solo un test específico por nombre
pytest tests/test_calculadora.py::TestOperacionesBasicas::test_sumar_numeros_positivos -v
```

### Ver Cobertura de un Módulo Específico
```bash
pytest tests/test_calculadora.py --cov=src.calculadora --cov-report=term
```

### Ejecutar con Salida Detallada de Fallos
```bash
pytest -vv --tb=long
```

## 🎓 Propósito Educativo

Este proyecto fue creado como material educativo para demostrar:

1. **Fundamentos de Testing**: Conceptos de Pressman sobre calidad de software
2. **Estrategias de Prueba**: Desde componentes hasta sistema completo
3. **Tácticas de Prueba**: Caja blanca y caja negra
4. **Testing Moderno**: Automatización, CI/CD, y mejores prácticas
5. **Aplicación Práctica**: Código real que puedes ejecutar y modificar

## 📝 Métricas de Cobertura Esperadas

Al ejecutar todas las pruebas con cobertura, deberías obtener:

- **Cobertura de líneas**: >90%
- **Cobertura de ramas**: >85%
- **Todos los tests**: PASSED ✅

## 🤝 Contribuciones

Este es un proyecto educativo. Siéntete libre de:
- Agregar más ejemplos de pruebas
- Mejorar la documentación
- Reportar problemas o sugerencias

## 📚 Referencias

Este proyecto está basado en los conceptos de:
- **Roger S. Pressman** - "Ingeniería del Software: Un Enfoque Práctico"
- Principios de Aseguramiento de la Calidad del Software (SQA)
- Prácticas modernas de DevOps y CI/CD
- Metodologías ágiles de testing

## 📄 Licencia

Este proyecto es de uso educativo libre.

---

**¡Feliz Testing! 🧪✨**

Para cualquier duda o consulta, revisa el código fuente que está completamente documentado con comentarios explicativos.
