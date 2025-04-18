from fastapi import FastAPI
import uvicorn

from api.leagues import router as leagues_router


app = FastAPI()
app.include_router(leagues_router)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host='0.0.0.0')