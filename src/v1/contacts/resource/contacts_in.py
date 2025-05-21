from typing import Optional
from uuid import UUID

from .base_contacts import BaseContact


class PostContactIn(BaseContact):
    id: Optional[UUID] = None
