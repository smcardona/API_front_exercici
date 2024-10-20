from typing import List, Optional
from fastapi import APIRouter, HTTPException, UploadFile
from api.classes import Alumne, TableAlumne, DescribedAlumne
from api.internal import alumne as InterfaceAlumne, db_alumne, db_aula
import csv

router = APIRouter()


@router.get("/alumne/list", response_model=List[TableAlumne])
def list_alumnes(
  orderby: Optional[str] = None,  
  contain: Optional[str] = None, 
  skip: int = 0, 
  limit: int = 0
  ):
  
  result = db_alumne.read(orderby, contain, skip, limit)
  
  alumnes = InterfaceAlumne.alumnes_schema(result)
  return alumnes

@router.get("/alumne/show/{id}", response_model=TableAlumne) # response_model=Alumne
def show_alumne(id: int):
  result = db_alumne.read_one(id)
  
  if result is None:
    raise HTTPException(status_code=404, detail="Item not found")

  alumne = InterfaceAlumne.alumne_schema(result)
  return alumne

@router.post("/alumne/add")
def create_alumne(data: Alumne):
  nom= data.nom
  cicle= data.cicle
  curs= data.curs
  grup= data.grup
  id_aula= data.id_aula
  
  if not db_aula.check_aula_exists(id_aula):
    raise HTTPException(status_code=400, detail=f"No hi ha aula amb l'id: {id_aula}")
  
  response = db_alumne.create_one(nom, cicle, curs, grup, id_aula)
  
  return { "status": "S'ha afegit correctement", "id": response }

@router.put("/alumne/{id}")
def update_alumne(id: int, data: Alumne):
  # Comprobacio d'alumne
  if not db_alumne.check_alumne_exists(id):
    raise HTTPException(status_code=400, detail=f"No hi ha alumne amb l'id: {id}")
  # Comprobacio d'aula
  if not db_aula.check_aula_exists(data.id_aula):
    raise HTTPException(status_code=400, detail=f"No hi ha aula amb l'id: {data.id_aula}")
  
  response = db_alumne.update_one(
    id, data.nom, data.cicle, data.curs, data.grup, data.id_aula)
  
  schema = InterfaceAlumne.raw_alumne_schema(response)
  
  return { "status": "S'ha modificat correctement", "new_value": schema }


@router.delete("/alumne/all")
def delete_all(key: str):
  if (key == "1234ñ"):
    affected = db_alumne.wipe_data()
    affected += db_aula.wipe_data()
    
    return {"status": "S'han eliminat totes les dades", "affected": affected}
  
  else:
    raise HTTPException(status_code=403, detail="Contrasenya incorrecte")


@router.delete("/alumne/{id}")
def delete_alumne(id: int):
  # Comprobacio d'alumne
  if not db_alumne.check_alumne_exists(id):
    raise HTTPException(status_code=400, detail=f"No hi ha alumne amb l'id: {id}")
  
  response = db_alumne.delete_one(id)
  
  alumne_esborrat = InterfaceAlumne.raw_alumne_schema(response)
  
  return { "status": "S'ha esborrat correctament", "dades": alumne_esborrat }

@router.get("/alumne/listAll", response_model=List[DescribedAlumne])
def describe_alumnes():
  response = db_alumne.describe_all()
  
  infos: List[dict] = []
  for data in response:
    infos.append(InterfaceAlumne.described_alumne_schema(data))
  
  return infos

@router.post("/alumne/loadAlumnes")
def load_bulk_alumnes(file: UploadFile):
  content = file.file.read().decode()
  # Transformando archivo a un Iterable de lists de datos
  datos = csv.reader(content.splitlines(), delimiter=",")
  # Elimina la cabecera
  next(datos)
  # Grupo de respuestas
  responses = []
  for dato in datos:
    try:
      # Formato de dato: [DescAula, Edifici, Pis, NomAlumne, Cicle, Curs, Grup]
      status: str
      aula = db_aula.read_one(dato[0])
      id_aula: int
      if aula is None:
        status = "S'ha afegit aula correctament, "
        id_aula = db_aula.create_one(dato[0], dato[1], dato[2])
      else:
        status = "Aula ja existeix, "
        id_aula = aula[0]
      
      # Comprobación de alumno
      alumne = db_alumne.read_one_raw_nom(dato[3])
      id_alumne: int
      if alumne is None:
        status += "s'ha afegit alumne correctament"
        id_alumne = db_alumne.create_one(
          dato[3], dato[4], dato[5], dato[6], id_aula
        )
      else: 
        status += "alumne ja existeix"
        id_alumne = alumne[0]
      
      
      responses.append({
        "status": status,
        "id_alumne": id_alumne,
        "id_aula": id_aula,
        "input": ",".join(dato)
      })
    except HTTPException as e:
      responses.append(e.detail) # En caso de error, lo agrega sin afectar los demas inserts
    except Exception as e:
      responses.append({
        "info": "Error llegint csv",
        "error": str(e),
        "input": ",".join(dato)
      })
    
    
  return responses

    