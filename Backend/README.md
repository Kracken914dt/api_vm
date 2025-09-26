# VM FactoryMethod API (FastAPI)

API que demuestra SOLID + Factory Method para gestión de VMs (AWS, Azure, GCP y On-Premise), con validación tipada por proveedor, persistencia simulada en memoria y logs de auditoría.

## Endpoints principales
- POST `/vm/create` crea una VM
- PUT `/vm/{id}` actualiza especificaciones
- DELETE `/vm/{id}` elimina
- POST `/vm/{id}/action` start|stop|restart
- GET `/vm/{id}` consulta una VM
- GET `/vm` lista todas las VMs
- GET `/health` estado del servicio

## Ejecutar
1) Instalar dependencias
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
2) Iniciar servidor
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
3) Documentación interactiva

http://localhost:8000/docs

## Requests de creación tipados por proveedor
La validación es estricta según `provider`. El campo `params` cambia de forma y es validado automáticamente por Pydantic.

- AWS
```json
{
  "provider": "aws",
  "name": "mi-vm-aws",
  "params": { "instance_type": "t2.micro", "region": "us-east-1", "vpc": "vpc-123", "ami": "ami-abc" },
  "requested_by": "alumno"
}
```

- Azure
```json
{
  "provider": "azure",
  "name": "mi-vm-azure",
  "params": { "size": "Standard_B1s", "resource_group": "rg1", "image": "UbuntuLTS", "vnet": "vnet-01" },
  "requested_by": "alumno"
}
```

- GCP
```json
{
  "provider": "gcp",
  "name": "mi-vm-gcp",
  "params": { "machine_type": "e2-micro", "zone": "us-central1-a", "base_disk": "pd-standard", "project": "demo-proj" },
  "requested_by": "alumno"
}
```

- On-Premise
```json
{
  "provider": "onpremise",
  "name": "mi-vm-onprem",
  "params": { "cpu": 4, "ram_gb": 8, "disk_gb": 50, "nic": "eth0" },
  "requested_by": "alumno"
}
```

## Diseño y arquitectura
- Patrón: Factory Method
  - Abstracción: `app/domain/factories/base.py` (`VirtualMachineFactory`)
  - Implementaciones: `aws.py`, `azure.py`, `gcp.py`, `onprem.py`
  - Resolución: `app/domain/factories/__init__.py#get_factory(provider)`
- Validación de entrada (DTOs):
  - `app/domain/schemas/common.py`: tipos comunes (ProviderEnum, VMDTO, etc.)
  - `app/domain/schemas/{aws,azure,gcp,onpremise}.py`: params por proveedor
  - `app/domain/schemas/create_requests.py`: `VMCreateRequest` (Union discriminado por `provider`)
- Servicios y puertos:
  - Servicio: `app/domain/services.py` (orquesta casos de uso)
  - Puerto de repo (DIP): `app/domain/ports.py` (`VMRepositoryPort`)
  - Implementación repo in-memory: `app/infrastructure/repository.py`
- API/Controller: `app/api/vm_controller.py`
- App FastAPI: `app/main.py`
- Logs: `app/infrastructure/logger.py` → `Backend/logs/audit.log`

## SOLID
- SRP: cada módulo tiene una responsabilidad clara (DTOs, fábricas por proveedor, servicio, repo, controller).
- OCP: agregar un proveedor es añadir su clase fábrica y sus DTOs, y registrarlo en `get_factory`.
- LSP: las fábricas concretas cumplen el contrato `VirtualMachineFactory`.
- ISP: contratos pequeños y específicos (puerto de repositorio).
- DIP: el servicio depende de `VMRepositoryPort` (abstracción), y el controller depende del servicio.

## Persistencia y estado
- Sin BD: persistencia simulada en memoria (dict) en `app/infrastructure/repository.py`.
- Stateless: la API no guarda estado de sesión; el repositorio in-memory simula almacenamiento volátil.

## Acciones y estados de VM
- `POST /vm/{id}/action` admite `start | stop | restart` y actualiza `status` a `running` o `stopped`.

## Logging de auditoría
- Formato JSON por línea con: timestamp, actor, acción, vm_id, provider, success, details.
- No se registran credenciales ni parámetros sensibles.
- Archivo: `Backend/logs/audit.log`.

## Extender con un nuevo proveedor
1. Crear `app/domain/schemas/<nuevo>.py` con los params del proveedor.
2. Añadir su variante en `create_requests.py`.
3. Implementar `VirtualMachineFactory` en `app/domain/factories/<nuevo>.py`.
4. Registrar en `get_factory` (`app/domain/factories/__init__.py`).
