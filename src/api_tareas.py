"""
API REST de Tareas - Ejemplo de Pruebas para WebApps
====================================================
Este módulo implementa una API REST simple usando Flask para demostrar
las pruebas de aplicaciones web.
"""

from flask import Flask, request, jsonify
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Tarea:
    """Modelo de Tarea"""
    id: int
    titulo: str
    descripcion: str
    completada: bool = False
    fecha_creacion: str = ""
    
    def __post_init__(self):
        if not self.fecha_creacion:
            self.fecha_creacion = datetime.now().isoformat()


class GestorTareas:
    """Gestor de tareas (lógica de negocio)"""
    
    def __init__(self):
        self.tareas: Dict[int, Tarea] = {}
        self.next_id = 1
    
    def crear_tarea(self, titulo: str, descripcion: str) -> Tarea:
        """Crea una nueva tarea"""
        if not titulo or len(titulo.strip()) == 0:
            raise ValueError("El título no puede estar vacío")
        
        if len(titulo) > 100:
            raise ValueError("El título no puede tener más de 100 caracteres")
        
        tarea = Tarea(
            id=self.next_id,
            titulo=titulo.strip(),
            descripcion=descripcion.strip() if descripcion else ""
        )
        self.tareas[self.next_id] = tarea
        self.next_id += 1
        return tarea
    
    def obtener_tarea(self, id: int) -> Optional[Tarea]:
        """Obtiene una tarea por ID"""
        return self.tareas.get(id)
    
    def obtener_todas(self) -> List[Tarea]:
        """Obtiene todas las tareas"""
        return list(self.tareas.values())
    
    def actualizar_tarea(self, id: int, titulo: Optional[str] = None, 
                        descripcion: Optional[str] = None,
                        completada: Optional[bool] = None) -> Optional[Tarea]:
        """Actualiza una tarea existente"""
        tarea = self.tareas.get(id)
        if not tarea:
            return None
        
        if titulo is not None:
            if len(titulo.strip()) == 0:
                raise ValueError("El título no puede estar vacío")
            tarea.titulo = titulo.strip()
        
        if descripcion is not None:
            tarea.descripcion = descripcion.strip()
        
        if completada is not None:
            tarea.completada = completada
        
        return tarea
    
    def eliminar_tarea(self, id: int) -> bool:
        """Elimina una tarea"""
        if id in self.tareas:
            del self.tareas[id]
            return True
        return False
    
    def obtener_estadisticas(self) -> Dict:
        """Obtiene estadísticas de las tareas"""
        total = len(self.tareas)
        completadas = sum(1 for t in self.tareas.values() if t.completada)
        pendientes = total - completadas
        
        return {
            "total": total,
            "completadas": completadas,
            "pendientes": pendientes,
            "porcentaje_completado": (completadas / total * 100) if total > 0 else 0
        }


def crear_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    gestor = GestorTareas()
    
    @app.route('/')
    def index():
        """Endpoint raíz"""
        return jsonify({
            "mensaje": "API de Tareas",
            "version": "1.0",
            "endpoints": [
                "GET /tareas",
                "GET /tareas/<id>",
                "POST /tareas",
                "PUT /tareas/<id>",
                "DELETE /tareas/<id>",
                "GET /estadisticas"
            ]
        })
    
    @app.route('/tareas', methods=['GET'])
    def listar_tareas():
        """Lista todas las tareas"""
        tareas = gestor.obtener_todas()
        return jsonify([asdict(t) for t in tareas]), 200
    
    @app.route('/tareas/<int:id>', methods=['GET'])
    def obtener_tarea(id):
        """Obtiene una tarea específica"""
        tarea = gestor.obtener_tarea(id)
        if not tarea:
            return jsonify({"error": "Tarea no encontrada"}), 404
        return jsonify(asdict(tarea)), 200
    
    @app.route('/tareas', methods=['POST'])
    def crear_tarea():
        """Crea una nueva tarea"""
        if not request.is_json:
            return jsonify({"error": "Se requiere Content-Type: application/json"}), 400
        
        datos = request.get_json()
        
        if 'titulo' not in datos:
            return jsonify({"error": "El campo 'titulo' es requerido"}), 400
        
        try:
            tarea = gestor.crear_tarea(
                titulo=datos['titulo'],
                descripcion=datos.get('descripcion', '')
            )
            return jsonify(asdict(tarea)), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    
    @app.route('/tareas/<int:id>', methods=['PUT'])
    def actualizar_tarea(id):
        """Actualiza una tarea existente"""
        if not request.is_json:
            return jsonify({"error": "Se requiere Content-Type: application/json"}), 400
        
        datos = request.get_json()
        
        try:
            tarea = gestor.actualizar_tarea(
                id=id,
                titulo=datos.get('titulo'),
                descripcion=datos.get('descripcion'),
                completada=datos.get('completada')
            )
            
            if not tarea:
                return jsonify({"error": "Tarea no encontrada"}), 404
            
            return jsonify(asdict(tarea)), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    
    @app.route('/tareas/<int:id>', methods=['DELETE'])
    def eliminar_tarea(id):
        """Elimina una tarea"""
        if gestor.eliminar_tarea(id):
            return '', 204
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    @app.route('/estadisticas', methods=['GET'])
    def obtener_estadisticas():
        """Obtiene estadísticas de las tareas"""
        stats = gestor.obtener_estadisticas()
        return jsonify(stats), 200
    
    @app.errorhandler(404)
    def not_found(error):
        """Manejador de errores 404"""
        return jsonify({"error": "Recurso no encontrado"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Manejador de errores 500"""
        return jsonify({"error": "Error interno del servidor"}), 500
    
    return app


if __name__ == '__main__':
    app = crear_app()
    app.run(debug=True, port=5000)
