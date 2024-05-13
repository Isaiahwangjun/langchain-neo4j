from fastapi import FastAPI, Request
from chain import chain
import uvicorn
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")


@app.post("/generator")
async def AISemantic(request: Request):

    inputData = await request.json()
    question = inputData.get('question')

    res = chain(question)
    return res


if __name__ == "__main__":
    uvicorn.run('main:app', host=HOST, port=int(PORT))
