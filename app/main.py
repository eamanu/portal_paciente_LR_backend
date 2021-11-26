from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Bienvenido al Portal de Pacientes de La Rioja"}
