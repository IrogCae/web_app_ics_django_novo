import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from pandas import isna
from ics_app.models import Pleito

class Command(BaseCommand):
    help = "Importa a aba 'PLEITOS' do Excel para o modelo Pleito"

    def handle(self, *args, **options):
        path = settings.EXCEL_PATH.get('Pleitos') or settings.EXCEL_PATH['Projetos']
        xls  = pd.ExcelFile(path)
        df   = xls.parse(sheet_name="PLEITOS")

        # 1) Padroniza colunas
        df.columns = df.columns.str.strip().str.upper()

        # 2) Datas (mantém NaT)
        date_cols = [
            "DATA PLEITO", "DATA CID ENVIADO", "DATA CID RECEBIDO",
            "DATA SAIC", "DATA ANÁLISE FINAL"
        ]
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors="coerce")

        # 3) Numéricos (fillna(0))
        num_cols = [
            "Nº SURVEY","PLEITO INICIAL","PLEITO VALIDADO",
            "PLEITO VALOR FINAL","VALOR DE REDUÇÃO","COST AVOIDANCE",
            "ANÁLISE DE VOLUME"
        ]
        for col in num_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # 4) Texto (fillna(""))
        text_cols = [
            "ORIGEM PLEITO","SAP SUPPLIER","FORNECEDOR SOLICITADO",
            "PROJETO SURVEY","ANALISTA RESPONSÁVEL","VALIDAÇÃO COMERCIAL",
            "VALIDAÇÃO SQD","RESPONSABILIDADE SORTING","STATUS PLEITO",
            "ID PLEITO","ORIENTATIVO"
        ]
        df[text_cols] = df[text_cols].fillna("")

        # 5) Bulk create
        Pleito.objects.all().delete()
        objs = []
        for _, row in df.iterrows():
            objs.append(Pleito(
                data_pleito              = row["DATA PLEITO"].date() if not isna(row["DATA PLEITO"]) else None,
                origem_pleito            = row["ORIGEM PLEITO"],
                nro_survey               = int(row["Nº SURVEY"]),
                sap_supplier             = row["SAP SUPPLIER"],
                fornecedor_solicitado    = row["FORNECEDOR SOLICITADO"],
                projeto_survey           = row["PROJETO SURVEY"],
                pleito_inicial           = row["PLEITO INICIAL"],
                pleito_validado          = row["PLEITO VALIDADO"],
                pleito_valor_final       = row["PLEITO VALOR FINAL"],
                valor_reducao            = row["VALOR DE REDUÇÃO"],
                cost_avoidance           = row["COST AVOIDANCE"],
                analista_responsavel     = row["ANALISTA RESPONSÁVEL"],
                data_cid_enviado         = row["DATA CID ENVIADO"].date() if not isna(row["DATA CID ENVIADO"]) else None,
                data_cid_recebido        = row["DATA CID RECEBIDO"].date() if not isna(row["DATA CID RECEBIDO"]) else None,
                analise_de_volume        = row["ANÁLISE DE VOLUME"],
                validacao_comercial      = row["VALIDAÇÃO COMERCIAL"],
                validacao_sqd            = row["VALIDAÇÃO SQD"],
                data_saic                = row["DATA SAIC"].date() if not isna(row["DATA SAIC"]) else None,
                responsabilidade_sorting = row["RESPONSABILIDADE SORTING"],
                status_pleito            = row["STATUS PLEITO"],
                data_analise_final       = row["DATA ANÁLISE FINAL"].date() if not isna(row["DATA ANÁLISE FINAL"]) else None,
                id_pleito                = row["ID PLEITO"],
                #id_pleito_extendido      = row["ID PLEITO EXTENDIDO"],
                orientativo              = row["ORIENTATIVO"],
            ))
        Pleito.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS("Importação de Pleitos concluída."))
