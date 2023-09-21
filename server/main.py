import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from server.iban.api.router import router as iban_router

origins = [
    "*"
]
middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
]

app = FastAPI(middleware=middlewares)

app.include_router(iban_router, tags=['iban'])


@app.get("/")
async def root():
    return {
        "name": "Iban checker",
        "version": "1.0.0"
    }


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=os.getenv("APP_PORT", 8000)
    )
