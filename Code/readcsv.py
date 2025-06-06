import csv
import re
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field

# Reutilizamos o Vertice já definido em grafo.py
from grafo import Vertice

# ------------------------------ MODELOS ---------------------------------- #
@dataclass
class Trecho:
    _id: int
    id_base_trecho: int
    id_rdagu: int
    larg_inicio: float
    larg_final: float
    lado_rdagu: str
    ind_rdagu: str
    data: Optional[str]
    geometria: str                          # texto bruto do CSV
    vertices: List[Vertice] = field(default_factory=list)  # gerados a partir de geometria


# -------------------- parser do campo GEOMETRIA -------------------------- #

def parse_vertices(geom: str, prefixo: str) -> List[Vertice]:
    """Converte 'LINESTRING (x1 y1, x2 y2, ...)' em lista de Vertice (classe grafo.Vertice).
    Cada vértice recebe um id composto pelo prefixo + índice (prefixo_i).
    """
    coords_txt = geom[geom.find("(") + 1 : geom.rfind(")")]
    pares = [p.strip() for p in coords_txt.split(",") if p.strip()]

    vertices: List[Vertice] = []
    for idx, par in enumerate(pares, start=1):
        x_str, y_str = re.split(r"\s+", par, maxsplit=1)
        vertices.append(Vertice(f"{prefixo}_{idx}", float(x_str), float(y_str)))
    return vertices


# -------------------------- leitura do CSV ------------------------------ #

def carregar_trechos_do_csv(arquivo: str | Path) -> List[Trecho]:
    caminho = Path(arquivo)
    if not caminho.exists():
        raise FileNotFoundError(f"CSV não encontrado: {caminho}")

    trechos: List[Trecho] = []

    with caminho.open(newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            geom_str = row["GEOMETRIA"]
            prefixo_id = row["_id"]
            trecho = Trecho(
                _id=int(prefixo_id),
                id_base_trecho=int(row["ID_BASE_TRECHO"]),
                id_rdagu=int(row["ID_RDAGU"]),
                larg_inicio=float(row["LARG_INICIO"]),
                larg_final=float(row["LARG_FINAL"]),
                lado_rdagu=row["LADO_RDAGU"],
                ind_rdagu=row["IND_RDAGU"],
                data=row["DATA"] if row["DATA"] else None,
                geometria=geom_str,
                vertices=parse_vertices(geom_str, prefixo_id),
            )
            trechos.append(trecho)
    return trechos


# -------------------------- teste rápido --------------------------------- #
if __name__ == "__main__":
    csv_path = Path(__file__).with_name("rede.csv")
    for t in carregar_trechos_do_csv(csv_path)[:2]:
        print(t._id, "->", len(t.vertices), "vértices")
