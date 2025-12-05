"""
Pruebas para WebApp - API REST de Tareas
========================================
Estas pruebas demuestran técnicas para testing de aplicaciones web:

1. Pruebas de Contenido (Content Testing)
2. Pruebas de Interfaz/API (Interface Testing)
3. Pruebas de Funcionalidad (Component Testing)
4. Pruebas de Navegación (para APIs: endpoints y rutas)
5. Pruebas de Configuración (códigos de estado HTTP)
"""

import pytest
import json
from src.api_tareas import crear_app, GestorTareas


@pytest.fixture
def app():
    """Fixture que crea la aplicación Flask para testing"""
    app = crear_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Fixture que crea un cliente de prueba"""
    return app.test_client()


class TestContenidoAPI:
    """
    Pruebas de Contenido (Content Testing).
    Verifican que la API retorna el contenido correcto en formato JSON.
    """
    
    def test_endpoint_raiz_contenido(self, client):
        """Verifica el contenido del endpoint raíz"""
        response = client.get('/')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        
        data = response.get_json()
        assert 'mensaje' in data
        assert 'version' in data
        assert 'endpoints' in data
        assert data['mensaje'] == "API de Tareas"
        assert data['version'] == "1.0"
        assert isinstance(data['endpoints'], list)
    
    def test_listar_tareas_vacio_contenido(self, client):
        """Verifica el contenido al listar tareas cuando no hay ninguna"""
        response = client.get('/tareas')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_crear_tarea_contenido_respuesta(self, client):
        """Verifica el contenido de la respuesta al crear una tarea"""
        payload = {
            "titulo": "Mi primera tarea",
            "descripcion": "Descripción de la tarea"
        }
        
        response = client.post('/tareas',
                              data=json.dumps(payload),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = response.get_json()
        
        # Verificar estructura del contenido
        assert 'id' in data
        assert 'titulo' in data
        assert 'descripcion' in data
        assert 'completada' in data
        assert 'fecha_creacion' in data
        
        # Verificar valores
        assert data['titulo'] == "Mi primera tarea"
        assert data['descripcion'] == "Descripción de la tarea"
        assert data['completada'] is False
        assert data['id'] > 0


class TestInterfazAPI:
    """
    Pruebas de Interfaz (Interface Testing).
    Verifican la correcta interacción con la API REST.
    """
    
    def test_metodos_http_permitidos(self, client):
        """Verifica los métodos HTTP permitidos en cada endpoint"""
        # GET en /tareas está permitido
        response = client.get('/tareas')
        assert response.status_code == 200
        
        # POST en /tareas está permitido
        response = client.post('/tareas',
                              data=json.dumps({"titulo": "Test"}),
                              content_type='application/json')
        assert response.status_code == 201
    
    def test_content_type_requerido(self, client):
        """Verifica que se requiera Content-Type: application/json"""
        # Sin Content-Type
        response = client.post('/tareas', data='{"titulo": "Test"}')
        assert response.status_code == 400
        
        # Con Content-Type correcto
        response = client.post('/tareas',
                              data=json.dumps({"titulo": "Test"}),
                              content_type='application/json')
        assert response.status_code == 201
    
    def test_headers_respuesta(self, client):
        """Verifica los headers de la respuesta"""
        response = client.get('/tareas')
        
        assert 'Content-Type' in response.headers
        assert 'application/json' in response.headers['Content-Type']
    
    def test_campos_requeridos(self, client):
        """Verifica validación de campos requeridos"""
        # Sin campo 'titulo'
        response = client.post('/tareas',
                              data=json.dumps({"descripcion": "Solo descripción"}),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'titulo' in data['error'].lower()


class TestFuncionalidadAPI:
    """
    Pruebas de Funcionalidad (Component Testing).
    Verifican que la lógica de negocio funcione correctamente.
    """
    
    def test_crear_y_obtener_tarea(self, client):
        """Flujo: Crear una tarea y luego obtenerla"""
        # Crear tarea
        payload = {"titulo": "Tarea de prueba", "descripcion": "Test"}
        response = client.post('/tareas',
                              data=json.dumps(payload),
                              content_type='application/json')
        
        tarea_creada = response.get_json()
        id_tarea = tarea_creada['id']
        
        # Obtener tarea
        response = client.get(f'/tareas/{id_tarea}')
        assert response.status_code == 200
        
        tarea_obtenida = response.get_json()
        assert tarea_obtenida['id'] == id_tarea
        assert tarea_obtenida['titulo'] == "Tarea de prueba"
    
    def test_actualizar_tarea(self, client):
        """Flujo: Crear, actualizar y verificar cambios"""
        # Crear
        response = client.post('/tareas',
                              data=json.dumps({"titulo": "Tarea original"}),
                              content_type='application/json')
        id_tarea = response.get_json()['id']
        
        # Actualizar
        actualizacion = {
            "titulo": "Tarea modificada",
            "completada": True
        }
        response = client.put(f'/tareas/{id_tarea}',
                             data=json.dumps(actualizacion),
                             content_type='application/json')
        
        assert response.status_code == 200
        tarea_actualizada = response.get_json()
        assert tarea_actualizada['titulo'] == "Tarea modificada"
        assert tarea_actualizada['completada'] is True
    
    def test_eliminar_tarea(self, client):
        """Flujo: Crear, eliminar y verificar que no existe"""
        # Crear
        response = client.post('/tareas',
                              data=json.dumps({"titulo": "Tarea a eliminar"}),
                              content_type='application/json')
        id_tarea = response.get_json()['id']
        
        # Eliminar
        response = client.delete(f'/tareas/{id_tarea}')
        assert response.status_code == 204
        
        # Verificar que ya no existe
        response = client.get(f'/tareas/{id_tarea}')
        assert response.status_code == 404
    
    def test_listar_multiples_tareas(self, client):
        """Verifica el listado de múltiples tareas"""
        # Crear 3 tareas
        for i in range(3):
            client.post('/tareas',
                       data=json.dumps({"titulo": f"Tarea {i+1}"}),
                       content_type='application/json')
        
        # Listar
        response = client.get('/tareas')
        tareas = response.get_json()
        
        assert len(tareas) == 3
        titulos = [t['titulo'] for t in tareas]
        assert "Tarea 1" in titulos
        assert "Tarea 2" in titulos
        assert "Tarea 3" in titulos
    
    def test_estadisticas(self, client):
        """Verifica el cálculo de estadísticas"""
        # Crear 5 tareas
        for i in range(5):
            client.post('/tareas',
                       data=json.dumps({"titulo": f"Tarea {i+1}"}),
                       content_type='application/json')
        
        # Completar 2 tareas
        client.put('/tareas/1',
                  data=json.dumps({"completada": True}),
                  content_type='application/json')
        client.put('/tareas/2',
                  data=json.dumps({"completada": True}),
                  content_type='application/json')
        
        # Obtener estadísticas
        response = client.get('/estadisticas')
        stats = response.get_json()
        
        assert stats['total'] == 5
        assert stats['completadas'] == 2
        assert stats['pendientes'] == 3
        assert stats['porcentaje_completado'] == 40.0


class TestNavegacionEndpoints:
    """
    Pruebas de Navegación (Navigation Testing).
    Para APIs REST: Verifican que todos los endpoints sean accesibles.
    """
    
    def test_todos_los_endpoints_accesibles(self, client):
        """Verifica que todos los endpoints principales sean accesibles"""
        # Endpoint raíz
        response = client.get('/')
        assert response.status_code == 200
        
        # Listar tareas
        response = client.get('/tareas')
        assert response.status_code == 200
        
        # Estadísticas
        response = client.get('/estadisticas')
        assert response.status_code == 200
    
    def test_endpoint_inexistente(self, client):
        """Verifica el manejo de endpoints que no existen"""
        response = client.get('/endpoint-inexistente')
        assert response.status_code == 404
        
        data = response.get_json()
        assert 'error' in data
    
    def test_navegacion_recurso_especifico(self, client):
        """Verifica la navegación a recursos específicos por ID"""
        # Crear tarea
        response = client.post('/tareas',
                              data=json.dumps({"titulo": "Test"}),
                              content_type='application/json')
        id_tarea = response.get_json()['id']
        
        # Navegar al recurso específico
        response = client.get(f'/tareas/{id_tarea}')
        assert response.status_code == 200


class TestConfiguracionCodigosHTTP:
    """
    Pruebas de Configuración (Configuration Testing).
    Verifican los códigos de estado HTTP correctos.
    """
    
    def test_codigo_200_operaciones_exitosas(self, client):
        """Verifica código 200 OK para operaciones GET exitosas"""
        response = client.get('/')
        assert response.status_code == 200
        
        response = client.get('/tareas')
        assert response.status_code == 200
    
    def test_codigo_201_recurso_creado(self, client):
        """Verifica código 201 Created al crear recursos"""
        response = client.post('/tareas',
                              data=json.dumps({"titulo": "Nueva tarea"}),
                              content_type='application/json')
        assert response.status_code == 201
    
    def test_codigo_204_eliminacion_exitosa(self, client):
        """Verifica código 204 No Content al eliminar"""
        # Crear tarea
        response = client.post('/tareas',
                              data=json.dumps({"titulo": "Test"}),
                              content_type='application/json')
        id_tarea = response.get_json()['id']
        
        # Eliminar
        response = client.delete(f'/tareas/{id_tarea}')
        assert response.status_code == 204
        assert len(response.data) == 0
    
    def test_codigo_400_solicitud_invalida(self, client):
        """Verifica código 400 Bad Request para solicitudes inválidas"""
        # Sin Content-Type
        response = client.post('/tareas', data='{"titulo": "Test"}')
        assert response.status_code == 400
        
        # Sin campo requerido
        response = client.post('/tareas',
                              data=json.dumps({}),
                              content_type='application/json')
        assert response.status_code == 400
        
        # Título vacío
        response = client.post('/tareas',
                              data=json.dumps({"titulo": ""}),
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_codigo_404_recurso_no_encontrado(self, client):
        """Verifica código 404 Not Found para recursos inexistentes"""
        # Tarea inexistente
        response = client.get('/tareas/9999')
        assert response.status_code == 404
        
        # Actualizar tarea inexistente
        response = client.put('/tareas/9999',
                             data=json.dumps({"titulo": "Test"}),
                             content_type='application/json')
        assert response.status_code == 404
        
        # Eliminar tarea inexistente
        response = client.delete('/tareas/9999')
        assert response.status_code == 404


class TestValidacionesFuncionales:
    """
    Pruebas de validaciones y reglas de negocio.
    """
    
    def test_titulo_no_puede_estar_vacio(self, client):
        """Verifica que no se permitan títulos vacíos"""
        response = client.post('/tareas',
                              data=json.dumps({"titulo": "   "}),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'vacío' in data['error'].lower()
    
    def test_titulo_maximo_100_caracteres(self, client):
        """Verifica la longitud máxima del título"""
        titulo_largo = "a" * 101
        response = client.post('/tareas',
                              data=json.dumps({"titulo": titulo_largo}),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert '100' in data['error']
    
    def test_actualizar_con_titulo_vacio_falla(self, client):
        """Verifica que no se pueda actualizar con título vacío"""
        # Crear tarea
        response = client.post('/tareas',
                              data=json.dumps({"titulo": "Original"}),
                              content_type='application/json')
        id_tarea = response.get_json()['id']
        
        # Intentar actualizar con título vacío
        response = client.put(f'/tareas/{id_tarea}',
                             data=json.dumps({"titulo": ""}),
                             content_type='application/json')
        
        assert response.status_code == 400
