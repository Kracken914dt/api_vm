from __future__ import annotations
from typing import Dict, Any
from app.domain.schemas import VMDTO, ProviderEnum, VMUpdateRequest
from app.domain.factories.base import VirtualMachineFactory
import uuid


class AWSVMFactory(VirtualMachineFactory):
    def validate_params(self, params: Dict[str, Any]) -> None:
        required = ["instance_type", "region", "vpc", "ami"]
        missing = [k for k in required if k not in params]
        if missing:
            raise ValueError(f"Missing AWS params: {missing}")

    def provision(self, name: str, params: Dict[str, Any]) -> VMDTO:
        self.validate_params(params)
        vm_id = f"aws-{uuid.uuid4()}"
        specs = {
            "instance_type": params["instance_type"],
            "region": params["region"],
            "vpc": params["vpc"],
            "ami": params["ami"],
        }
        return VMDTO(id=vm_id, name=name, provider=ProviderEnum.aws, status="stopped", specs=specs)

    def update(self, vm: VMDTO, changes: VMUpdateRequest) -> VMDTO:
        if changes.instance_type:
            vm.specs["instance_type"] = changes.instance_type
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
