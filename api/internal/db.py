from mysql import connector
from fastapi.exceptions import HTTPException
import traceback

class DBConnectionError(Exception): 
  def __init__(self, message):
    super().__init__(message)
    

def db_client():
  try:
    dbname = "alumnat"
    user = "root"
    password = "system"
    host = "localhost"
    port = "3306"
    collation = "utf8mb4_general_ci"
    
    return connector.connect(
      host = host,
      port = port,
      user = user,
      password = password,
      database = dbname,
      collation = collation
    ) 
      
  except Exception as e:
    raise DBConnectionError(f"Error de connexió: {e}")
  

""" 
Este decorador lo he creado para evitarme tantos try_catch dentro 
de todo el proyecto. Permite encapsular las funciones pasadas despues del decorador.
Las encapsula dentro de un try catch general que transforma los posibles errores
a HTTPExceptions para ser manejadas facilmente por fastAPI.
Obviamente al ser cosas avanzadas me tuve que ayudar de internet.
"""
# Decorador para encapsular manejo de excepciones
def db_exception_handler(func):
  def wrapper(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except HTTPException as e: raise e  # Deja que las HTTPExceptions se manejen por FastAPI
    except DBConnectionError as e:
      print(traceback.format_exc())
      raise HTTPException(
        status_code=500,
        detail=f"Error de conexió a la base de dades: {e}"
      )
    except connector.Error as e:
      print(traceback.format_exc())
      raise HTTPException(
        status_code=500, 
        detail={
          "info": f"Error a la base de dades",
          "error": str(e)
        }
      )
    except Exception as e:
      print(traceback.format_exc())
      raise HTTPException(status_code=500, detail={
        "info": f"Error inesperat",
        "error": str(e)
      })
  return wrapper
  


