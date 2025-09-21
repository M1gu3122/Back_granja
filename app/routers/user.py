from app.database import get_db_connection
from fastapi import APIRouter, HTTPException
from app.schemas import Usuario, LoginRequest,EstadoUsuario
from datetime import datetime, timedelta
import jwt

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


# obtiene un usuario en especifico de la tabla usuarios
@router.get("/obtener_usuario/{id_usuario}")
def obtener_usuario(id_usuario: int):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,)
            )
            user = cursor.fetchone()

        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Ruta para obtener todos los contactos
@router.get("/obtener_usuarios")
def obtener_usuarios():
    try:
        connection = get_db_connection()  # Se obtiene la conexión a la base de datos
        with connection.cursor() as cursor:
            # Se realiza la consulta de los usuarios y sus roles
            cursor.execute(
                """
                SELECT u.id_usuario, u.nombres, u.apellidos, u.usuario, u.contraseña, r.tipo_usuario, u.edad, u.sexo ,u.estado
                FROM usuarios u 
                JOIN roles r ON u.id_rol = r.id_rol ;
                """
            )
            datos = cursor.fetchall()  # Se obtienen todos los registros

        connection.close()  # Se cierra la conexión a la base de datos

        return datos
    except Exception as e:
        print(f"Error: {e}")  # Se imprime el error en el servidor
        raise HTTPException(status_code=500, detail=str(e))


# Ruta para obtener el conteo de los registros
@router.get("/total_usuarios")
def total_usuarios():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total FROM usuarios")
            count = cursor.fetchone()
        connection.close()
        return count
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Ruta para crear un nuevo contacto
@router.post("/nuevo_usuario")
def nuevo_usuario(new_contact: Usuario):

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """INSERT INTO usuarios (id_usuario, nombres, apellidos, edad, sexo, usuario, contraseña, id_rol) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(
                sql,
                (
                    new_contact.id_usuario,
                    new_contact.nombres,
                    new_contact.apellidos,
                    new_contact.edad,
                    new_contact.sexo,
                    new_contact.usuario,
                    new_contact.contraseña,
                    new_contact.id_rol,
                    
                ),
            )
        connection.commit()
        connection.close()
        return {"informacion": "Registro exitoso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/editar_usuario/{id_usuario}")
def editar_usuario(id_usuario: int, usuario: Usuario):
    print("JSON recibido:", usuario.dict())  # 👀 te dirá qué falla
    try:
        connection = get_db_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = """
                UPDATE usuarios
                SET
                    id_usuario = %s,
                    nombres = %s,
                    apellidos = %s,
                    edad = %s,
                    sexo = %s,
                    usuario = %s,
                    contraseña = %s,
                    id_rol = %s
                WHERE id_usuario = %s
                """
                cursor.execute(
                    sql,
                    (
                        usuario.id_usuario,
                        usuario.nombres,
                        usuario.apellidos,
                        usuario.edad,
                        usuario.sexo,
                        usuario.usuario,
                        usuario.contraseña,
                        usuario.id_rol,
                        id_usuario,  # Este es el id_usuario del WHERE
                    ),
                )
            connection.commit()
            connection.close()
        return {"informacion": "Registro actualizado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/editar_estado_usuario/{id_usuario}")
def editar_usuario(id_usuario: int, estado_usuario: EstadoUsuario):
    try:
        connection = get_db_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = """
                UPDATE usuarios
                SET
                    estado = %s
                WHERE id_usuario = %s
                """
                cursor.execute(
                    sql,
                    (
                        estado_usuario.estado,
                        id_usuario,  # Este es el id_usuario del WHERE
                    ),
                )
            connection.commit()
            
        return {"informacion": "Estado actualizado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Ruta para eliminar un usuario
@router.delete("/eliminar_usuario/{id}")
def eliminar_usuario(id: int):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
        connection.commit()
        connection.close()
        return {"informacion": "Registro eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Obtiene un usuario por su usuario con rol de trabajador


@router.get("/buscar_usuario_tb/{nombre}")
def buscar_usuario_tb(nombre: str, rol: int = None):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Construir la consulta dinámica
            query = "SELECT * FROM usuarios WHERE nombres LIKE %s"
            params = ["%" + nombre + "%"]

            # Si se proporciona el rol, se agrega a la consulta
            if rol is not None:
                query += " AND id_rol = %s"
                params.append(rol)

            cursor.execute(query, params)
            users = cursor.fetchall()
        connection.close()

        if not users:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return users

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/buscar_usuario_vt/{nombre}")
def buscar_usuario_vt(nombre: str):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM usuarios WHERE nombres LIKE %s and id_rol=3;",
                ("%" + nombre + "%",),
            )
            user = cursor.fetchall()
        connection.close()
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


SECRET_KEY = "DJEJFKJLSFK"


# Función para crear un token de acceso
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
    else:
        to_encode.update(
            {"exp": datetime.utcnow() + timedelta(minutes=10)}
        )  # Default 30 minutos
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


# Función para verificar el token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


@router.post("/login")
async def login(login_request: LoginRequest):
    try:
        usuario = login_request.usuario
        contraseña = login_request.contraseña

        print(f"Usuario recibido: {usuario}")
        print(f"Contraseña recibida: {contraseña}")

        # Verificar las credenciales del usuario
        connection = get_db_connection()
        print("Conexión a la base de datos exitosa")

        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT usuarios.id_usuario,usuarios.usuario, usuarios.contraseña,usuarios.estado,usuarios.sexo, roles.tipo_usuario 
            FROM usuarios 
            JOIN roles ON usuarios.id_rol = roles.id_rol 
            WHERE usuarios.usuario = %s and usuarios.estado='activo' 
        """,
            (usuario,),
        )

        user = cursor.fetchone()
        cursor.close()
        connection.close()

        print(f"Resultado de la consulta SQL: {user}")

        if user:
            id_usuario = user["id_usuario"]  # Acceder usando la clave del diccionario
            stored_password = user[
                "contraseña"
            ].strip()  # La contraseña almacenada está en la segunda columna
            user_role = user["tipo_usuario"]  # El rol está en la tercera columna
            usuario = user["usuario"]
            genero = user["sexo"]

            print(f"ID Usuario: {id_usuario}")
            print(f"Contraseña almacenada: {stored_password}")
            print(f"Rol del usuario: {user_role}")
            print(f"Rol del usuario: {usuario}")

            # Verificar si la contraseña coincide
            if stored_password == contraseña.strip():
                print("Las contraseñas coinciden, creando token...")
                payload = {
                    "usuario": usuario,
                    "id": id_usuario,
                    "rol": user_role,
                    "genero" : genero,
                   
                }
                token = create_access_token(payload)

                print(f"Token generado: {token}")
                return {"token": token, "rol": user_role}
            else:
                print("La contraseña no coincide")
                raise HTTPException(status_code=401, detail="Credenciales inválidas")
        else:
            print("No se encontró el usuario")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
    except Exception as e:
        print(f"Error en login: {e}")
        raise HTTPException(status_code=500, detail=f"Error en login: {str(e)}")
    




