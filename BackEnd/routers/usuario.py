from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas.usuario import CheckUniqueRequest, UserRegister, UserLogin, UserUpdate, UsuarioPublico
from database import get_db
import bcrypt

router = APIRouter()

@router.post("/check_unique")
def check_unique(data: CheckUniqueRequest, db: Session = Depends(get_db)):
    query_map = {
        'nombre_usuario': Usuario.nombre_usuario,
        'cedula_identidad': Usuario.cedula_identidad,
    }

    if data.field not in query_map:
        raise HTTPException(status_code=400, detail="Campo inválido")

    exists = db.query(Usuario).filter(query_map[data.field] == data.value).first() is not None
    return {"unique": not exists}

@router.post("/register")
def register(usuario: UserRegister, db: Session = Depends(get_db)):
    # Verificar si el nombre de usuario o la cédula ya existen
    existing_user = db.query(Usuario).filter(
        (Usuario.nombre_usuario == usuario.nombre_usuario) | 
        (Usuario.cedula_identidad == usuario.cedula_identidad)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nombre de usuario o cédula de identidad ya están en uso")
    
    # Hash de la contraseña
    hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt())
    
    # Crear el nuevo usuario
    db_usuario = Usuario(
        nombre_completo=usuario.nombre_completo,
        nombre_usuario=usuario.nombre_usuario,
        contrasena=hashed_password.decode('utf-8'),
        nivel_acceso='visitante',
        correo_electronico=usuario.correo_electronico,
        cedula_identidad=usuario.cedula_identidad,
        fecha_nacimiento=usuario.fecha_nacimiento,
        contacto=usuario.contacto,
        nacionalidad=usuario.nacionalidad,
        discapacidades=usuario.discapacidades
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return {"message": "Usuario registrado exitosamente"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.nombre_usuario == user.nombre_usuario).first()
    if not db_user or not bcrypt.checkpw(user.contrasena.encode('utf-8'), db_user.contrasena.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Usuario o contraseña inválidos")
    return {"message": "Login successful", "role": db_user.nivel_acceso}

@router.get("/info/{nombre_usuario}")
def get_user_basic_info(nombre_usuario: str, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"full_name": user.nombre_completo, "identity_card": user.cedula_identidad}

@router.get("/cedula/{cedula_identidad}")
def get_user_by_identity_card(cedula_identidad: str, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.cedula_identidad == cedula_identidad).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"full_name": user.nombre_completo, "identity_card": user.cedula_identidad}

@router.get("/usuario/{nombre_usuario}", response_model=UsuarioPublico)
def get_usuario(nombre_usuario: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioPublico.from_orm(usuario)

@router.put("/usuario/{nombre_usuario}")
def update_usuario(nombre_usuario: str, usuario: UserUpdate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.nombre_usuario and usuario.nombre_usuario != nombre_usuario:
        existing_user = db.query(Usuario).filter(Usuario.nombre_usuario == usuario.nombre_usuario).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
        db_usuario.nombre_usuario = usuario.nombre_usuario

    if usuario.correo_electronico:
        db_usuario.correo_electronico = usuario.correo_electronico
    if usuario.contacto:
        db_usuario.contacto = usuario.contacto
    if usuario.discapacidades:
        db_usuario.discapacidades = usuario.discapacidades
    if usuario.contrasena:
        hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt())
        db_usuario.contrasena = hashed_password.decode('utf-8')

    db.commit()
    db.refresh(db_usuario)

    return {"message": "Usuario actualizado exitosamente", "nuevo_nombre_usuario": db_usuario.nombre_usuario if usuario.nombre_usuario else None}
