from __future__ import annotations
from typing import Dict, Any
from app.domain.schemas import VMDTO, ProviderEnum, VMUpdateRequest
from app.domain.factories.base import VirtualMachineFactory
import uuid


class GCPVMFactory(VirtualMachineFactory):
    def validate_params(self, params: Dict[str, Any]) -> None:
        required = ["machine_type", "zone", "base_disk", "project"]
        missing = [k for k in required if k not in params]
        if missing:
            raise ValueError(f"Missing GCP params: {missing}")

    def provision(self, name: str, params: Dict[str, Any]) -> VMDTO:
        self.validate_params(params)
        vm_id = f"gcp-{uuid.uuid4()}"
        specs = {
            "machine_type": params["machine_type"],
            "zone": params["zone"],
            "base_disk": params["base_disk"],
            "project": params["project"],
        }
        return VMDTO(id=vm_id, name=name, provider=ProviderEnum.gcp, status="stopped", specs=specs)

    def update(self, vm: VMDTO, changes: VMUpdateRequest) -> VMDTO:
        if changes.machine_type:
            vm.specs["machine_type"] = changes.machine_type
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
