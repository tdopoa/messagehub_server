from typing import Optional
from uuid import UUID

from v1.contacts.schema.base_contacts import BaseContact


class PostContactIn(BaseContact):
    id: Optional[UUID] = None
