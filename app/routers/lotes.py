from app.database import get_db_connection
from fastapi import APIRouter,HTTPException
from app.schemas import Lote

router =APIRouter(
    prefix="/lotes",
    tags=["Lotes"],
    
)
# Ruta para contar los lotes del administrador
@router.get("/contar_lotes")
def contar_lotes():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total FROM lote")
            count = cursor.fetchone()
        connection.close()
        return count
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Ruta para crear un lote
@router.post("/crear_lote")
def crear_lote(lote: Lote):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO lote (num_aves, fecha_ingreso, id_galpon) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (lote.num_aves, lote.fecha_ingreso, lote.id_galpon))
        connection.commit()
        connection.close()
        return {"informacion": "Lote agregado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener_lotes")
def obtener_lotes():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM lote")
            lotes = cursor.fetchall()
        connection.close()
        return lotes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Ruta para actualizar un lote
@router.put("/actualizar_lote/{id_lote}")
def actualizar_lote(id_lote: int, lote: Lote):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                UPDATE lote
                SET num_aves = %s, fecha_ingreso = %s, id_galpon = %s
                WHERE id_lote = %s
            """
            cursor.execute(
                sql, (lote.num_aves, lote.fecha_ingreso, lote.id_galpon, id_lote)
            )
        connection.commit()
        connection.close()
        return {"informacion": "Lote actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))