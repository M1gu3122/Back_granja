from pydantic import BaseModel, Field



class LoginRequest(BaseModel):
    usuario: str
    contraseña: str
# Modelo Pydantic para los datos del contacto
class Usuario(BaseModel):
    id_usuario: int
    nombres: str
    apellidos: str
    usuario: str
    contraseña: str
    id_rol: int
    edad: int
    sexo: str
    estado: str = Field(default="activo")

    
class EstadoUsuario(BaseModel):
     estado:str


class EstadoTarea(BaseModel):
    estado: str  # El estado a actualizar


class Alerta(BaseModel):
    id_alertas: int
    fecha: str


class AlertUser(BaseModel):
    id_alertas: int
    id_usuario: int


class DatosClimaticos(BaseModel):
    id_dato: int
    humedad: float
    temperatura: float
    fecha: str
    id_galpon: int


class Galpon(BaseModel):
    # id_galpon: int
    capacidad: int
    aves: int


class Granja(BaseModel):
    id_granja: int
    nombre_granja: str
    contraseña: str


class GranGalpon(BaseModel):
    id_granja: int
    id_galpon: int


class Huevos(BaseModel):
    # id_recoleccion: int
    cantidad: int
    fecha: str
    id_lote: int


class Lote(BaseModel):
    # id_lote: int
    num_aves: int
    fecha_ingreso: str
    id_galpon: int


class Reporte(BaseModel):
    # id_reporte: int
    fecha_registro: str
    id_lote: int
    diagnostico: str = None
    tratamiento_prescrito: str = None
    fecha_inicio_tratamiento: str = None
    fecha_fin_tratamiento: str = None
    id_usuario: int
    estado_general: str = None
    dosis: str = None
    frecuencia_tratamiento: str = None


class Rol(BaseModel):
    id_rol: int
    tipo_usuario: str  # Puede ser 'administrador', 'trabajador' o 'veterinario'


class Tarea(BaseModel):
    # id_tareas: int
    descripcion: str
    fecha_asignacion: str
    estado: str  # Puede ser 'Pendiente', 'En progreso' o 'Completado'
    id_usuario: int


class EditarTarea(BaseModel):
    descripcion: str
    fecha_asignacion: str
    estado: str  # Puede ser 'Pendiente', 'En progreso' o 'Completado'
    id_usuario: int