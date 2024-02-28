from dataclasses import field
from datetime import datetime
from pydantic import field_validator, BaseModel


class DataHiveBaseModel(BaseModel):
    creator: str
    version: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @field_validator('creator', mode='after')
    def check_strings(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError('Field must be a string')
        return v
