from __future__ import annotations
from typing import Dict, Any
from app.domain.schemas import VMDTO, ProviderEnum, VMUpdateRequest
from app.domain.factories.base import VirtualMachineFactory
import uuid


class OnPremiseVMFactory(VirtualMachineFactory):
    def validate_params(self, params: Dict[str, Any]) -> None:
        required = ["cpu", "ram_gb", "disk_gb", "nic"]
        missing = [k for k in required if k not in params]
        if missing:
            raise ValueError(f"Missing On-Premise params: {missing}")

    def provision(self, name: str, params: Dict[str, Any]) -> VMDTO:
        self.validate_params(params)
        vm_id = f"onprem-{uuid.uuid4()}"
        specs = {
            "cpu": params["cpu"],
            "ram_gb": params["ram_gb"],
            "disk_gb": params["disk_gb"],
            "nic": params["nic"],
        }
        return VMDTO(id=vm_id, name=name, provider=ProviderEnum.onpremise, status="stopped", specs=specs)

    def update(self, vm: VMDTO, changes: VMUpdateRequest) -> VMDTO:
        if changes.cpu:
            vm.specs["cpu"] = changes.cpu
        if changes.ram_gb:
            vm.specs["ram_gb"] = changes.ram_gb
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
