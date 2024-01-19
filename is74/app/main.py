import uvicorn
from fastapi import FastAPI

from app.api.routers import all_routers

app = FastAPI(title='is74')

for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
