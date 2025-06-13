from app.database import get_db_connection
from app.schemas import Tarea,EstadoTarea
from fastapi import HTTPException,APIRouter

router =APIRouter(
    prefix="/tareas",
    tags=["Tareas"],
    
)
@router.get("/obtener_tareas")
def obtener_tareas():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT t.id_tareas,t.descripcion,t.fecha_asignacion, t.estado,u.nombres, u.id_usuario FROM  tareas t JOIN usuarios u  ON t.id_usuario = u.id_usuario ORDER BY t.fecha_asignacion ASC"
            )
            rv = cursor.fetchall()
        connection.close()
        return rv
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/obtener_tareas_trabajador/{id}")
def obtener_tareas(id: int):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_tareas, descripcion, fecha_asignacion, estado FROM tareas WHERE id_usuario = %s  ORDER BY estado desc, fecha_asignacion asc",
                (id,),
            )
            rv = cursor.fetchall()
        connection.close()
        return rv
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# obtener todas las tareas por trabajador
@router.get("/obtener_tareas_id/{id}")
def obtener_tareas_id(id: int):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM tareas WHERE id_tareas= %s",
                (id,),
            )
            rv = cursor.fetchone()
        connection.close()

        if rv is None:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        return rv
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#### ruta para crear una tarea
@router.post("/agregar_tarea")
def agregar_tarea(new_task: Tarea):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO tareas (descripcion, fecha_asignacion, estado, id_usuario) VALUES (%s, %s, %s, %s)"
            cursor.execute(
                sql,
                (
                    new_task.descripcion,
                    new_task.fecha_asignacion,
                    new_task.estado,
                    new_task.id_usuario,
                ),
            )
        connection.commit()
        connection.close()
        return {"informacion": "Tarea asignada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# eliminar tareas  por id
@router.delete("/eliminar_tarea/{id}")
def eliminar_tarea(id: int):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM tareas WHERE id_tareas = %s", (id,))
        connection.commit()
        connection.close()
        return {"informacion": "Registro eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@router.put("/editar_tarea/{id_tareas}")
def editar_tarea(id_tareas: int, task: Tarea):
    try:
        connection = get_db_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = """
                UPDATE tareas
                SET descripcion = %s,
                    fecha_asignacion = %s,
                    estado = %s,
                    id_usuario = %s
                WHERE id_tareas = %s
                """
                cursor.execute(
                    sql,
                    (
                        task.descripcion,
                        task.fecha_asignacion,
                        task.estado,
                        task.id_usuario,
                        id_tareas,  # Se usa el id_tareas recibido en la URL
                    ),
                )
            connection.commit()
        return {"informacion": "Registro actualizado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# editar estado de las tareas del trabajador
@router.put("/actualizar_estado/{id_tareas}")
def actualizar_estado(id_tareas: int, estado_tarea: EstadoTarea):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                UPDATE tareas
                SET estado = %s
                WHERE id_tareas = %s
            """
            cursor.execute(sql, (estado_tarea.estado, id_tareas))
        connection.commit()
        connection.close()
        return {"informacion": "Estado actualizado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


