from enum import Enum
from typing import Literal, Optional, List
from pydantic import BaseModel, Field


class ProviderEnum(str, Enum):
    aws = "aws"
    azure = "azure"
    gcp = "gcp"
    onpremise = "onpremise"


class AWSParams(BaseModel):
    instance_type: str = Field(..., example="t2.micro")
    region: str = Field(..., example="us-east-1")
    vpc: str
    ami: str


class AzureParams(BaseModel):
    size: str = Field(..., example="Standard_B1s")
    resource_group: str
    image: str
    vnet: str


class GCPParams(BaseModel):
    machine_type: str = Field(..., example="e2-micro")
    zone: str = Field(..., example="us-central1-a")
    base_disk: str
    project: str


class OnPremParams(BaseModel):
    cpu: int
    ram_gb: int
    disk_gb: int
    nic: str


class VMCreateRequest(BaseModel):
    provider: ProviderEnum
    name: str
    params: dict
    requested_by: Optional[str] = Field(default="system")


class VMUpdateRequest(BaseModel):
    # cambios genéricos; los proveedores validarán lo aplicable
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
