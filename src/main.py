import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.config import APP_NAME
from src.file_management.router import router as router_file_management

app = FastAPI(title=APP_NAME)

app.include_router(router_file_management)


@app.get('/healthcheck', response_class=JSONResponse)
async def get_healthcheck_response():
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'It works!'})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8765)
