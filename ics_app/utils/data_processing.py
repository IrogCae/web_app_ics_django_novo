from datetime import datetime
import logging
import os
from pathlib import Path
from typing import List, Tuple, Any
import json

import numpy as np
import pandas as pd

from .config import EXCEL_PATH, IGNORE_SHEETS, HEADER_MAP, SURVEY_DIR
from .exceptions import DataProcessingError
from ics_app.models import RdaSemPedido

logger = logging.getLogger(__name__)


def list_sheets(tab: str) -> List[str]:
    """Lista as sheets de um único Excel (abordagem antiga)."""
    path = EXCEL_PATH.get(tab)
    if not path:
        logger.error("Chave EXCEL_PATH não encontrada ou vazia: %s", tab)
        return []
    try:
        xls = pd.ExcelFile(path)
        return [str(s) for s in xls.sheet_names if isinstance(s, str) and s not in IGNORE_SHEETS]
    except Exception as e:
        logger.exception("Falha ao ler sheets do Excel (%s): %s", path, e)
        return []


def _remove_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Remove linhas onde todos os valores sejam NaN, strings vazias ou zero."""
    def is_empty(x):
        if pd.isna(x):
            return True
        if isinstance(x, str) and not x.strip():
            return True
        if isinstance(x, (int, float, np.integer, np.floating)) and x == 0:
            return True
        return False

    mask = df.apply(lambda col: col.map(is_empty))
    return df.loc[~mask.all(axis=1)]


def load_dataframe(tab: str, sheet: str) -> pd.DataFrame:
    """
    Carrega um único DataFrame de um Excel, buscando a sheet
    case-insensitive e limpando linhas vazias.
    """
    path = EXCEL_PATH.get(tab)
    if not path:
        raise DataProcessingError(f"Chave de arquivo não encontrada: {tab}")

    try:
        xls = pd.ExcelFile(path)
        # encontra o nome real da sheet, ignorando case
        match = next((s for s in xls.sheet_names if isinstance(s, str) and s.lower() == sheet.lower()), None)
        if not match:
            raise DataProcessingError(
                f"Aba '{sheet}' não encontrada em {xls.sheet_names}"
            )
        header_row = HEADER_MAP.get(match.lower(), 0)
        df = pd.read_excel(path, sheet_name=match, header=header_row)
        df = df.replace(r'^\s*$', pd.NA, regex=True)
        return _remove_empty_rows(df)

    except DataProcessingError:
        # repassa nossa exceção customizada
        raise
    except Exception as e:
        logger.exception("Erro ao carregar DataFrame (%s - %s): %s", tab, sheet, e)
        raise DataProcessingError(f"Erro ao carregar aba '{sheet}': {e}")



def filter_pleitos(df: pd.DataFrame, id_pleito: str) -> pd.DataFrame:
    """Filtra pelo ID PLEITO."""
    if id_pleito:
        return df[df['ID PLEITO'].astype(str) == id_pleito]
    return df


def filter_analista(df: pd.DataFrame, analista: str) -> pd.DataFrame:
    """Filtra pela coluna 'ANALISTA RESPONSÁVEL'."""
    col = 'ANALISTA RESPONSÁVEL'
    if col not in df.columns:
        raise DataProcessingError(f"Coluna '{col}' não encontrada em {df.columns.tolist()}")
    if analista:
        mask = df[col].astype(str).str.strip().eq(analista.strip())
        return df.loc[mask]
    return df

def filter_by_column(df: pd.DataFrame, column: str, value: str) -> pd.DataFrame:
    """
    Filtra DataFrame pela coluna exata (case-sensitive).
    Se a coluna não existir ou valor for vazio, retorna df original.
    """
    if not value or column not in df.columns:
        return df
    mask = df[column].astype(str).str.strip().str.contains(value, case=False, na=False)
    return df.loc[mask]


def df_to_html(df: pd.DataFrame) -> str:
    """Converte DataFrame em HTML com classes Bootstrap."""
    return df.astype(str).to_html(
        classes="table table-sm table-striped table-bordered",
        index=False,
        border=0
    )


def compute_survey_metrics(df_survey: pd.DataFrame) -> Tuple[int, str, str]:
    """
    Calcula total de surveys e % de resposta para cada uma,
    retornando (n_surveys, survey_codes_json, response_rates_json).
    """
    cols_map = {c.lower(): c for c in df_survey.columns}
    survey_col = cols_map.get('survey code')
    sap_col    = cols_map.get('sap code')
    version_col= cols_map.get('version')
    status_col = cols_map.get('status')
    if not all([survey_col, sap_col, version_col, status_col]):
        missing = [k for k,v in [
            ('Survey Code', survey_col),
            ('Sap Code', sap_col),
            ('Version', version_col),
            ('Status', status_col)
        ] if v is None]
        raise DataProcessingError(f"Faltando colunas: {missing}")

    n_surveys = df_survey[survey_col].nunique()

    if version_col is None:
        raise DataProcessingError("Coluna 'Version' não encontrada para ordenação.")

    latest = (
        df_survey
        .sort_values(version_col)
        .groupby([survey_col, sap_col], as_index=False)
        .last()
    )

    idx = df_survey.columns.get_loc(status_col)
    resp_cols = list(df_survey.columns[idx:])

    latest['respondido'] = latest[resp_cols].notna().any(axis=1)

    stats = (
        latest
        .groupby(survey_col)
        .agg(
            total_suppliers     = (sap_col, 'nunique'),
            suppliers_responded = ('respondido', 'sum'),
        )
        .assign(
            response_rate=lambda d: d['suppliers_responded'] / d['total_suppliers'] * 100
        )
        .reset_index()
    )

    stats_dict = stats.to_dict(orient='list')
    return (
        n_surveys,
        json.dumps(stats_dict[survey_col]),
        json.dumps(stats_dict['response_rate'])
    )


def list_survey_files() -> List[str]:
    """Retorna caminhos de todos os .xls[x] em SURVEY_DIR."""
    files = []
    for fname in os.listdir(SURVEY_DIR):
        if fname.lower().endswith(('.xls', '.xlsx')):
            files.append(str(SURVEY_DIR / fname))
    return files


def load_all_surveys() -> pd.DataFrame:
    """
    Lê e concatena cada Excel em SURVEY_DIR,
    adiciona coluna 'survey_file' com o nome do arquivo.
    """
    dfs = []
    for file_path in list_survey_files():
        try:
            df = pd.read_excel(file_path, header=HEADER_MAP.get('data', 0))
            df = df.replace(r'^\s*$', pd.NA, regex=True)
            df = _remove_empty_rows(df)
            df['survey_file'] = Path(file_path).stem
            dfs.append(df)
        except Exception as e:
            logger.exception("Erro ao carregar survey %s: %s", file_path, e)
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


def save_pleitos_dataframe(
    selected_id: str,
    analista: str,
    responsabilidade: str,
    id_iniciativa: str,
    cid_enviado: str
) -> None:
    """
    Atualiza o Excel de Projetos → sheet 'Pleitos' (case-insensitive),
    escrevendo nas colunas já existentes:
      - 'ANALISTA RESPONSÁVEL'
      - 'RESPONSABILIDADE SORTING'
      - 'ID INICIATIVA'
      - 'CID ENVIADO'
      - 'DATA ANÁLISE FINAL' (timestamp do envio)
    Se o Pleito não existir, adiciona uma linha nova.
    """
    path = EXCEL_PATH['Projetos']
    xls = pd.ExcelFile(path)
    sheet_name = next((s for s in xls.sheet_names if isinstance(s, str) and s.lower() == 'pleitos'), None)
    if not sheet_name:
        raise DataProcessingError(f"Aba 'Pleitos' não encontrada em {xls.sheet_names!r}")

    header_key = sheet_name.lower() if isinstance(sheet_name, str) else sheet_name
    header_row = HEADER_MAP.get(header_key, 0)
    df = pd.read_excel(path, sheet_name=sheet_name, header=header_row)
    df = df.replace(r'^\s*$', pd.NA, regex=True)

    # localização das colunas
    cols = {c.lower(): c for c in df.columns}
    col_id   = cols.get('id pleito')
    col_init = cols.get('id iniciativa')
    col_cid  = cols.get('cid enviado') or cols.get('cid')
    col_anal = cols.get('analista responsável')
    col_resp = cols.get('responsabilidade sorting')
    col_data = cols.get('data análise final')

    # se a coluna de data não existir, cria
    if col_data is None:
        col_data = 'DATA ANÁLISE FINAL'
        df[col_data] = pd.NA

    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    mask = df[col_id].astype(str).eq(selected_id)
    if mask.any():
        if col_anal: df.loc[mask, col_anal] = analista
        if col_resp: df.loc[mask, col_resp] = responsabilidade
        if col_init: df.loc[mask, col_init] = id_iniciativa
        if col_cid:  df.loc[mask, col_cid]  = cid_enviado
        df.loc[mask, col_data] = now
    else:
        new: dict[str, Any] = {c: pd.NA for c in df.columns}
        if col_id is not None and col_id in new:
            new[col_id] = selected_id if selected_id is not None else pd.NA
        if col_anal and col_anal in new:  new[col_anal] = analista if analista is not None else pd.NA  # type: ignore
        if col_resp and col_resp in new:  new[col_resp] = responsabilidade if responsabilidade is not None else pd.NA  # type: ignore
        if col_init and col_init in new:  new[col_init] = id_iniciativa if id_iniciativa is not None else pd.NA  # type: ignore
        if col_cid and col_cid in new:    new[col_cid]  = cid_enviado if cid_enviado is not None else pd.NA  # type: ignore
        if col_data and col_data in new:  new[col_data] = now if now is not None else pd.NA  # type: ignore
        df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)

    with pd.ExcelWriter(path,
                        engine='openpyxl',
                        mode='a',
                        if_sheet_exists='replace') as writer:
        df.to_excel(writer,
                    sheet_name=sheet_name,
                    index=False,
                    header=True,
                    startrow=header_row)

def save_projetos_dataframe(id_gerador: str, planta: str, analista: str) -> None:
    """
    Atualiza a aba 'Projetos' no Excel PROJECT MANAGEMENT.xlsx.
    Se já existir o ID GERADOR, atualiza os dados.
    Caso contrário, cria uma nova linha.
    """
    path = EXCEL_PATH['Projetos']
    xls = pd.ExcelFile(path)
    sheet_name = next((s for s in xls.sheet_names if isinstance(s, str) and s.lower() == 'projetos'), None)
    if not sheet_name:
        raise DataProcessingError(f"Aba 'Projetos' não encontrada em {xls.sheet_names!r}")

    header_row = HEADER_MAP.get(sheet_name.lower(), 0)
    df = pd.read_excel(path, sheet_name=sheet_name, header=header_row)
    df = df.replace(r'^\s*$', pd.NA, regex=True)

    # localiza colunas
    cols = {c.lower(): c for c in df.columns}
    col_id    = cols.get('gerador id projeto') or cols.get('id gerador')
    col_planta = cols.get('planta')
    col_analista = cols.get('analista')

    if col_id is None:
        raise DataProcessingError("Coluna 'ID GERADOR' não encontrada.")

    mask = df[col_id].astype(str).eq(id_gerador)
    if mask.any():
        if col_planta: df.loc[mask, col_planta] = planta
        if col_analista: df.loc[mask, col_analista] = analista
    else:
        new = {}
        new[col_id] = id_gerador
        if col_planta: new[col_planta] = planta
        if col_analista: new[col_analista] = analista
        # Fill missing columns with pd.NA
        for c in df.columns:
            if c not in new:
                new[c] = pd.NA
        df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)

    with pd.ExcelWriter(path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=str(sheet_name), index=False, header=True, startrow=header_row)


