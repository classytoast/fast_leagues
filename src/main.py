from fastapi import FastAPI
import uvicorn

from api.leagues import router as leagues_router
from api.teams import router as teams_router
from api.persons import router as persons_router


app = FastAPI()
app.include_router(leagues_router)
app.include_router(teams_router)
app.include_router(persons_router)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host='0.0.0.0')
