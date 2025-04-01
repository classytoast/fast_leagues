from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/")
def start():
    return "top here"


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host='0.0.0.0')