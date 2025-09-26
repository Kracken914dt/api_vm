from enum import Enum
from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


class ProviderEnum(str, Enum):
    aws = "aws"
    azure = "azure"
    gcp = "gcp"
    onpremise = "onpremise"


class VMUpdateRequest(BaseModel):
    cpu: Optional[int] = None
    ram_gb: Optional[int] = None
    disk_gb: Optional[int] = None
    instance_type: Optional[str] = None
    size: Optional[str] = None
    machine_type: Optional[str] = None


class VMActionRequest(BaseModel):
    action: Literal["start", "stop", "restart"]
    requested_by: Optional[str] = Field(default="system")


class VMDTO(BaseModel):
    id: str
    name: str
    provider: ProviderEnum
    status: str
    specs: dict


class VMResponse(BaseModel):
    success: bool
    vm: Optional[VMDTO]
    error: Optional[str] = None


class VMListResponse(BaseModel):
    items: List[VMDTO]
