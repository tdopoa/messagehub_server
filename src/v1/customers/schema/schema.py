from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BaseCustomer(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    tenant_id: Optional[str] = Field(
        alias="TenantId",
        title="ID do Tenant",
        description="Identificador único do tenant",
        default=None,
    )
    first_name: Optional[str] = Field(
        alias="FirstName",
        title="Nome",
        description="Nome do cliente",
        min_length=1,
        max_length=50,
        default=None,
    )
    last_name: Optional[str] = Field(
        alias="LastName",
        title="Sobrenome",
        description="Sobrenome do cliente",
        max_length=50,
        default=None,
    )
    organization: Optional[str] = Field(
        alias="Organization",
        title="Organização",
        description="Nome da organização do cliente",
        max_length=50,
        default=None,
    )
    email: Optional[str] = Field(
        alias="Email",
        title="Email",
        description="Endereço de email do cliente",
        min_length=1,
        max_length=50,
    )
    phone: Optional[str] = Field(
        alias="Phone",
        title="Telefone",
        description="Número de telefone do cliente",
        max_length=15,
        default=None,
    )
    address: Optional[str] = Field(
        alias="Address",
        title="Endereço",
        description="Endereço do cliente",
        max_length=80,
        default=None,
    )
    city: Optional[str] = Field(
        alias="City",
        title="Cidade",
        description="Cidade do cliente",
        max_length=50,
        default=None,
    )
    state: Optional[str] = Field(
        alias="State",
        title="Estado",
        description="Estado do cliente",
        max_length=50,
        default=None,
    )
    zip_code: Optional[str] = Field(
        alias="ZipCode",
        title="CEP",
        description="CEP do cliente",
        max_length=20,
        default=None,
    )
    country: Optional[str] = Field(
        alias="Country",
        title="País",
        description="País do cliente",
        max_length=20,
        default=None,
    )
    profile_image: Optional[str] = Field(
        alias="ProfileImage",
        title="Imagem de Perfil",
        description="URL da imagem de perfil do cliente",
        max_length=255,
        default=None,
    )
    temporary_password: Optional[str] = Field(
        alias="TemporaryPassword",
        title="Senha Temporária",
        description="Senha temporária do cliente",
        max_length=50,
        default=None,
    )
    created_at: Optional[datetime] = Field(
        alias="CreatedAt",
        title="Data de Criação",
        description="Data de criação do registro",
        default=None,
    )
    updated_at: Optional[datetime] = Field(
        alias="UpdatedAt",
        title="Data de Atualização",
        description="Data da última atualização do registro",
        default=None,
    )
