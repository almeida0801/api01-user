from typing import List
from fastapi import APIRouter, Response, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from db.database import engine,SessionLocal, get_db
from db.models import Usuarios as UsuariosModel
from schemas.usuario import Usuarios, UsuarioRequest, UsuarioResponse
from sqlalchemy.orm import Session
from repository.usuario import UsuarioRepository

from db.base import Base
from db.database import get_db


#cria a tabela
Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/v1/api/usuarios")


@router.post("/criar", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def create(request: UsuarioRequest, db: Session = Depends(get_db)):
    usuario = UsuarioRepository.save(db, UsuariosModel(**request.dict()))
    return UsuarioResponse.from_orm(usuario)
   
    
    
@router.get("/listar_todos", response_model=list[UsuarioResponse])
def find_all(db: Session = Depends(get_db)):
    usuarios = UsuarioRepository.find_all(db)
    return [UsuarioResponse.from_orm(usuario) for usuario in usuarios]


@router.get("/procurar_por_id/{id}", response_model=UsuarioResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    usuario = UsuarioRepository.find_by_id(db, id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="usuario não encontrado"
        )
    return UsuarioResponse.from_orm(usuario)


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    if not UsuarioRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado"
        )
    UsuarioRepository.delete_by_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/update/{id}", response_model=UsuarioResponse)
def update(id: int, request: UsuarioRequest, db: Session = Depends(get_db)):
    usuario = UsuarioRepository.save(db, UsuariosModel(id=id, **request.dict()))
    return UsuarioResponse.from_orm(usuario)
