from app.domain.factories.aws import AWSVMFactory
from app.domain.factories.azure import AzureVMFactory
from app.domain.factories.gcp import GCPVMFactory
from app.domain.factories.onprem import OnPremiseVMFactory
from app.domain.schemas import ProviderEnum
from app.domain.factories.base import VirtualMachineFactory


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
