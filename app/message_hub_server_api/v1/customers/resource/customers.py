from typing import List
from uuid import UUID

from fastapi import APIRouter

from message_hub_server_api.v1.db.customer_db import CustomerDB

from .customers_in import PostCustomerIn
from .customers_out import GetCustomerListOut

router = APIRouter(prefix="")


@router.get("/customers-list/", response_model=List[GetCustomerListOut])
async def get_customers_list() -> List[GetCustomerListOut]:
    """
    Obtém a lista de clientes.
    """
    res: List[GetCustomerListOut] = CustomerDB().list_customer()
    return res


@router.get("/{id}", response_model=List[GetCustomerListOut])
async def get_customer_by_id(id: UUID) -> List[GetCustomerListOut]:
    """
    Obtém um cliente específico pelo ID.
    """
    customers = CustomerDB().select_customer(id)
    return [GetCustomerListOut(**customer.model_dump()) for customer in customers]


@router.post("/customers", response_model=GetCustomerListOut)
async def post_customer(body: PostCustomerIn):
    """
    Cria um novo cliente.
    """
    customer_data = PostCustomerIn(
        TenantId=body.tenant_id,
        FirstName=body.first_name,
        LastName=body.last_name,
        Organization=body.organization,
        Email=body.email,
        Phone=body.phone,
        Address=body.address,
        City=body.city,
        State=body.state,
        ZipCode=body.zip_code,
        Country=body.country,
        ProfileImage=body.profile_image,
        TemporaryPassword=body.temporary_password,
    )
    CustomerDB().create_customer(**customer_data.model_dump())
    return GetCustomerListOut(**customer_data.model_dump())


@router.put("/customers/{tenant_id}/{email}", response_model=GetCustomerListOut)
async def put_customer(
    tenant_id: str, email: str, body: PostCustomerIn
) -> GetCustomerListOut:
    """
    Atualiza um cliente existente.
    """
    customer_data = PostCustomerIn(
        TenantId=tenant_id,
        FirstName=body.first_name,
        LastName=body.last_name,
        Organization=body.organization,
        Email=email,
        Phone=body.phone,
        Address=body.address,
        City=body.city,
        State=body.state,
        ZipCode=body.zip_code,
        Country=body.country,
        ProfileImage=body.profile_image,
        TemporaryPassword=body.temporary_password,
    )
    CustomerDB().update_customer(
        tenant_id, email, **customer_data.model_dump(exclude={"tenant_id", "email"})
    )
    return GetCustomerListOut(**customer_data.model_dump())


@router.delete("/customers/{tenant_id}/{email}")
async def delete_customer(tenant_id: str, email: str):
    """
    Remove um cliente pelo tenant_id e email.
    """
    CustomerDB().delete_customer(tenant_id, email)
    return {"message": f"Cliente com email {email} removido com sucesso."}


@router.get(
    "/customers/search/{tenant_id}/{search_term}",
    response_model=List[GetCustomerListOut],
)
async def search_customers(
    tenant_id: str, search_term: str
) -> List[GetCustomerListOut]:
    """
    Busca clientes por termo de pesquisa.
    """
    customers = CustomerDB().search_customers(tenant_id, search_term)
    return [GetCustomerListOut(**customer) for customer in customers]
    return [GetCustomerListOut(**customer) for customer in customers]
    return [GetCustomerListOut(**customer) for customer in customers]
