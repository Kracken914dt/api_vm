from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any
from app.domain.schemas import ProviderEnum, VMDTO, VMUpdateRequest
import uuid


class VirtualMachineFactory(ABC):
    @abstractmethod
    def validate_params(self, params: Dict[str, Any]) -> None:
        ...

    @abstractmethod
    def provision(self, name: str, params: Dict[str, Any]) -> VMDTO:
        ...

    @abstractmethod
    def update(self, vm: VMDTO, changes: VMUpdateRequest) -> VMDTO:
        ...

    @abstractmethod
    def apply_action(self, vm: VMDTO, action: str) -> VMDTO:
        ...


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


def get_factory(provider: ProviderEnum) -> VirtualMachineFactory:
    mapping = {
        ProviderEnum.aws: AWSVMFactory(),
        ProviderEnum.azure: AzureVMFactory(),
        ProviderEnum.gcp: GCPVMFactory(),
        ProviderEnum.onpremise: OnPremiseVMFactory(),
    }
    if provider not in mapping:
        raise ValueError("Unsupported provider")
    return mapping[provider]
