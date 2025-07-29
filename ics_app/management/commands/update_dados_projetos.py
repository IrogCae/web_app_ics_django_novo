# ics_app/management/commands/update_dados_projetos.py

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from pandas import isna
from ics_app.models import Projeto

class Command(BaseCommand):
    help = "Importa a aba 'PROJETOS' do Excel para o modelo Projeto"

    def handle(self, *args, **options):
        path = settings.EXCEL_PATH['Projetos']
        xls  = pd.ExcelFile(path)
        df   = xls.parse(sheet_name="PROJETOS")  # nome exato da aba

        # 1) Padroniza colunas: remove espaços e converte para UPPERCASE
        df.columns = df.columns.str.strip().str.upper()

        # 2) Trata datas (mantém NaT para vazios)
        date_cols = [
            "KICK OFF PROJETO",
            "LAST MEETING",
            "NEXT MEETING",
            "PO (DATA)",
            "DATA BENESTARE",
            "DATA PPAP FULL"
        ]
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors="coerce")

        # 3) Trata numéricos (preenche vazios com 0)
        num_cols = [
            "INVESTIMENTO APROVADO",
            "LEAD TIME SUPPLIER (MESES)",
            "LEAD TIME PROJETO (MESES)",
            "QTY REUNIÕES PREVISTAS",
            "QTY VISITAS PREVISTAS",
            "QTD REUNIÕES REALIZADAS",
            "QTD VISITAS REALIZADAS"
        ]
        for col in num_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # 4) Preenche apenas colunas de texto com ""
        text_cols = [
            "ID GERADOR","PLANTA","GERADOR ID PROJETO","ANALISTA","ORIGEM","SAP",
            "FORNECEDOR","PROJETO INVESTIMENTO","MODELOS","TIPO DE INVESTIMENTO",
            "APROVAÇÃO SAIC","APROVAÇÃO COMERCIAL","APROVAÇÃO VALIDAÇÃO TÉCNICA",
            "SOP TARGET","% DE CONCLUSÃO DO FERRAMENTAL","OTOP","SPV","IAA",
            "STATUS PROJETO","SOP EXECUTADO","STATUS SOP"
        ]
        df[text_cols] = df[text_cols].fillna("")

        # 5) Limpa tabela e faz bulk create
        Projeto.objects.all().delete()
        objs = []
        for _, row in df.iterrows():
            objs.append(Projeto(
                id_gerador                   = row["ID GERADOR"],
                planta                       = row["PLANTA"],
                gerador_id_projeto           = row["GERADOR ID PROJETO"],
                analista                     = row["ANALISTA"],
                origem                       = row["ORIGEM"],
                sap                          = row["SAP"],
                fornecedor                   = row["FORNECEDOR"],
                projeto_investimento         = row["PROJETO INVESTIMENTO"],
                modelos                      = row["MODELOS"],
                tipo_de_investimento         = row["TIPO DE INVESTIMENTO"],
                investimento_aprovado        = row["INVESTIMENTO APROVADO"],
                aprovacao_saic               = row["APROVAÇÃO SAIC"],
                kick_off_projeto             = row["KICK OFF PROJETO"].date() if not isna(row["KICK OFF PROJETO"]) else None,
                lead_time_supplier           = int(row["LEAD TIME SUPPLIER (MESES)"]),
                aprovacao_comercial          = row["APROVAÇÃO COMERCIAL"],
                aprovacao_validacao_tecnica  = row["APROVAÇÃO VALIDAÇÃO TÉCNICA"],
                lead_time_projeto            = row["LEAD TIME PROJETO (MESES)"],
                qty_reunioes_previstas       = int(row["QTY REUNIÕES PREVISTAS"]),
                qty_visitas_previstas        = int(row["QTY VISITAS PREVISTAS"]),
                sop_target                   = row["SOP TARGET"],
                qtd_reunioes_realizadas      = int(row["QTD REUNIÕES REALIZADAS"]),
                qtd_visitas_realizadas       = int(row["QTD VISITAS REALIZADAS"]),
                last_meeting                 = row["LAST MEETING"].date() if not isna(row["LAST MEETING"]) else None,
                next_meeting                 = row["NEXT MEETING"].date() if not isna(row["NEXT MEETING"]) else None,
                po_data                      = row["PO (DATA)"].date() if not isna(row["PO (DATA)"]) else None,
                perc_conclusao_ferramental   = row["% DE CONCLUSÃO DO FERRAMENTAL"],
                otop                         = row["OTOP"],
                spv                          = row["SPV"],
                iaa                          = row["IAA"],
                data_benestare               = row["DATA BENESTARE"].date() if not isna(row["DATA BENESTARE"]) else None,
                data_ppap_full               = row["DATA PPAP FULL"].date() if not isna(row["DATA PPAP FULL"]) else None,
                status_projeto               = row["STATUS PROJETO"],
                sop_executado                = row["SOP EXECUTADO"],
                status_sop                   = row["STATUS SOP"],
            ))
        Projeto.objects.bulk_create(objs)

        self.stdout.write(self.style.SUCCESS("Importação de Projetos concluída."))
