from app.database import get_db_connection
from fastapi import APIRouter,HTTPException


router =APIRouter(
    prefix="/graficos",
    tags=["Graficos"],
    
)
# Ruta para obtener el total de aves por galpón
@router.get("/total_aves_por_galpon")
def total_aves_por_galpon():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_galpon, SUM(aves) AS total_aves FROM galpon GROUP BY id_galpon"
            )
            datos = cursor.fetchall()
        
        return datos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Ruta para obtener la cantidad de lotes y aves por galpón
@router.get("/lotes_y_aves_por_galpon")
def lotes_y_aves_por_galpon():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_galpon, COUNT(id_lote) AS numero_lotes, SUM(num_aves) AS total_aves FROM lote GROUP BY id_galpon"
            )
            datos = cursor.fetchall()
        
        return datos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Ruta para obtener el número de tareas pendientes por usuario
@router.get("/tareas_pendientes_por_usuario")
def tareas_pendientes_por_usuario():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT u.nombres, COUNT(*) AS tareas_pendientes
                FROM tareas t
                JOIN usuarios u ON t.id_usuario = u.id_usuario
                WHERE t.estado = %s
                GROUP BY u.id_usuario, u.nombres
            """,
                ("Pendiente",),
            )
            datos = cursor.fetchall()
        
        return datos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Ruta para obtener la frecuencia de diagnósticos en los reportes
@router.get("/frecuencia_diagnostico")
def frecuencia_diagnostico():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT diagnostico, COUNT(*) AS frecuencia
                FROM reportes
                GROUP BY diagnostico
                ORDER BY frecuencia DESC
            """
            )
            datos = cursor.fetchall()
        
        return datos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
