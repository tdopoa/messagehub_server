from typing import List
from uuid import UUID

from fastapi import APIRouter

from message_hub_server_api.v1.db.profile_db import ProfileDB

from .profiles_in import PostProfileIn
from .profiles_out import GetProfileListOut

router = APIRouter(prefix="")


@router.get("/profiles-list/", response_model=List[GetProfileListOut])
async def get_profiles_list() -> List[GetProfileListOut]:
    """
    Obtém a lista de perfis.
    """
    res: List[GetProfileListOut] = ProfileDB().list_profiles()
    return res


@router.get("/{id}", response_model=List[GetProfileListOut])
async def get_profile_by_id(id: UUID) -> List[GetProfileListOut]:
    """
    Obtém um perfil específico pelo ID.
    """
    profiles = ProfileDB().select_profile(id)
    return [GetProfileListOut(**profile.dict()) for profile in profiles]


@router.post("/profiles", response_model=GetProfileListOut)
async def post_profile(body: PostProfileIn):
    """
    Cria um novo perfil.
    """
    profile_data = PostProfileIn(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone=body.phone,
        password=body.password,
    )
    ProfileDB().insert_profile(profile_data)
    return GetProfileListOut(**profile_data.dict())


@router.put("/profiles", response_model=GetProfileListOut)
async def put_profile(body: PostProfileIn) -> GetProfileListOut:
    """
    Atualiza um perfil existente.
    """
    profile_data = PostProfileIn(
        id=body.id,
        firstName=body.first_name,
        lastName=body.last_name,
        email=body.email,
        phone=body.phone,
        password=body.password,
    )
    ProfileDB().update_profile(profile_data)
    return GetProfileListOut(**profile_data.dict())


@router.delete("/profiles/{id}")
async def delete_profile(id: UUID):
    """
    Remove um perfil pelo ID.
    """
    ProfileDB().delete_profile(id)
    return {"message": f"Perfil com ID {id} removido com sucesso."}
    return {"message": f"Perfil com ID {id} removido com sucesso."}
