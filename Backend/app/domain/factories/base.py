from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any
from app.domain.schemas import VMDTO, VMUpdateRequest


class VirtualMachineFactory(ABC):
    @abstractmethod
    def validate_params(self, params: Dict[str, Any]) -> None: ...

    @abstractmethod
    def provision(self, name: str, params: Dict[str, Any]) -> VMDTO: ...

    @abstractmethod
    def update(self, vm: VMDTO, changes: VMUpdateRequest) -> VMDTO: ...

    @abstractmethod
    def apply_action(self, vm: VMDTO, action: str) -> VMDTO: ...
