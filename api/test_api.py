#!/usr/bin/env python3
"""
API de teste simplificada para verificar se o FastAPI está funcionando
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="EcoRota Test API")

@app.get("/")
async def root():
    return {"message": "EcoRota Angola API funcionando!"}

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "API funcionando"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
