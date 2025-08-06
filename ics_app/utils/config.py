# Configurações e caminhos do ICS App.

from pathlib import Path
from typing import Dict, List

# NOVO BASE_DIR aponta para a raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent


EXCEL_PATH: Dict[str, str] = {
    "Projetos": str(BASE_DIR / "data" / "PROJECT MANAGEMENTS.xlsx"),
}

IGNORE_SHEETS: List[str] = [
    "DROPLIST",
    "BASE FORNECEDORES 22-05-2025",
    "OUT CAPACITY"
]

HEADER_MAP: Dict[str, int] = {
    'data': 0,  # para as surveys, assumimos header na linha 0
}

ANALISTAS: List[str] = [
    "OSMAIR GONÇALVES",
    "DETLEY GOMES",
    "MOISÉS TORRES",
    "POLLYANNA PINHEIRO",
    "GABRIEL MONTEIRO",
    "THIAGO FEU",
    "FLÁVIA MARQUES",
    "KEDMA ALVES",
    "JÉSSICA RIBEIRO",
    "VINCENT PERNARH",
    "AMANDA PENA",
    "LUCAS OLIVEIRA",
    "ISABELA SANTOS",
    "AMANDA PENA",
    "WESLEY BASILIO",
]

RESPONSABILIDADES: List[str] = [
    "CAPACITY SUPPLIER",
    "CAPEX SUPPLIER",
    "PACKAGING",
    "PLATAFORM VEHICLE",
    "PURCHASING",
    "RETOOLING/SQD",
    "SDRM",
    "SEMICONDUTOR",
    "STRADA 770 2810",
    "SUPPLIER INVESTMENT",
    "SURVEY MOBI PL8",
]