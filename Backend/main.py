from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
async def run():
    return {"hello":"world"}

