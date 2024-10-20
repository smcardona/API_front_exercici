from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.routers import alumne

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alumne.router)

@app.get("/")
def root():
  return "200 ey"


# Para que no pete el sistema cuando la petición está mala
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
  print(exc.errors())
  return JSONResponse(
      status_code=422,
      content={"detail": exc.errors()},
  )
  
# , "body": exc.body
