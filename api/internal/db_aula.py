from typing import Optional
from mysql.connector import Error

from api.internal import db_client, db_exception_handler

@db_exception_handler
def check_aula_exists(id_aula: int) -> bool:
  conn = db_client()
  cur = conn.cursor()
  cur.execute("SELECT * FROM aula WHERE id = %s", (id_aula,))
  return cur.fetchone() is not None

@db_exception_handler
def check_aula_named_exists(desc: str) -> bool:
  conn = db_client()
  cur = conn.cursor()
  cur.execute(
    "SELECT * FROM aula a where LOWER(a.desc) = LOWER(%s)",
    (desc,)
  )
  
  return cur.fetchone() is not None

@db_exception_handler
def read_one(desc: str):
  
  with db_client() as conn: # cliente de conexion a la bd
    cur = conn.cursor() # ejecutor / cursor
    query = "SELECT * FROM aula a WHERE a.desc LIKE %s"
    
    cur.execute(query, (desc,)) # ejecuta y devuelve un generador de datos para python | interfaz
    aula = cur.fetchone() # Lista de valores valor[][]
    
    return aula
  
@db_exception_handler
def create_one(desc: str, edifici: str, pis: int, id: Optional[int] = None):
  if check_aula_named_exists(desc):
    raise Error(f"El aula amb la descripcio {desc} ja existeix")
  
  with db_client() as conn:
    cur = conn.cursor()
    if id is not None:
      print("id: "+str(id))
      query = "INSERT INTO aula (id, `desc`, edifici, pis) VALUES (%s, %s, %s, %s)"
      values = (id, desc, edifici, pis)
    else:
      query = "INSERT INTO aula (`desc`, edifici, pis) VALUES (%s, %s, %s)"
      values = (desc, edifici, pis)
    
    cur.execute(query, values)
    conn.commit()
    return cur.lastrowid
  
@db_exception_handler
def wipe_data():
  with db_client() as conn:
    cur = conn.cursor()
    query = "DELETE FROM aula"
    cur.execute(query)
    affected = cur.rowcount
    cur.execute("ALTER TABLE aula AUTO_INCREMENT = 1;")
    conn.commit()
    
    return affected