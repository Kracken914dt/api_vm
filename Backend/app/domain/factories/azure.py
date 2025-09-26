from __future__ import annotations
from typing import Dict, Any
from app.domain.schemas import VMDTO, ProviderEnum, VMUpdateRequest
from app.domain.factories.base import VirtualMachineFactory
import uuid


class AzureVMFactory(VirtualMachineFactory):
    def validate_params(self, params: Dict[str, Any]) -> None:
        required = ["size", "resource_group", "image", "vnet"]
        missing = [k for k in required if k not in params]
        if missing:
            raise ValueError(f"Missing Azure params: {missing}")

    def provision(self, name: str, params: Dict[str, Any]) -> VMDTO:
        self.validate_params(params)
        vm_id = f"azure-{uuid.uuid4()}"
        specs = {
            "size": params["size"],
            "resource_group": params["resource_group"],
            "image": params["image"],
            "vnet": params["vnet"],
        }
        return VMDTO(id=vm_id, name=name, provider=ProviderEnum.azure, status="stopped", specs=specs)

    def update(self, vm: VMDTO, changes: VMUpdateRequest) -> VMDTO:
        if changes.size:
            vm.specs["size"] = changes.size
        if changes.ram_gb:
            vm.specs["ram_gb"] = changes.ram_gb
        if changes.cpu:
            vm.specs["cpu"] = changes.cpu
        if changes.disk_gb:
            vm.specs["disk_gb"] = changes.disk_gb
        return vm

    def apply_action(self, vm: VMDTO, action: str) -> VMDTO:
        if action == "start":
            vm.status = "running"
        elif action == "stop":
            vm.status = "stopped"
        elif action == "restart":
            vm.status = "running"
        else:
            raise ValueError("Invalid action")
        return vm
