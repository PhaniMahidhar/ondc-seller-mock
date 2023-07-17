from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_serializer


class Action(str, Enum):
    SEARCH = 'search'
    ON_SEARCH = 'on_search'
    SELECT = 'select'
    ON_SELECT = 'on_select'


class Domain(str, Enum):
    ONDC_TRV10 = 'ONDC:TRV10'


class Context(BaseModel):
    domain: Domain
    action: Action
    message_id: str
    transaction_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow, )
    bap_id: str
    bap_uri: str
    bpp_id: Optional[str] = Field(default=None)
    bpp_uri: Optional[str] = Field(default=None)

    @field_serializer('timestamp')
    def serialize_dt(self, dt: datetime, _info):
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]




