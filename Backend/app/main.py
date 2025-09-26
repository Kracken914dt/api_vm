from fastapi import FastAPI
from app.api.vm_controller import router as vm_router

app = FastAPI(title="VM FactoryMethod API", version="1.0.0")

app.include_router(vm_router, prefix="/vm", tags=["vm"])


@app.get("/health")
def health():
    return {"status": "ok"}
