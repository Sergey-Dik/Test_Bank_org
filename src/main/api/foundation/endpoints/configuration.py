from dataclasses import dataclass
from typing import Optional, Type

from src.main.api.models.base_model import BaseModel


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]] = None
    response_model: Optional[Type[BaseModel]] = None
