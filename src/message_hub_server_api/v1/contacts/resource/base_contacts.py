from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BaseContact(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[UUID] = Field(
        default=None,
        title="ID",
        description="Identificador único do contato",
        alias="id",
    )
    first_name: Optional[str] = Field(
        default=None,
        title="Nome",
        description="Nome do contato",
        min_length=1,
        max_length=50,
        alias="firstName",
    )
    last_name: Optional[str] = Field(
        default=None,
        title="Sobrenome",
        description="Sobrenome do contato",
        min_length=1,
        max_length=50,
        alias="lastName",
    )
    organization: Optional[str] = Field(
        None,
        title="Organização",
        description="Organização do contato",
        alias="organization",
    )
    mobile: Optional[str] = Field(
        None,
        title="Celular",
        description="Número de celular do contato",
        min_length=1,
        max_length=20,
        alias="mobile",
    )
    email: Optional[str] = Field(
        None,
        title="Email",
        description="Endereço de email do contato",
        min_length=1,
        max_length=100,
        alias="email",
    )
    fax: Optional[str] = Field(
        None,
        title="Fax",
        description="Número de fax do contato",
        alias="fax",
    )
    custom1: Optional[str] = Field(
        None,
        title="Campo Personalizado 1",
        description="Campo personalizado 1 do contato",
        alias="custom1",
    )
    custom2: Optional[str] = Field(
        None,
        title="Campo Personalizado 2",
        description="Campo personalizado 2 do contato",
        alias="custom2",
    )
    custom3: Optional[str] = Field(
        None,
        title="Campo Personalizado 3",
        description="Campo personalizado 3 do contato",
        alias="custom3",
    )
    custom4: Optional[str] = Field(
        None,
        title="Campo Personalizado 4",
        description="Campo personalizado 4 do contato",
        alias="custom4",
    )
    address: Optional[str] = Field(
        None,
        title="Endereço",
        description="Endereço do contato",
        min_length=1,
        max_length=200,
        alias="address",
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        title="Data de Criação",
        description="Data de criação do contato",
        alias="createdAt",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        title="Data de Atualização",
        description="Data da última atualização do contato",
        alias="updatedAt",
    )
