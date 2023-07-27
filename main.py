import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from routers.mobility_seller import router

app = FastAPI()

app.include_router(router=router)


@app.get("/")
async def root():
    return {"message": "Mobility Mock Seller!!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
