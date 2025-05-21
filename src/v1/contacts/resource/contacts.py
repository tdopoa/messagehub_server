from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.db.contact_db import ContactDB

from .contacts_in import PostContactIn
from .contacts_out import GetContactListOut

router = APIRouter(prefix="")


@router.get("/contacts-list/", response_model=List[GetContactListOut])
async def get_contacts_list() -> List[GetContactListOut]:
    """
    Obtém a lista de contatos.
    """
    res: List[GetContactListOut] = ContactDB().list_contacts()
    return res


@router.get("/{id}", response_model=List[GetContactListOut])
async def get_contact_by_id(id: UUID) -> List[GetContactListOut]:
    """
    Obtém um contato específico pelo ID.
    """
    contacts = ContactDB().select_contact(id)
    return [GetContactListOut(**contact.dict()) for contact in contacts]


@router.post("/contacts", response_model=GetContactListOut)
async def post_contact(body: PostContactIn):
    """
    Cria um novo contato.
    """
    contact_data = PostContactIn(
        first_name=body.first_name,
        last_name=body.last_name,
        organization=body.organization,
        mobile=body.mobile,
        email=body.email,
        fax=body.fax,
        custom1=body.custom1,
        custom2=body.custom2,
        custom3=body.custom3,
        custom4=body.custom4,
        address=body.address,
    )
    ContactDB().insert_contact(contact_data)
    return GetContactListOut(**contact_data.dict())


@router.put("/contacts", response_model=GetContactListOut)
async def put_contact(body: PostContactIn) -> GetContactListOut:
    """
    Atualiza um contato existente.
    """
    contact_data = PostContactIn(
        id=body.id,
        first_name=body.first_name,
        last_name=body.last_name,
        organization=body.organization,
        mobile=body.mobile,
        email=body.email,
        fax=body.fax,
        custom1=body.custom1,
        custom2=body.custom2,
        custom3=body.custom3,
        custom4=body.custom4,
        address=body.address,
    )
    ContactDB().update_contact(contact_data)
    return GetContactListOut(**contact_data.dict())


@router.delete("/contacts/{id}")
async def delete_contact(id: UUID):
    """
    Remove um contato pelo ID.
    """
    ContactDB().delete_contact(id)
    return {"message": f"Contato com ID {id} removido com sucesso."}
    return {"message": f"Contato com ID {id} removido com sucesso."}
