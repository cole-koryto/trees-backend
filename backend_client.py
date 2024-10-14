from fastapi import FastAPI
from schemas.input_schemas import TreeInputPayload
import uvicorn

# configure FastAPI
app = FastAPI()


@app.post("/")
def main():


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)