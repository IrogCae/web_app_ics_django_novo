#!/usr/bin/env python
import os
import pandas as pd
import re

# 1) Defina os diretórios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # onde está este script
DATA_DIR = os.path.join(BASE_DIR, 'data')              # pasta data/ ao lado

# 2) Mapeie cada classe ao seu arquivo Excel
file_paths = {
    'DadosIniciativa'           : os.path.join(DATA_DIR, 'base_completa_iniciativa.xlsx'),
    'DadosPedidosAdiantados'    : os.path.join(DATA_DIR, 'dados_pedidos_adiantados.xlsx'),
    'DadosPedidosAQ'            : os.path.join(DATA_DIR, 'dados_pedidos_aq.xlsx'),
    'DadosPedidosPagos'         : os.path.join(DATA_DIR, 'dados_pedidos_pagos.xlsx'),
    'DadosPedidosPendentes'     : os.path.join(DATA_DIR, 'dados_pedidos_pendentes.xlsx'),
}

def snake_case(s: str) -> str:
    """
    Converte 'Nome da Coluna' em 'nome_da_coluna'
    """
    # substitui qualquer coisa que não seja letra/dígito por underscore
    s = re.sub(r'[^0-9a-zA-Z]+', '_', s).strip('_')
    #  evita underscores duplicados e coloca tudo em minúsculas
    s = re.sub(r'_+', '_', s).lower()
    # adiciona underscore se começar com dígito
    if re.match(r'^\d', s):
        s = '_' + s
    return s

if __name__ == '__main__':
    for model_name, path in file_paths.items():
        # 3) checa existência do arquivo
        if not os.path.exists(path):
            print(f"Arquivo não encontrado, pulando: {path}")
            continue

        # 4) lê somente os cabeçalhos (nrows=0)
        df = pd.read_excel(path, nrows=0)
        cols = df.columns.tolist()

        # 5) imprime a classe Django
        print("from django.db import models\n")
        print(f"class {model_name}(models.Model):")
        for col in cols:
            field = snake_case(col)
            print(f"    {field} = models.CharField(" 
                  f"\"{col}\", max_length=255, blank=True, null=True)")
        print("\n    class Meta:")
        print(f"        db_table = \"{model_name.lower()}\"")
        # ajusta verbose_name para o singular e plural
        singular = model_name.replace('DadosPedidos', 'Pedido ').replace('DadosIniciativa','Iniciativa').strip()
        plural   = singular + 's'
        print(f"        verbose_name = \"{singular}\"")
        print(f"        verbose_name_plural = \"{plural}\"\n\n")
