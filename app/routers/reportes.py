from app.database import get_db_connection
from fastapi import APIRouter,HTTPException
from app.schemas import Reporte

router =APIRouter(
    prefix="/reportes",
    tags=["Reportes"],
    
)

# Ruta para crear reporte del veterinario
@router.post("/crear_reporte")
def crear_reporte(new_report: Reporte):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """INSERT INTO reportes (
                    fecha_registro, id_lote, estado_general, diagnostico, tratamiento_prescrito,
                    dosis, frecuencia_tratamiento, fecha_inicio_tratamiento, fecha_fin_tratamiento, id_usuario
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(
                sql,
                (
                    new_report.fecha_registro,  # Asegúrate de incluir todos los campos necesarios
                    new_report.id_lote,
                    new_report.estado_general,
                    new_report.diagnostico,
                    new_report.tratamiento_prescrito,
                    new_report.dosis,
                    new_report.frecuencia_tratamiento,
                    new_report.fecha_inicio_tratamiento,
                    new_report.fecha_fin_tratamiento,
                    new_report.id_usuario,
                ),
            )
        connection.commit()
        connection.close()
        return {"informacion": "Registro exitoso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Ruta para obtener todos los reportes
@router.get("/obtener_reportes")
def obtener_reportes():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT r.id_reporte, r.id_lote, r.fecha_registro, u.nombres 
            FROM reportes r
            JOIN usuarios u ON r.id_usuario = u.id_usuario
            ORDER BY r.fecha_registro ASC """
            )
            reportes = cursor.fetchall()

        connection.close()

        # Convertir los resultados a una lista de diccionarios
        return reportes

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/editar_reporte/{id_reporte}")
def editar_reporte(id_reporte: int, reporte: Reporte):
    try:
        connection = get_db_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = """
                UPDATE reportes
                SET id_usuario = %s,
                    fecha_registro = %s,
                    id_lote = %s,
                    estado_general = %s,
                    diagnostico = %s,
                    tratamiento_prescrito = %s,
                    dosis = %s,
                    frecuencia_tratamiento = %s,
                    fecha_inicio_tratamiento = %s,
                    fecha_fin_tratamiento = %s
                WHERE id_reporte = %s
                """
                cursor.execute(
                    sql,
                    (
                        reporte.id_usuario,
                        reporte.fecha_registro,
                        reporte.id_lote,
                        reporte.estado_general,
                        reporte.diagnostico,
                        reporte.tratamiento_prescrito,
                        reporte.dosis,
                        reporte.frecuencia_tratamiento,
                        reporte.fecha_inicio_tratamiento,
                        reporte.fecha_fin_tratamiento,
                        id_reporte,
                    ),
                )
            connection.commit()
        return {"informacion": "Reporte actualizado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# obtiene un reporte especifico por id
@router.get("/obtener_reporte/{id_reporte}")
def obtener_reporte(id_reporte: int):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM reportes WHERE id_reporte = %s", (id_reporte,)
            )
            rv = cursor.fetchone()
        connection.close()

        if rv is None:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        return rv
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener_todos_los_reportes")
def obtener_todos_los_reportes():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM reportes")
            reportes = cursor.fetchall()
        connection.close()
        return reportes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

