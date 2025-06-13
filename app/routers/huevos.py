from app.database import get_db_connection
from fastapi import APIRouter,HTTPException
from app.schemas import Huevos

router =APIRouter(
    prefix="/huevos",
    tags=["Huevos"],
    
)
# Ruta para agregar huevos
@router.post("/agregar_huevos")
def agregar_huevos(huevos: Huevos):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO huevos (cantidad, fecha, id_lote) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (huevos.cantidad, huevos.fecha, huevos.id_lote))
        connection.commit()
        connection.close()
        return {"informacion": "Registro de huevos agregado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/obtener_huevos")
def obtener_huevos():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM huevos")
            huevos = cursor.fetchall()
        connection.close()
        return huevos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Ruta para obtener la cantidad total de huevos por fecha
@router.get("/total_huevos")
def total_huevos():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT fecha, SUM(cantidad) AS total_huevos FROM huevos GROUP BY fecha"
            )
            datos = cursor.fetchall()
        connection.close()
        return datos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))