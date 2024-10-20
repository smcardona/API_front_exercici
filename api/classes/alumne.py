from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Alumne(BaseModel):
  id_aula: int
  nom: str
  cicle: str
  curs: str
  grup: str
  crated_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  
class TableAlumne(BaseModel):
  NomAlumne: str
  Cicle: str
  Curs: str
  Grup: str
  DescAula: str
  
class DescribedAlumne(BaseModel):
  id: int
  nom: str
  cicle: str
  curs: str
  grup: str
  desc_aula: str
  edifici: str
  pis: int
  