# ics_app/management/commands/update_pedidos.py

import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from ics_app.models import Pedido

class Command(BaseCommand):
    help = "Importa dados de Pedidos do Excel para o modelo Pedido"

    def handle(self, *args, **options):
        # 1) Leia o Excel completo
        df = pd.read_excel(settings.BASE_COMPLETA_INICIATIVA_PATH)

        # 2) Converta as colunas de data (ajuste nomes conforme seu Excel)
        date_cols = [
            'Data do documento_Compromisso',
            'Data de lançamento_sq01',
        ]
        for col in date_cols:
            if col in df.columns:
                df[col] = (
                    pd.to_datetime(df[col], dayfirst=True, errors='coerce')
                      .dt.date
                )

        # 3) Filtre apenas linhas com número de requisição/PO
        po_col = 'requisicao_de_compras_agrp_rda_po'
        df = df[df[po_col].notna()]

        # 4) Apague dados antigos e prepare instâncias
        Pedido.objects.all().delete()
        pedidos = []
        for _, row in df.iterrows():
            pedidos.append(Pedido(
                iniciativa               = row.get('iniciativa'),
                definicao_projeto        = row.get('Definição do projeto_Compromisso'),
                elemento_pep             = row.get('Elemento PEP_Compromisso'),
                requisicao_compras       = str(row.get(po_col)),
                doc_compra               = row.get('doc_compra'),
                data_documento           = row.get('Data do documento_Compromisso'),
                fornecedor_codigo        = row.get('Fornec_sq00'),
                razao_social             = row.get('RazSoc_sq00'),
                empresa_compromisso      = row.get('Empresa_Compromisso'),
                cpg                      = row.get('Cpg_sq00'),
                denominacao              = row.get('Denomi_sq00'),
                moeda                    = row.get('Moeda_me2n'),
                preco_liquido            = row.get('Preço líq._sq01'),
                data_lancamento          = row.get('Data de lançamento_sq01'),
                montante                 = row.get('Montante_sq01'),
                comprador                = row.get('Comprador_sq00'),
            ))

        # 5) Insira tudo de uma vez
        Pedido.objects.bulk_create(pedidos)

        # 6) Mensagem de sucesso
        self.stdout.write(self.style.SUCCESS(
            f"{len(pedidos)} pedidos importados com sucesso."
        ))
