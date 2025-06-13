from app.database import get_db_connection
from fastapi import APIRouter,HTTPException
from app.schemas import Galpon

router =APIRouter(
    prefix="/galpones",
    tags=["Galpones"],
    
)

# Ruta para contar los galpones del administrador
@router.get("/contar_galpones")
def contar_galpones():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total FROM galpon")
            count = cursor.fetchone()
        connection.close()
        return count
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#### ruta para crear un galpon ########
@router.post("/crear_galpon")
def crear_galpon(galpon: Galpon):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO galpon (capacidad, aves) 
                VALUES (%s, %s)
            """
            cursor.execute(sql, (galpon.capacidad, galpon.aves))
        connection.commit()
        connection.close()
        return {"informacion": "Galpón agregado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener_galpones")
def obtener_galpones():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM galpon")
            galpones = cursor.fetchall()
        connection.close()
        return galpones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Ruta para actualizar un galpón
@router.put("/actualizar_galpon/{id_galpon}")
def actualizar_galpon(id_galpon: int, galpon: Galpon):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                UPDATE galpon
                SET capacidad = %s, aves = %s
                WHERE id_galpon = %s
            """
            cursor.execute(sql, (galpon.capacidad, galpon.aves, id_galpon))
        connection.commit()
        connection.close()
        return {"informacion": "Galpón actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

