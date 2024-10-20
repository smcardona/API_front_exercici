from typing import Optional
from api.internal import db_client, db_exception_handler


@db_exception_handler
def read(
  orderby: Optional[str],  contain: Optional[str], 
  skip: int = 0, limit: int = 0):
  
  with db_client() as conn: # cliente de conexion a la bd
    cur = conn.cursor() # ejecutor / cursor
    query = """SELECT al.nom, al.cicle, al.curs, al.grup, au.desc, au.id
      FROM alumne al JOIN aula au ON (al.id_aula = au.id)"""
      
    params = []
        
    # Añadir filtro por "contain"
    if contain is not None:
      query += " WHERE al.nom LIKE %s"
      params.append(f"%{contain}%")
    
    # Añadir orden
    if orderby is not None:
      query += " ORDER BY al.nom " + orderby
    
    # Añadir limit y offset
    if limit > 0:
      query += " LIMIT %s"
      params.append(limit)
      if skip > 0: # skip only if has limit
        query += " OFFSET %s"
        params.append(skip)
    

    cur.execute(query, tuple(params)) # ejecuta y devuelve un generador de datos para python | interfaz
    alumnes = cur.fetchall() # Lista de valores valor[][]
    
    return alumnes

@db_exception_handler
def read_one_raw(id: int):
  with db_client() as conn:
    cur = conn.cursor()
    query = "SELECT * FROM alumne WHERE id = %s"
    params = (id, )
    
    cur.execute(query, params)
    alumne = cur.fetchone()
    return alumne

@db_exception_handler
def read_one_raw_nom(nom: str): 
  with db_client() as conn:
    cur = conn.cursor()
    query = "SELECT * FROM alumne WHERE LOWER(nom) = %s"
    params = (nom, )
    
    cur.execute(query, params)
    alumne = cur.fetchone()
    return alumne

@db_exception_handler
def read_one(id: int):
  with db_client() as conn:
    cur = conn.cursor()
    query = """
      SELECT al.nom, al.cicle, al.curs, al.grup, au.desc
      FROM alumne al JOIN aula au ON (al.id_aula = au.id)
      WHERE al.id = %s
      """
    params = (id, )
    
    cur.execute(query, params)
    alumne = cur.fetchone()
    return alumne

@db_exception_handler
def create_one(nom: str, cicle: str, curs: str, grup: str, id_aula: int, id: Optional[int] = None):
  with db_client() as conn:
    cur = conn.cursor()
    if id is not None:
      query = """INSERT INTO alumne (id, nom, id_aula, cicle, curs, grup)
                  VALUES (%s, %s, %s, %s, %s, %s)"""
      values = (id, nom, id_aula, cicle, curs, grup)
    else:
      query = """INSERT INTO alumne (nom, id_aula, cicle, curs, grup)
                  VALUES (%s, %s, %s, %s, %s)"""
      values = (nom, id_aula, cicle, curs, grup)
    
    cur.execute(query, values)
    conn.commit()
    return cur.lastrowid

@db_exception_handler
def update_one(id: int, nom: str, cicle: str, curs: str, grup: str, id_aula: int ):
  with db_client() as conn:
    cur = conn.cursor()
    query = "UPDATE alumne SET nom = %s, id_aula = %s, cicle = %s, curs = %s, grup = %s WHERE id = %s"
    values = (nom, id_aula, cicle, curs, grup)
    params = (*values, id)
    
    cur.execute(query, params)
    conn.commit()
    return read_one(id)

@db_exception_handler
def delete_one(id: int):
  with db_client() as conn:
    previous = read_one_raw(id)
    cur = conn.cursor()
    query = "DELETE FROM alumne WHERE id = %s"

    cur.execute(query, (id,))
    conn.commit()
    return previous

@db_exception_handler
def describe_all():
  with db_client() as conn:
    cur = conn.cursor()
    query = """
      SELECT al.id, al.nom, al.cicle, al.curs, al.grup, au.desc, au.edifici, au.pis
      FROM alumne al JOIN aula au ON (al.id_aula = au.id)
      """

    cur.execute(query)
    dades = cur.fetchall()
    return dades

@db_exception_handler
def check_alumne_exists(id: int) -> bool:
  with db_client() as conn:
    cur = conn.cursor()
    query = "SELECT * FROM alumne WHERE id = %s"
    
    cur.execute(query, (id,))
    return cur.fetchone() is not None
  
@db_exception_handler
def wipe_data():
  with db_client() as conn:
    cur = conn.cursor()
    query = "DELETE FROM alumne;"
    cur.execute(query)
    affected = cur.rowcount
    cur.execute("ALTER TABLE alumne AUTO_INCREMENT = 1;")
    conn.commit()
    
    return affected