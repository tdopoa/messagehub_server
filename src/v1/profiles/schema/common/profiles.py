from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BaseProfile(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True, alias_generator=lambda x: x.replace("_", "")
    )

    tenant_id: Optional[str] = Field(
        alias="TenantId",
        title="ID do Tenant",
        description="Identificador único do tenant",
        default=None,
    )

    id: Optional[UUID] = Field(
        default=None,
        title="ID",
        description="Identificador único do perfil",
        alias="id",
    )
    first_name: str = Field(
        ...,
        title="Nome",
        description="Nome do perfil",
        min_length=1,
        max_length=50,
        alias="firstName",
    )
    last_name: str = Field(
        ...,
        title="Sobrenome",
        description="Sobrenome do perfil",
        min_length=1,
        max_length=50,
        alias="lastName",
    )
    email: str = Field(
        ...,
        title="Email",
        description="Endereço de email do perfil",
        min_length=1,
        max_length=100,
        alias="email",
    )
    phone: Optional[str] = Field(
        None,
        title="Telefone",
        description="Número de telefone do perfil",
        min_length=1,
        max_length=20,
        alias="phone",
    )
    password: str = Field(
        ...,
        title="Senha",
        description="Senha do perfil",
        min_length=1,
        max_length=100,
        alias="password",
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        title="Data de Criação",
        description="Data de criação do perfil",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        title="Data de Atualização",
        description="Data da última atualização do perfil",
    )
