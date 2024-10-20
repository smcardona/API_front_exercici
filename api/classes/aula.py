from pydantic import BaseModel
from datetime import datetime

class Aula(BaseModel):
  desc: str
  edifici: str
  pis: int  
  crated_at: datetime
  updated_at: datetime