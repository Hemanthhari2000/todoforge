import hashlib
import re
from datetime import datetime, timezone

from pydantic import BaseModel, field_validator


class SpaceModel(BaseModel):
    name: str

    @field_validator("name")
    def validate_name(cls, value):
        if not re.match(r"^[a-zA-Z0-9]+$", value):
            raise ValueError(
                "name must contain only letters and numbers, no special characters allowed."
            )
        return value


class TodoModel(BaseModel):
    id: str
    title: str
    done: bool = False

    @staticmethod
    def generate_id(title: str) -> str:
        curr_utc_time = str(datetime.now(timezone.utc))
        hash_input = f"{title}{curr_utc_time}".encode("utf-8")
        return hashlib.sha1(hash_input).hexdigest()
