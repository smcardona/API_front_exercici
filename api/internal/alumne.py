from typing import List
from api.classes import Alumne, TableAlumne, DescribedAlumne

def alumne_schema(data) -> TableAlumne:
    return {
        "NomAlumne": data[0],
        "Cicle": data[1],
        "Curs": data[2],
        "Grup": data[3],
        "DescAula": data[4]
    }


def alumnes_schema(alumnes) -> List[TableAlumne]:
    return [alumne_schema(alumne) for alumne in alumnes]

def raw_alumne_schema(data) -> Alumne:
    return {
        "id": data[0],
        "id_aula": data[1],
        "nom": data[2],
        "cicle": data[3],
        "curs": data[4],
        "grup": data[5],
        "created_at": data[6],
        "updated_at": data[7]
    }
    
def raw_alumnes_schema(alumnes) -> List[Alumne]:
    return [raw_alumne_schema(alumne) for alumne in alumnes]

def described_alumne_schema(data) -> DescribedAlumne:
    return {
        "id": data[0],
        "nom": data[1],
        "cicle": data[2],
        "curs": data[3],
        "grup": data[4],
        "desc_aula": data[5],
        "edifici": data[6],
        "pis": data[7]
    }